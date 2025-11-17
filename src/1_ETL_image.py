##
# imports 
import zipfile
from pathlib import Path
from PIL import Image
import pandas as pd
import re
import os
from datetime import datetime
from pymongo import UpdateOne

from utils.ETL_preprocess_helper import extract_product_id, check_products
from utils.setup_helper import setup_mongodb, load_env_vars

# paths
ROOT, DATA, VENV, _ = load_env_vars()       

TEST_IMAGES = DATA / "unzipped_images" / "images" / "image_test"
TEST_IMAGES.mkdir(parents=True, exist_ok=True)

# TRAIN_IMAGES = DATA / "unzipped_images" / "images" / "image_train"
# TRAIN_IMAGES.mkdir(parents=True, exist_ok=True)

# DATA_LAKE = DATA / "data_lake"
# DATA_LAKE.mkdir(parents=True, exist_ok=True)
# 
# DATA_PROCESSED = DATA / "data_processed"
# DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

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

# extract product ID from the filename
records = []

for img_file in TEST_IMAGES.glob("*.jpg"):
    try:
        # Open the image to get width and height
        with Image.open(img_file) as img:
            width, height = img.size

        # Extract product ID directly from the filename
        product_id = extract_product_id(img_file.name)

        if not product_id:
            print(f"️ No product ID found for {img_file.name}")
            continue

        # Append image info to the records list
        records.append({
            "product_id": product_id,
            "path": str(img_file.relative_to(DATA)),
            "width": width,
            "height": height
        })

    except Exception as e:
        print(f" Error processing {img_file.name}: {e}")

df_test = pd.DataFrame(records)

# Path for the output CSV
output_csv = TEST_IMAGES / "metadata.csv"

# # Save the records to CSV
# pd.DataFrame(records).to_csv(output_csv, index=False)

# EXTRACTING METADATA FOR TRAIN IMAGES 

# loading data into MongoDB
db, collection = setup_mongodb()

now_db = datetime.now()

for name, df in [
                # ("df_train", df_train), 
                ("df_test", df_test)
                 ]:
    # df = pd.read_csv(f"{DATA_PROCESSED}/{f}_clean.csv", index_col=0)
    # cols = [col for col in allowed_cols if col in df.columns]
    
    data = df.copy()
    data["source"] = name
    data["upload_time (images)"] = now_db

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
