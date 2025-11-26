## 3_data_split.py
# imports
import time
import numpy as np
import click
import importlib
from pymongo import UpdateOne

import utils.db_helper as dh

importlib.reload(dh)

@click.command()
def main():

    cols_needed = ["_id", "productid"]
    coll_name = "products"
    NUM_SLICES = click.prompt("How many subgroups should be created?",
                              type=int,
                              default=5) 
    print(f"[INPUT] number of subgroups = {NUM_SLICES}") 
    # workflow
    
    df = dh.load_cursor(coll_name, cols_needed)
    if df is None:
        return None
    
    product_ids = list_products(df)
    create_subgroups(product_ids, 
                    NUM_SLICES,
                    coll_name)
    

def list_products(df):
    prod_list = df["product_id"].values().copy()
    return prod_list

def create_subgroups(id_list, n_subgroups, coll_name):
    # configuration + loading
    random_seed_numpy()
    
    collection = dh.load_collection(coll_name)

    # generate random subgroup assigment 
    subgroup = np.random.randint(0, 
                                n_subgroups, 
                                size=len(id_list))
    
    records = []
    for pid, group in zip(id_list, subgroup): 
        records.append(UpdateOne(
            {"productid": pid},
            {"$set": {"subgroup": group},
            "$currentDate": {"lastModified": True }}
        ))

    results = collection.bulk_write(records, ordered=False)      # prefer 'bulk_write' for multiple updates (> 85k records)
    print("Finished uploading 'subgroup' assignments.")
    print(f"Matched:\t{results.matched_count}")
    print(f"Modified:\t{results.modified_count}")
    

def random_seed_numpy():
    seed = int(time.time()) % 2**32               # 'randomly' generated seed
    np.random.seed(seed)
    print(f"[INFO] temporary seed set: {seed}")


if __name__ == "__main__":
    main()


# def df_from_mongodb(coll_name, cols):

#     df = dh.load_cursor(coll_name, cols)
#     if df is None:
#         return None
    
    

    # yield
    


