
## imports
from datetime import datetime
from pathlib import Path
import numpy as np
from utils.similarity_helper import (create_array, 
                                     combine_txt_img, 
                                     create_faiss_idx, 
                                     save_faiss_to_mongo, 
                                     faiss_search) 
from utils.file_helper import save_pickle2

import utils.setup_helper as sh 
import utils.db_helper as dh 
from utils.settings import session


def main():
    # configurations + paths
    sh.load_env_vars()

    coll_name = "products"
    cols_needed = ["productid", "text_embed", "embedding_str"]

#     NUM_K = click.prompt()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    if session.root is None:
        session.root = Path(".").resolve()

    if session.data is None:
        session.data = session.root / "data"

    if session.venv is None:
        session.venv = session.root / ".venv"
    DATA = session.data

    MODEL = DATA / "models"
    MODEL.mkdir(parents=True, exist_ok=True)

    SM_FOLDER = MODEL / f"{now}_content_RecomSys"
    SM_FOLDER.mkdir(parents=True, exist_ok=True)

    # load cursors from MongoDB
    df = dh.load_cursor(coll_name, cols_needed)
    docs = df.sort_values("productid").to_dict(orient="records")
    

    ar_prod, ar_txt, ar_img, idx_map = create_array(docs)

    ar_comb = combine_txt_img(ar_img, ar_txt, 0.3)
    
    # 
    faiss_index_path = SM_FOLDER / "faiss_index.bin"
    idx = create_faiss_idx(ar_comb, faiss_index_path)  
    k = 10
    topk_neighbors = np.zeros((len(ar_comb), k), dtype=np.int64)
    for i in range(len(ar_comb)):
        indices, _ = faiss_search(idx, ar_comb[i:i+1], k=k)
        topk_neighbors[i] = indices

# Speichern
   # np.save(SM_FOLDER / f"top{k}_neighbors.npy", topk_neighbors)    
    file_id = save_faiss_to_mongo(SM_FOLDER)

    

    # save files/ data
    # [PLACEHOLDER] save all? arrays in MongoDB incl Datum (--> now)
    # wie topk_knn speichern?

   # path = SM_FOLDER/"id_to_index.pkl"   # oder in DB speichern?
   # save_pickle2(idx_map, path)

 #   save arrays to SM_FOLDER ?
 #   for name, ar in [
 #                    ("product_ids", product_ids),
 #                    ("text_emb", text_emb), 
 #                    ("image_emb", image_emb),
 #                    ("embed_comb", ar_comb)]:
 #       
 #           save_path = SM_FOLDER / f"{name}.npy"
 #           np.save(save_path, ar)
 #           print(f"Saved {name}:\tshape: {ar.shape}")

    SM_FOLDER = MODEL / f"{now}_content_RecomSys"
    np.save(SM_FOLDER / "faiss_product_ids.npy", ar_prod)
    np.save(SM_FOLDER / "faiss_embed_comb.npy", ar_comb)
    np.save(SM_FOLDER / f"faiss_top{k}_neighbors.npy", topk_neighbors)
    save_pickle2(idx_map, SM_FOLDER / "faiss_id_to_index.pkl")
if __name__ == "__main__":
    main()