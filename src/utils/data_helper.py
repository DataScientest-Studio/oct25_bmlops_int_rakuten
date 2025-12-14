## data_handling.py
# imports
import os
import time
import numpy as np
from pymongo import UpdateOne

import utils.db_helper as dh

### 
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
    
    collection = dh.load_collection(coll_name)

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

    # configuration + loading
    seed = random_seed_numpy()
    
    collection = dh.load_collection(coll_name)

    samples = np.random.choice(id_list, size=samp_size, replace=False)

    records = []
    for pid, group in zip(id_list, samples): 
        records.append(UpdateOne(
            {"productid": pid},
            {"$set": {"sample": "Yes", 
                      "sample_seed (np)": seed},
            "$currentDate": {"lastModified": True }}
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


