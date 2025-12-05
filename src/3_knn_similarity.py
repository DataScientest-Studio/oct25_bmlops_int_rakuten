from datetime import datetime
import numpy as np
from pathlib import Path
import pickle

import utils.setup_helper as sh
import utils.db_helper as dh
from utils.settings import session
from utils.file_helper import save_pickle2
from utils.similarity_helper import (
    create_array,
    combine_txt_img,
    create_knn_sm
)

def main(num_k):
    sh.load_env_vars()

    # Resolve base paths
    if session.root is None:
        session.root = Path(".").resolve()
    if session.data is None:
        session.data = session.root / "data"
    if session.venv is None:
        session.venv = session.root / ".venv"

    DATA = session.data
    MODEL = DATA / "models"
    MODEL.mkdir(parents=True, exist_ok=True)

    # Create timestamp folder
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    SM_FOLDER = MODEL / f"{now}_content_RecomSys"
    SM_FOLDER.mkdir(parents=True, exist_ok=True)

    print(f"[SAVE FOLDER] {SM_FOLDER}")

    # Load docs
    df = dh.load_cursor("products", ["productid", "text_embed", "embedding_str"])
    docs = df.sort_values("productid").to_dict(orient="records")

    # Build arrays
    ar_prod, ar_txt, ar_img, idx_map = create_array(docs)
    ar_comb = combine_txt_img(ar_img, ar_txt, 0.6)

    # Compute topK KNN similarity matrix
    topk_knn = create_knn_sm(ar_comb, num_k=num_k)

    # ---------- SAVE ----------
    with open(SM_FOLDER / "idx_map.pkl", "wb") as f:
        pickle.dump(idx_map, f)

    np.save(SM_FOLDER / "knn_product_ids.npy", ar_prod)
    np.save(SM_FOLDER / "knn_embed_comb.npy", ar_comb)
    np.save(SM_FOLDER / f"knn_top{num_k}_neighbors.npy", topk_knn)
    save_pickle2(idx_map, SM_FOLDER / "knn_id_to_index.pkl")

    print("[DONE] Saved KNN similarity files.")


# CLI wrapper
import click
@click.command()
@click.option("--num_k", type=int, default=10)
def cli(num_k):
    main(num_k)

if __name__ == "__main__":
    cli()