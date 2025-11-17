## imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import numpy as np
import faiss
import pickle
from pathlib import Path
from sklearn.neighbors import NearestNeighbors

from utils.setup_helper import get_latest_training_folder, load_env_vars

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
ROOT, DATA, VENV, args = load_env_vars()

# DATA_ROOT = Path("./data")

MODEL = DATA / "models" 
latest_dir = get_latest_training_folder(MODEL).name

SM_FOLDER = MODEL / f"{latest_dir}"
EMB_COMBINED = SM_FOLDER / "embed_comb.npy"
PRODUCT_IDS = SM_FOLDER / "product_ids.npy"
ID_TO_INDEX = SM_FOLDER / "id_to_index.pkl"
FAISS_INDEX = SM_FOLDER / "faiss_index_flatip.bin"

# candidates = [f for f in SM_FOLDER.iter() if f.isfile() and f.name.startswith("top_") and (f.name.endswith("_knn") or f.name.endswith("_fiass"))]
TOPK_KNN = Path([f for f in SM_FOLDER.iter() if f.isfile() and f.name.startswith("top_") and f.name.endswith("_knn")])
                # f for f in candidates if f.name.endswith("_knn")])
                
#                 fSM_FOLDER / f"top_{args.n_neighbors}_knn.npy"
# TOPK_FAISS = SM_FOLDER / f"top_{args.n_neighbors}_faiss.npy"

TOPK_DEFAULT = 5 # args.n_neighbors
METHOD_DEFAULT = "both"

# ---------------------------------------------------
# API initialization
# ---------------------------------------------------
app = FastAPI(title="Product Recommendation API (content-based)")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@app.on_event("startup")        # auch vor 'AUSFÜHRUNG API_QUERY'
def load_data():
    global embed_combined, product_ids, id_to_index, faiss_index, topk_knn

    print("Loading data...")
    embed_combined = np.load(EMB_COMBINED)
    product_ids = np.load(PRODUCT_IDS)

    with open(ID_TO_INDEX, "rb") as f:
        id_to_index = pickle.load(f)

    faiss_index = faiss.read_index(str(FAISS_INDEX))
    topk_knn = np.load(TOPK_KNN)
    print("Data loaded successfully.")

# ---------------------------------------------------
# Request and Response Models
# ---------------------------------------------------
class CreateSMRequest(BaseModel):
    top_k: int = TOPK_DEFAULT

class RecommendRequest(BaseModel):
    product_id: int
    top_k: int = TOPK_DEFAULT
    method: str = METHOD_DEFAULT  # choice = ["knn", "faiss" "both"]

# class RecommendResponse(BaseModel):
    # recommended_product_ids: List[int]

# ---------------------------------------------------
# API Endpoint 1: Create Similarity Datamatrices
# ---------------------------------------------------
@app.post("/create_sm", 
          summary="Create Similarity Matrix", 
          tags=["similarity_matrix"])
def create_similarity_matrix(request: CreateSMRequest):
    top_k = request.top_k
    
    global topk_faiss, faiss_index, embed_combined
    
    # # (A) KNN with cosine similarity
    print(f"KNN: Computing top-{top_k} neighbors for all products…")
    knn = NearestNeighbors(metric="cosine", 
                        n_neighbors=top_k)

    topk_knn = knn.kneighbors(embed_combined, return_distance=False)
    
    np.save(TOPK_KNN, topk_knn) 
#         f"{SM_FOLDER}/top_{top_k}_knn.npy", neighbors) 
    
    # (B) FAISS
    print(f"FAISS: Computing top-{top_k} neighbors for all products…")
    d = embed_combined.shape[0]
    index_faiss = faiss.IndexFlatIP(d)
    # _, indices = faiss_index.search(embed_combined, top_k)

    # topk_faiss = indices
    faiss.write_index(index_faiss, FAISS_INDEX)

    # n_products = embed_combined.shape[0]
    # similarity_matrix = np.zeros((n_products, top_k), dtype=int)

    # for idx in range(n_products):
    #     similarity_matrix[idx] = topk_neighbors[idx, 1:top_k + 1]

    # sm_file = DATA_ROOT / f"similarity_matrix_topk_{top_k}.npy"
    # np.save(sm_file, similarity_matrix)
    return {"status": "done",
            "message": f"Similarity matrices (KNN + FAISS, top_k={top_k}) saved in SM_FOLDER."}

# ---------------------------------------------------
# Endpoint 2: Recommend products
# ---------------------------------------------------
@app.post("/recommend")
def recommend(req: RecommendRequest):

    if req.product_id not in id_to_index:
        raise HTTPException(status_code=404, 
                            detail="Product ID not found")

    PID = req.product_id
    k = req.top_k

    mode = []
    mode.append("knn") if req.method in ["knn", "both"]
    mode.append("faiss") if req.method in ["faiss", "both"]

    if mode is None:
        print("⚠️ ERROR (500): Invalid input for 'method'.") # print()        

    idx = id_to_index[PID]

    # Use top-k precomputed neighbors if available
    if "knn" in mode:
        if topk_knn is not None:
            indices_knn = topk_knn[idx][:k]
            recommend_knn = product_ids[indices_knn].tolist()

        else: 
            recommend_knn = "⚠️ HTTPException (404): Since KNN data is missing, 'recommend (KNN)' cannot be computed"
    else:
        recommend_knn = "not requested"

    # On-demand FAISS query
    if "faiss" in mode:
        if faiss_index is None:
            recommend_knn = "⚠️ HTTPException (404): Since FAISS index is missing, 'recommend (FAISS)' cannot be computed"
            # raise HTTPException(
            #     status_code=500,
            #     detail="FAISS index missing and top-k neighbors not computed"
            #     )
        
        else:
            _, indices_faiss = faiss_index.search(embed_combined[idx:idx+1], k)
            idx_faiss = indices_faiss[0]

            # Map embedding indices → product ids
            recommend_faiss = product_ids[idx_faiss].tolist()
    else:
        recommend_faiss = "not requested"

    return {
        "product_id": PID,
        "n_neighbors": k,
        "recommended (KNN)": recommend_knn,
        "recommended (FAISS)": recommend_faiss
    }
