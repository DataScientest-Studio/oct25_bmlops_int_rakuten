import click
import numpy as np
import pickle
from pathlib import Path
from utils.setup_helper import get_latest_training_folder, load_env_vars
from utils.settings import session


@click.command()
@click.option("--query_pid", type=int, required=True, help="Product ID to query")
@click.option("--n_neighbors", type=int, default=10, help="Number of recommended neighbors")
def main(query_pid, n_neighbors):

    # Load env / paths
    load_env_vars()

    if session.root is None:
        session.root = Path(".").resolve()
    if session.data is None:
        session.data = session.root / "data"
    if session.venv is None:
        session.venv = session.root / ".venv"

    DATA = session.data
    MODEL = DATA / "models"

    latest_dir = get_latest_training_folder(MODEL).name
    SM_FOLDER = MODEL / latest_dir

    # -------- Load mapping + data --------
    with open(SM_FOLDER / "idx_map.pkl", "rb") as f:
        id_to_index = pickle.load(f)

    product_ids = np.load(SM_FOLDER / "knn_product_ids.npy")
    embed_comb = np.load(SM_FOLDER / "knn_embed_comb.npy")
    topk_neighbors = np.load(SM_FOLDER / f"knn_top{n_neighbors}_neighbors.npy")

    # -------- Query index --------
    if query_pid not in id_to_index:
        print(f"❌ Product ID {query_pid} not found!")
        return

    query_index = id_to_index[query_pid]

    print(f"\n=== KNN Recommendation for Product {query_pid} ===")

    # -------- Print Recommendations --------
    for rank, idx in enumerate(topk_neighbors[query_index]):
        rec_pid = product_ids[idx]
        print(f"  Rank {rank + 1}: Product ID {rec_pid}")

    print()


if __name__ == "__main__":
    main()