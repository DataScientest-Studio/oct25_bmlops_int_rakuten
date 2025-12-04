
## imports
from datetime import datetime
import click

from utils.similarity_helper import create_array, combine_txt_img, create_knn_sm
from utils.file_helper import save_pickle

import utils.setup_helper as sh 
import src.utils.database_helper as dbh 
# from utils.settings import session

@sh.cli_or_api
def main(num):
    # configurations + paths
    sh.load_env_vars()

    coll_name = "products"
    cols_needed = ["productid", "text_embed", "image_embed"]

#     NUM_K = click.prompt()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # DATA = session.data

    # MODEL = DATA / "models"
    # MODEL.mkdir(parents=True, exist_ok=True)

    # SM_FOLDER = MODEL / f"{now}_content_RecomSys"
    # SM_FOLDER.mkdir(parents=True, exist_ok=True)

    # load cursors from MongoDB
    docs = dbh.load_cursor(coll_name, cols_needed)
    docs = sorted(docs, key=lambda x: x["productid"])

    ar_prod, ar_txt, ar_img, idx_map = create_array(docs)

    ar_comb = combine_txt_img(ar_img, ar_txt)
    
    topk_knn = create_knn_sm(ar_comb, num_k=num)  # <-- CLICK

    # save files/ data
    # [PLACEHOLDER] save all? arrays in MongoDB incl DAtum (--> now)
    # wie topk_knn speichern?

    path = "[FOLDER]/idx_map"
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


@click.command()
@click.option("--num", 
              type=int, #click.choices=(["core", "heavy_+", "dev_+", "all"]), 
              default=10, 
              required=False)
def main_entry_check(num):
    main(num)

if __name__ == "__main__":
    main_entry_check()

