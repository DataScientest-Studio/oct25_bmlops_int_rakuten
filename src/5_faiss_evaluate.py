import numpy as np
import pandas as pd
import pickle
from pathlib import Path

from utils.settings import session
from utils.setup_helper import load_env_vars, get_latest_training_folder
import utils.db_helper as dh


def main():
    load_env_vars()

    # ---- Load model folder ----
    if session.root is None:
        session.root = Path(".").resolve()

    DATA = session.root / "data"
    MODEL = DATA / "models"
    latest = get_latest_training_folder(MODEL)
    SM_FOLDER = MODEL / latest.name

    print(f"Using Faiss model folder: {SM_FOLDER}")

    # ---- Load arrays ----
    product_ids = np.load(SM_FOLDER / "faiss_product_ids.npy")
    topk_neighbors = np.load(SM_FOLDER / "faiss_top10_neighbors.npy")

    with open(SM_FOLDER / "faiss_id_to_index.pkl", "rb") as f:
        id_to_index = pickle.load(f)

    K = topk_neighbors.shape[1]

    # ---- Load prdtypecode from MongoDB ----
    df = dh.load_cursor("products", ["productid", "prdtypecode"])
    df = df.sort_values("productid")
    prdtype_arr = df["prdtypecode"].to_numpy()

    # Safety check
    assert len(product_ids) == len(prdtype_arr), \
        "Mismatch: product_ids and prdtypecode length differ!"

    # ---- Evaluation ----
    cat_match_counts = np.zeros(len(product_ids), dtype=int)

    for i in range(len(product_ids)):
        true_cat = prdtype_arr[i]
        neighbors = topk_neighbors[i]
        match = np.sum(prdtype_arr[neighbors] == true_cat)
        cat_match_counts[i] = match

    avg_score = np.mean(cat_match_counts / K)
    distribution = np.bincount(cat_match_counts, minlength=K+1)

    # ---- Print results ----
    print("\n===== KNN Category-Consistency Evaluation =====")
    print(f"Average category match score: {avg_score:.4f}")

    print("\nDistribution of matches (0..10):")
    for i, count in enumerate(distribution):
        print(f"{i} matches: {count}")

    # ---- Save CSV results ----
    out_df = pd.DataFrame({
        "productid": product_ids,
        "prdtypecode": prdtype_arr,
        "matched_categories_top10": cat_match_counts
    })

    out_path = SM_FOLDER / "faiss_evaluation_category_match_top10.csv"
    out_df.to_csv(out_path, index=False)

    print("\nSaved evaluation CSV to:")
    print(out_path)


if __name__ == "__main__":
    main()