
## imports
import pandas as pd 
import numpy as np
from datetime import datetime
import pickle
from sklearn.neighbors import NearestNeighbors
import faiss

from utils.setup_helper import setup_mongodb, load_env_vars

# paths
now = datetime.now().strftime("%Y%m%d_%H%M%S")

ROOT, DATA, VENV, args = load_env_vars()

MODEL = DATA / "models"
MODEL.mkdir(parents=True, exist_ok=True)
now = datetime.now().strftime("%Y%m%d_%H%M%S")
SM_FOLDER = MODEL / f"{now}_content_RecomSys"
SM_FOLDER.mkdir(parents=True, exist_ok=True)

# connect to MongoDB
db, collection = setup_mongodb()

cursor = collection.find(
    {},
    {"_id": 0, 
     "productid": 1, 
     "text_embed": 1,
     "image_embed": 1}
    )

docs = list(cursor)
docs = sorted(docs, key=lambda x: x["productid"])

# create numpy arrays for recommender system
product_ids = np.array([d["productid"] for d in docs], dtype=np.int32)
text_emb = np.array([d["text_embed"] for d in docs], dtype=np.float32)
image_emb= np.array([d["image_embed"] for d in docs], dtype=np.float32)

# create id to index mapping
id_to_index = {pid: i for i, pid in enumerate(product_ids)}

# if necessary, normalize vectors
def l2_norm(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)

image_emb = l2_norm(image_emb)
# txt_emb = l2_norm(text_emb) 

# combining vectors to recommender system matrix
alpha = 0.3          # weight for image vector
beta = 1- alpha      # weight for text vector

embed_comb = np.hstack([alpha * image_emb, beta * text_emb])
embed_comb = l2_norm(embed_comb.astype("float32"))

# save arrays to SM_FOLDER
for name, ar in [("product_ids", product_ids),
                 ("text_emb", text_emb), 
                 ("image_emb", image_emb),
                 ("embed_comb", embed_comb)]:
    save_path = SM_FOLDER / f"{name}.npy"
    np.save(save_path, ar)
    print(f"Saved {name}:\tshape: {ar.shape}")

# save id_to_index as pickle
with open("id_to_index.pkl", "wb") as f:
    pickle.dump(id_to_index, f)

## "TRAINING": calculating similarity matrices
# (A) KNN with cosine similarity

knn = NearestNeighbors(metric="cosine", 
                       n_neighbors=args.n_neighbors)

neighbors = knn.kneighbors(embed_comb, return_distance=False)
np.save(f"{SM_FOLDER}/top_{args.n_neighbors}_knn.npy", neighbors)

# (B) FAISS library
d = embed_comb.shape[1]
index = faiss.IndexFlatIP(d)  # Using Inner Product for Cosine Similarity
index.add(embed_comb) 

faiss.write_index(index, f"{SM_FOLDER}/faiss_index_flatip.bin")
