
## imports
from datetime import datetime

from utils.similarity_helper import (create_array, 
                                     combine_txt_img, 
                                     create_faiss_idx, 
                                     save_faiss_to_mongo) 
from utils.file_helper import save_pickle

import utils.setup_helper as sh 
import src.utils.database_helper as dbh 
from utils.settings import session


def main():
    # configurations + paths
    sh.load_env_vars()

    coll_name = "products"
    cols_needed = ["productid", "text_embed", "image_embed"]

#     NUM_K = click.prompt()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    DATA = session.data

    MODEL = DATA / "models"
    MODEL.mkdir(parents=True, exist_ok=True)

    SM_FOLDER = MODEL / f"{now}_content_RecomSys"
    SM_FOLDER.mkdir(parents=True, exist_ok=True)

    # load cursors from MongoDB
    docs = dbh.load_cursor(coll_name, cols_needed)
    docs = sorted(docs, key=lambda x: x["productid"])

    ar_prod, ar_txt, ar_img, idx_map = create_array(docs)

    ar_comb = combine_txt_img(ar_img, ar_txt)
    
    # 
    idx = create_faiss_idx(ar_comb, SM_FOLDER)      
    file_id = save_faiss_to_mongo(SM_FOLDER)


    # save files/ data
    # [PLACEHOLDER] save all? arrays in MongoDB incl Datum (--> now)
    # wie topk_knn speichern?

    path = "[FOLDER]/idx_map"   # oder in DB speichern?
    save_pickle(idx_map, path)

    # save arrays to SM_FOLDER ?
    # for name, ar in [
    #                 # ("product_ids", product_ids),
    #                 # ("text_emb", text_emb), 
    #                 # ("image_emb", image_emb),
    #                 ("embed_comb", ar_comb)]:
        
    #     save_path = SM_FOLDER / f"{name}.npy"
    #     np.save(save_path, ar)
    #     print(f"Saved {name}:\tshape: {ar.shape}")


if __name__ == "__main__":
    main()