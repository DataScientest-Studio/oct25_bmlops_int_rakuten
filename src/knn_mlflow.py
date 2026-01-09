from datetime import datetime
from pathlib import Path
import pickle
import os
import numpy as np
import pandas as pd
import mlflow
import mlflow.pyfunc
import click
# Utils
import utils.setup_helper as sh
import utils.db_helper as dh
from utils.settings import session
from utils.file_helper import save_pickle2
from utils.similarity_helper import create_array, combine_txt_img, create_knn_sm

# ----------------- MLflow Setup -----------------
mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
)
mlflow.set_experiment("Recos")

def build_knn(num_k=10, combine_weight=0.6):
    sh.load_env_vars()

    if session.root is None:
        session.root = Path(".").resolve()
    if session.data is None:
        session.data = session.root / "data"

    DATA = session.data
    MODEL = DATA / "models"
    MODEL.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    sm_folder = MODEL / f"{now}_content_RecomSys"
    sm_folder.mkdir(parents=True, exist_ok=True)
    print(f"[SAVE FOLDER] {sm_folder}")

    mlflow.log_param("num_k", num_k)
    mlflow.log_param("combine_weight", combine_weight)


    df = dh.load_cursor("products", ["productid", "text_embed", "embedding_img"])
    docs = df.sort_values("productid").to_dict(orient="records")
    df2 = df.sort_values("productid")


    input_path = sm_folder / "products_input.parquet"
    df2.to_parquet(input_path, index=False)
    #mlflow.log_artifact(input_path)

    mlflow.log_param("input_rows", len(df2))
    mlflow.log_param("input_cols", len(df2.columns))
    mlflow.log_param("input_file", "products_input.parquet")
    ar_prod, ar_txt, ar_img, idx_map = create_array(docs)
    ar_comb = combine_txt_img(ar_img, ar_txt, combine_weight)


    topk_knn = create_knn_sm(ar_comb, num_k=num_k)

    with open(sm_folder / "idx_map.pkl", "wb") as f:
        pickle.dump(idx_map, f)
    np.save(sm_folder / "knn_product_ids.npy", ar_prod)
    np.save(sm_folder / "knn_embed_comb.npy", ar_comb)
    np.save(sm_folder / f"knn_top{num_k}_neighbors.npy", topk_knn)
    save_pickle2(idx_map, sm_folder / "knn_id_to_index.pkl")

    #mlflow.log_artifact(sm_folder / f"knn_top{num_k}_neighbors.npy")
    #mlflow.log_artifact(sm_folder / "knn_embed_comb.npy")
    #mlflow.log_artifact(sm_folder / "idx_map.pkl")

    mlflow.log_artifact(input_path, artifact_path="models")
    mlflow.log_artifact(sm_folder / f"knn_top{num_k}_neighbors.npy", artifact_path="models")
    mlflow.log_artifact(sm_folder / "knn_embed_comb.npy", artifact_path="models")
    mlflow.log_artifact(sm_folder / "idx_map.pkl", artifact_path="models")

    

    print("[DONE] Saved KNN similarity files and logged to MLflow.")
    return sm_folder, topk_knn, ar_prod

def evaluate_knn(sm_folder, topk_neighbors, product_ids, K=10):
    df = dh.load_cursor("products", ["productid", "prdtypecode"])
    df = df.sort_values("productid")
    prdtype_arr = df["prdtypecode"].to_numpy()

    assert len(product_ids) == len(prdtype_arr), \
        "Mismatch: product_ids und prdtypecode Länge unterschiedlich!"

    cat_match_counts = np.zeros(len(product_ids), dtype=int)
    for i in range(len(product_ids)):
        true_cat = prdtype_arr[i]
        neighbors = topk_neighbors[i]
        match = np.sum(prdtype_arr[neighbors] == true_cat)
        cat_match_counts[i] = match

    avg_score = np.mean(cat_match_counts / K)
    distribution = np.bincount(cat_match_counts, minlength=K+1)


    mlflow.log_metric("avg_category_match_score", avg_score)
    for i, count in enumerate(distribution):
        mlflow.log_metric(f"matches_{i}", count)

    print("\n===== KNN Category-Consistency Evaluation =====")
    print(f"Average category match score: {avg_score:.4f}")
    print(f"\nDistribution of matches (0..{K}):")
    for i, count in enumerate(distribution):
        print(f"{i} matches: {count}")

    out_df = pd.DataFrame({
        "productid": product_ids,
        "prdtypecode": prdtype_arr,
        "matched_categories_top10": cat_match_counts
    })
    out_path = sm_folder / "knn_evaluation_category_match_top10.csv"
    out_df.to_csv(out_path, index=False)
    mlflow.log_artifact(out_path)
    print(f"\nSaved evaluation CSV to: {out_path}")

    return avg_score

# ----------------- pyfunc Model Wrapper -----------------
class KNNSimilarityModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        with open(context.artifacts["idx_map"], "rb") as f:
            self.idx_map = pickle.load(f)
        self.ar_comb = np.load(context.artifacts["ar_comb"])

    def predict(self, context, product_id):
        idx = self.idx_map[product_id]
        return self.ar_comb[idx]

# ----------------- CLI Wrapper -----------------
@click.command()
@click.option("--num_k", type=int, default=10, help="Number of top K neighbors")
@click.option("--combine_weight", type=float, default=0.4, help="Weight for combining text and image embeddings")
def cli(num_k, combine_weight):
    with mlflow.start_run(run_name="KNN"):
        sm_folder, topk_neighbors, product_ids = build_knn(num_k, combine_weight)
        K = topk_neighbors.shape[1]
        evaluate_knn(sm_folder, topk_neighbors, product_ids, K)

        mlflow.pyfunc.log_model(
            name="knn_model",
            python_model=KNNSimilarityModel(),
            artifacts={
                "idx_map": str(sm_folder / "idx_map.pkl"),
                "ar_comb": str(sm_folder / "knn_embed_comb.npy")
            }
        )

# ----------------- Entry Point -----------------
if __name__ == "__main__":
    cli()