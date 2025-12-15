##
# imports 
# import importlib
# import os
# import pandas as pd 
# import numpy as np
 

import utils.ETL_preprocess_helper as eph 
# import src.setup_helper as sh 
import utils.database_helper as dbh 
# from utils.settings import session

# importlib.reload(sh)
# importlib.reload(dh)

def text_embed(coll_name=None, cols_needed=None):
    # # load env variables from .env and .env.session
    # sh.load_env_vars()

    # # load paths
    # sh.get_paths()
    # DATA = session.data

    # DATA_PROCESSED = DATA / "processed"
    # DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # DATA_LAKE = DATA / "data_lake"
    # DATA_LAKE.mkdir(parents=True, exist_ok=True)

    # load collection from MongoDB + load data from collection
    if not coll_name:   
        coll_name = "products"
    
    if not cols_needed:
       cols_needed = ["clean_designation", "clean_description",
                      "productid"]

    # workflow
    df = dbh.load_cursor(coll_name, cols_needed)
    if df is None:
        return None
    
    # due to memory limits, we will not proceed with embedding for now
    print("⚠️ Creating embedding from text skipped due to memory limits.")
    return None

    # df_prep = eph.prepare_embed(df)
    # df_emb = eph.embed_text(df_prep)
    # dbh.upload_embeds(df_emb, coll_name)

if __name__ == "__main__":
    text_embed()
