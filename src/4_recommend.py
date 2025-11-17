## imports
import pandas as pd 
import numpy as np
from datetime import datetime
import pickle
# from sklearn.neighbors import NearestNeighbors
import faiss

from utils.setup_helper import get_latest_training_folder, load_env_vars

# paths
ROOT, DATA, VENV, args = load_env_vars()

MODEL = DATA / "models" 
latest_dir = get_latest_training_folder(MODEL).name

SM_FOLDER = MODEL / f"{latest_dir}" 

# load similarity matrices and id_to_index mapping
map_path = SM_FOLDER / "id_to_index.pkl"
with open(map_path, "rb") as f:
    id_to_index = pickle.load(f)

path_dict = {}
for name in ["product_ids", 
            #  "text_emb", 
            #  "image_emb", 
            f"top{args.n_neighbors}_neighbors", 
             "embed_comb",
             "faiss_index_flatip"]:
    
    if name != "faiss_index_flatip":
        path_dict[name]  = SM_FOLDER / f"{name}.npy"
    else:
        path_dict[name] = SM_FOLDER / "faiss_index_flatip.bin"

product_ids =  np.load(path_dict["product_ids"])
embed_comb =  np.load(path_dict["embed_comb"])
topk_neighbors = np.load(path_dict[f"top{args.n_neighbors}_neighbors"])
faiss_index = faiss.read_index(str(path_dict["faiss_index_flatip"]))

# "PREDICTION": querying similarity matrices
query_pid = args.query_pid
query_index = id_to_index[query_pid]

# print(f"{'='*30}")
print(f"--- Query Product ID: {query_pid} ---")
# print(f"{'='*30}")

# (A) Using sklearn NearestNeighbors
print("Recommended Product IDs (KNN):")
for rank, idx in enumerate(topk_neighbors[query_index]):
    rec_pid = product_ids[idx]
    print(f"\tRank {rank + 1}:\tProduct ID {rec_pid}")

# (B) Using FAISS
d_faiss, i_faiss = faiss_index.search(embed_comb[query_index:query_index+1], 
                                      args.n_neighbors)

print("Recommended Product IDs (FAISS):")
for rank, idx in enumerate(i_faiss[0]):
    rec_pid = product_ids[idx]
    print(f"\tRank {rank + 1}:\tProduct ID {rec_pid}")