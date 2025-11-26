##
# imports 
import importlib
import os
# from pathlib import Path
import re
from datetime import datetime  

import click
import pandas as pd
import numpy as np
from pymongo import UpdateOne

import utils.ETL_preprocess_helper as eph 
import utils.setup_helper as sh 
import utils.db_helper as dh 
from utils.settings import session

importlib.reload(eph)
importlib.reload(sh)
importlib.reload(dh)

@click.command()
def main():
    # load env variables from .env and .env.session
    sh.load_env_vars()

    # load paths
    sh.get_paths()
    DATA = session.data 
    
    DATA_LAKE = DATA / "data_lake"
    DATA_LAKE.mkdir(parents=True, exist_ok=True)

    DATA_PROCESSED = DATA / "data_processed"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # load parsed arguments
    raw = click.prompt("Which files should be used in ETL pipeline?", #click.Choice(["core", "+_heavy", "+_dev", "all"]), 
                        default="",
                        show_default=False
                        )

    if raw.strip() == "":
        F_NAMES = None
    else:
        F_NAMES = [f.strip() for f in re.split(r"[ ,]+", raw.strip())]

    print(f"[INPUT] File name(s) = {F_NAMES}")
    
    # workflow  
    df_dict = data_preview(DATA_LAKE)
    if not df_dict:
        print("Files cannot be found. Please check the input.")
        return None
        
    dfs_to_update = eph.check_latest_products(df_dict, "products")
    if not dfs_to_update:
        print("✅ Database is up-to-date")
        return None
    
    cleaned_dfs = eph.clean_text(dfs_to_update, F_NAMES)
    dfs = merge_dfs(cleaned_dfs, F_NAMES)
    if not dfs:
        return None
                
    upload_data_mongoDB(dfs, F_NAMES) 
                

def data_preview(lake, f_names=None):
    """
    Docstring for data_preview
    
    :param lake: Description
    :param f_names: Description
    """
    ## data preview
    if not f_names:
        f_names = ["X_test_update", "X_train_update", "Y_train_CVw08PX"]

    now_etl = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_dict = {}
    for f in f_names:
        f_path = os.path.join(lake, f"{f}.csv")
        try:
            df = pd.read_csv(f_path)
            df = df.rename(columns={"Unnamed: 0": "id"}) 
            df["now"] = now_etl 
            df_dict[f] = df
            sh.log_header("EDA RAW DATA")
            # print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")

        except Exception as e:
            print(f"⚠️ Loading {f}: Error occured:\n{e}")

    return df_dict if len(df_dict) > 0 else None

def merge_dfs(dfs, names=None):
    """
    Docstring for merge_dfs
    
    :param dfs: Description
    :param names: Description
    """
    ## merge data frames
    if not names:
        names = ["df_train", "df_test"]

        df_train = pd.merge(dfs["X_train_update"], 
                            dfs["Y_train_CVw08PX"], 
                            on='id',
                            how='outer')

        df_test = dfs["X_test_update"].copy()
        df_test['prdtypecode'] = np.nan

        for name, df in zip(names,
                        [df_train, df_test]): 
            sh.log_header(f"CHECK MERGED DF ('{name}')")
            # print(f"\n{'='*30}\n--- CHECK MERGED DF ('{name}') ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")
        
        return [df_train, df_test]

    else: 
        print("Function probably not yet suitable for that input. Please check.")
        return None 


def upload_data_mongoDB(dfs, names=None, coll_name="product"):
    """
    Docstring for upload_data_mongoDB
    
    :param dfs: Description
    :param names: Description
    :param coll_name: Description
    """
    # load MongoDB collection
    collection = dh.load_collection(coll_name)

    # loading data into MongoDB
    now_db = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    allowed_cols = ['_id', 'prdtypecode', 
                    'designation', 'clean_designation',
                    'description', 'clean_description',
                    'productid', 'imageid',
                    "upload_time (text)",
                    "upload_time (image)"]

    if not names:
        names = ["df_train", "df_test"]

        for name, df in zip(names, 
                            dfs):
            # df = pd.read_csv(f"{DATA_PROCESSED}/{f}_clean.csv", index_col=0)
            cols = [col for col in allowed_cols if col in df.columns]
            
            data = df[cols].copy()
            data["source"] = name
            data["upload_time (text)"] = now_db

            records = []
            records.append(UpdateOne(
                            {"productid": data["productid"]},
                            {"$set": data,
                            "$currentDate": {"lastModified": True }},
                            upsert=True
                            ))

            collection.bulk_write(records, ordered=False)
            # records = data.to_dict(orient="records")
            # collection.insert_many(records)
            print(f"Inserted {len(records)} records from '{name}'.\n\t--> cols: {cols}\n")

        print(f"\n{'='*60}\n--- DB CHECK AFTER DATA LOAD ---\n{'='*60}")
        count = collection.count_documents({})
        print(f"\nNumber of entries:\t{count}") #, collection.count_documents({}))

        if count > 0:
            print("\nExemple document:")
            doc = collection.find_one()
            for key, value in doc.items():
                print(f"{key}:\t{value}")
        else:
            print("\nNo entries found in the collection.")
    
    else: 
        print("Function probably not yet suitable for that input. Please check.")
        # return None 


if __name__ == "__main__":
    main()
