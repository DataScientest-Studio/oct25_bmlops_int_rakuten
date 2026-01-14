## data_handling.py
# imports
import time
import numpy as np
import pandas as pd
from pymongo import UpdateOne

from . import database_helper as dbh

# ------------------
# helper functions
# ------------------

def list_products(df):
    prod_list = df["product_id"].values().copy()
    return prod_list

def create_subgroups(id_list, num, coll_name=None):
    if coll_name:
        print(f"Start creating {num} subgroups from collection {coll_name}")
    else:
        print(f"Start creating {num} subgroups from file")

    # configuration + loading
    seed = random_seed_numpy()
    
    collection = dbh.load_collection(coll_name)

    # generate random subgroup assigment 
    subgroup = np.random.randint(0, 
                                num, 
                                size=len(id_list))
    
    records = []
    for pid, group in zip(id_list, subgroup): 
        records.append(UpdateOne(
            {"productid": pid},
            {"$set": {"subgroup": group, 
                      "subgroup_seed (np)": seed},
            "$currentDate": {"lastModified": True }}
        ))

    results = collection.bulk_write(records, ordered=False)      # prefer 'bulk_write' for multiple updates (> 85k records)
    print("Finished uploading 'SUBGROUP' assignments.")
    print(f"Matched:\t{results.matched_count}")
    print(f"Modified:\t{results.modified_count}")


def draw_samples(id_list, samp_size, coll_name=None):
    if coll_name:
        print(f"Start creating {samp_size} subgroups from collection {coll_name}")
    else:
        print(f"Start creating {samp_size} subgroups from file")

    # configuration + loading db collection
    seed = random_seed_numpy()
    
    collection = dbh.load_collection(coll_name)

    # draw samples
    samples = np.random.choice(id_list, size=samp_size, replace=False)

    # update records in db
    records = []
    for pid, group in zip(id_list, samples): 
        records.append(UpdateOne(
            {"productid": pid},
            {"$set": {"sample": "Yes", 
                      "sample_seed (np)": seed},
            "$currentDate": {"lastModified": True}}
        ))

    results = collection.bulk_write(records, ordered=False)      # prefer 'bulk_write' for multiple updates (> 85k records)
    print("Finished uploading 'SAMPLE' assignment.")
    print(f"Matched:\t{results.matched_count}")
    print(f"Modified:\t{results.modified_count}")


def random_seed_numpy():
    seed = int(time.time()) % 2**32               # 'randomly' generated seed
    np.random.seed(seed)
    print(f"[INFO] NumPy seed set: {seed}")
    return seed


def check_latest_products(df_dict, coll_name, days=30):
    # load MongoDB collection
    _, _, coll_dict = dbh.setup_mongodb()
    collection = coll_dict.get(coll_name)
    
    update_text = None
    update_image = None

    cols_needed = ["productid",
                   "upload_time (image)",
                   "upload_time (text)"]
    
    if collection is None:
        print(f"⚠️ No collection '{coll_name}' found in db")
        return None

    # obtain existing upload times from db
    df_db = dbh.load_cursor(coll_name, cols_needed)

    if df_db is None:
        return {"txt_update": "all", 
                "img_update": "all"}

    # convert upload times to datetime
    for col in ["upload_time (image)", "upload_time (text)"]:
        if col in df_db.columns:
            df_db[col] = pd.to_datetime(df_db[col], errors='coerce')
    
    # determine cutoff date
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)

    # filter outdated products
    update_image = {}
    update_text = {}

    for name, df in df_dict.items():
        if "productid" not in df.columns:
            print(f"⚠️ DataFrame '{name}' has no 'productid' column → skipped.")
            continue

        missing_products = set(df["productid"]) - set(df_db["product_id"])

        merged = df.merge(df_db, on="productid", how="left")

        need_img = merged[
            (merged["upload_time (image)"].isna()) | 
            (merged["upload_time (image)"] < cutoff)
            ]["productid"].tolist()

        need_txt = merged[
            (merged["upload_time (text)"].isna()) | 
            (merged["upload_time (text)"] < cutoff)
            ]["productid"].tolist()

        update_image[name] = sorted(set(need_img) | missing_products)
        update_text[name] = sorted(set(need_txt) | missing_products)

    return {
        "txt_update": update_text,
        "img_update": update_image
    }
