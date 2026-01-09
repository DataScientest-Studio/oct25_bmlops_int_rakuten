## imports
import pandas as pd 
import numpy as np
from datetime import datetime
import pickle
# from sklearn.neighbors import NearestNeighbors
from pathlib import Path
import faiss
import click
from utils.settings import session
from utils.setup_helper import get_latest_training_folder, load_env_vars

# paths
@click.command()
@click.option("--query_pid", type=int, required=True, help="Product ID to query")
@click.option("--n_neighbors", type=int, default=10, help="Number of recommended neighbors")
def main(query_pid, n_neighbors):
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

    SM_FOLDER = MODEL / f"{latest_dir}" 

# load similarity matrices and id_to_index mapping
    map_path = SM_FOLDER / "faiss_id_to_index.pkl"
    with open(map_path, "rb") as f:
      id_to_index = pickle.load(f)

    path_dict = {}
    for name in ["faiss_product_ids", 
            #  "text_emb", 
            #  "image_emb", 
                f"faiss_top{n_neighbors}_neighbors", 
                "faiss_embed_comb",
                "faiss_index"]:
    
        if name != "faiss_index":
         path_dict[name]  = SM_FOLDER / f"{name}.npy"
        else:
            path_dict[name] = SM_FOLDER / "faiss_index.bin"

    product_ids =  np.load(path_dict["faiss_product_ids"])
    embed_comb =  np.load(path_dict["faiss_embed_comb"])
    topk_neighbors = np.load(path_dict[f"faiss_top{n_neighbors}_neighbors"])
    faiss_index = faiss.read_index(str(path_dict["faiss_index"]))

# "PREDICTION": querying similarity matrices
    #query_pid = args.query_pid
    query_index = id_to_index[query_pid]

# print(f"{'='*30}")
    print(f"--- Query Product ID: {query_pid} ---")
# print(f"{'='*30}")

# (A) Using sklearn NearestNeighbors
#    print("Recommended Product IDs (KNN):")
#    for rank, idx in enumerate(topk_neighbors[query_index]):
 #       rec_pid = product_ids[idx]
 #       print(f"\tRank {rank + 1}:\tProduct ID {rec_pid}")

# (B) Using FAISS
    d_faiss, i_faiss = faiss_index.search(embed_comb[query_index:query_index+1], 
                                      n_neighbors)

    print("Recommended Product IDs (FAISS):")
    for rank, idx in enumerate(i_faiss[0]):
        rec_pid = product_ids[idx]
        print(f"\tRank {rank + 1}:\tProduct ID {rec_pid}")

    print("faiss_embed_comb.shape:", embed_comb.shape)
    print("faiss_product_ids.shape:", product_ids.shape)
    print("faiss_topk_neighbors.shape:", topk_neighbors.shape)

# show raw neighbor indices for query by both methods
    print("faiss_topk_neighbors (precomputed):", topk_neighbors[query_index][:10])

    D_faiss, I_faiss = faiss_index.search(embed_comb[query_index:query_index+1], n_neighbors)
    print("faiss indices:", I_faiss[0][:10])
    print("faiss distances:", D_faiss[0][:10])

# quick equality checks
    print("arrays equal?:", np.array_equal(topk_neighbors[query_index], I_faiss[0]))
    print("any positions equal?:", np.any(topk_neighbors[query_index] == I_faiss[0]))
if __name__ == "__main__":
    main()