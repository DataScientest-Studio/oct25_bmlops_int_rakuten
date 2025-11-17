##
# imports 
import pandas as pd
import numpy as np
import os
from datetime import datetime   
from pymongo import UpdateOne

from utils.ETL_preprocess_helper import clean_text, check_chars, check_products
from utils.setup_helper import setup_mongodb, load_env_vars

# paths
ROOT, DATA, VENV, _ = load_env_vars()

DATA_LAKE = DATA / "data_lake"
DATA_LAKE.mkdir(parents=True, exist_ok=True)

DATA_PROCESSED = DATA / "data_processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

## data preview
f_names = ["X_test_update", "X_train_update", "Y_train_CVw08PX"]

now_etl = datetime.now()
df_dict = {}
for f in f_names:
    f_path = os.path.join(DATA_LAKE, f"{f}.csv")
    df = pd.read_csv(f_path)
    df = df.rename(columns={"Unnamed: 0": "id"}) 
    df["timestamp"] = now_etl if "timestamp" not in df.columns else df["timestamp"]
    df_dict[f] = df
    print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
    print("SHAPE:\t", df.shape)
    print("INFO\n", df.info())
    print(f"HEAD:\n{df.head(5)}\n")

    try:
        df.to_csv("DATA_LAKE/{f}.csv", index=False)
    except Exception as e:
        print(f"⚠️ ERROR -- SAVING DF '{f}': {e}")
    
# check if futher ETL + preprocessing is needed
db, collection = setup_mongodb()

df_dict = check_products(df_dict, collection)

## cleaning data (using RegEx + BeautifulSoup)
text_col = ["description", "designation"]

df_to_merge = {}
for name, df in df_dict.items():
    df_clean = df.copy()

    print(f"{'='*45}\n📘 TEXT CLEANING '{name}'\n{'='*45}")
    for col in text_col:
        if col not in df_clean.columns:
            print(f"⚠️  Column '{col}' not found in {name}, skipping.")
            continue

        df_clean[f"is_valid_{col}"] = df_clean[col].apply(check_chars)
        invalid_pre = df_clean.loc[~df_clean[f"is_valid_{col}"], col]

        print(f"🔍 BEFORE Cleaning ('{name}' / '{col}'):\t{len(invalid_pre)} invalid entries ({len(invalid_pre)/len(df_clean):.2%})")
        if len(invalid_pre) > 0:
            exemple = invalid_pre.iloc[0]
            print("-->  Example:", exemple[:120] if isinstance(exemple, str) else exemple)

        print(f"🧽 START Cleaning ('{name}' / '{col}')")
        df_clean[f"clean_{col}"] = df_clean[col].apply(clean_text)

        df_clean[f"is_valid_2_{col}"] = df_clean[f"clean_{col}"].apply(check_chars)
        invalid_post = df_clean.loc[~df_clean[f"is_valid_2_{col}"], col]
        print(f"✅ AFTER Cleaning ('{name}' / '{col}':\t{len(invalid_post)} invalid entries ({len(invalid_post)/len(df_clean):.2%})")
        if len(invalid_post) > 0:
            exemple_2 = invalid_post.iloc[0]
            print("-->  Example:", exemple[:120] if isinstance(exemple_2, str) else exemple_2)

    df_to_merge[f'{name}'] = df_clean # print()

    # QUO VADIS?
    # saving cleaned data frames
    # try:
    #     df_clean.to_csv(f"{DATA_PROCESSED}/{name}_clean.csv")
    #     print(f"✅ SAVED DF '{name}_clean' successfully")
    # except Exception as e:
    #     print(f"⚠️ ERROR -- DF '{name}_clean': {e}")

## merge data frames
df_names = ["df_train", "df_test"]

df_train = pd.merge(df_to_merge["X_train_update"], 
                    df_to_merge["Y_train_CVw08PX"], 
                    on='id',
                    how='outer')

df_test = df_to_merge["X_test_update"].copy()
df_test['prdtypecode'] = np.nan

# QUO VAIDS?
# # saving merged data frames
# for name, df in zip(["df_train", "df_test"], [df_train, df_test]):
    # try:
    #    df.to_csv(f"{DATA_PROCESSED}/{name}.csv", index=False)
    #    print(f"✅ SAVED DF '{df}' successfully")
    # except Exception as e:
    #    print(f"⚠️ ERROR -- DF '{name}_clean': {e}")

for name, df in zip(df_names,
                    [df_train, df_test]): 
    print(f"\n{'='*30}\n--- CHECK MERGED DF ('{name}') ---") 
    print("SHAPE:\t", df.shape)
    print("INFO:\n", df.info())
    print(f"HEAD:\n{df.head(5)}\n")


# loading data into MongoDB
now_db = datetime.now()

allowed_cols = ['id', 'prdtypecode', 
                'designation', 'clean_designation',
                'description', 'clean_description',
                'productid', 'imageid']


for name, df in zip(df_names, 
                    [df_train, df_test]):
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

    collection.bulk_write(records)
    # records = data.to_dict(orient="records")
    # collection.insert_many(records)
    print(f"Inserted {len(records)} records from '{name}'.\n\t--> cols: {cols}\n")

print(f"\n{'='*60}\n--- DB CHECK AFTER DATA LOAD ---\n{'='*60}")
count = collection.count_documents({})
print(f"\nNumber of entries:\t{count}") #, collection.count_documents({}))

if count > 0:
    print(f"\nExemple document:")
    doc = collection.find_one()
    for key, value in doc.items():
        print(f"{key}:\t{value}")
else:
    print("\nNo entries found in the collection.")
