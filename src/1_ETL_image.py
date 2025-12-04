import zipfile
from PIL import Image
import pandas as pd
import os
from datetime import datetime
from pymongo import UpdateOne

from utils.settings import session
from utils.ETL_preprocess_helper import extract_product_id
from utils.setup_helper import load_env_vars
from src.utils.database_helper import setup_mongodb
from pathlib import Path

load_env_vars()

ROOT = Path(os.getenv("LOCAL_ROOT"))
DATA = Path(os.getenv("LOCAL_DATA"))
VENV = Path(os.getenv("LOCAL_VENV"))

############################################## Unzipp images###############################################
zip_path = DATA / "images.zip"
extract_dir = zip_path.parent / "unzipped_images"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("Unzipped to:", extract_dir)


############################################# Create raw Meta-databases for images ##############################
TEST_IMAGES = DATA / "unzipped_images" / "images" / "image_test"
TEST_IMAGES.mkdir(parents=True, exist_ok=True)

TRAIN_IMAGES = DATA / "unzipped_images" / "images" / "image_train"
TRAIN_IMAGES.mkdir(parents=True, exist_ok=True)


DATA_LAKE = DATA / "data_lake"
DATA_LAKE.mkdir(parents=True, exist_ok=True)
 
DATA_PROCESSED = DATA / "data_processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

def extract_metadata(image_dir, output_name):
    records = []
    for img_file in image_dir.glob("*.jpg"):
        try:
            with Image.open(img_file) as img:
                width, height = img.size

            product_id = extract_product_id(img_file.name)
            if not product_id:
                print(f"No product ID found for {img_file.name}")
                continue

            records.append({
                "product_id": product_id,
                "path": str(img_file.relative_to(DATA)),
                "width": width,
                "height": height
            })

        except Exception as e:
            print(f"Error processing {img_file.name}: {e}")

    df = pd.DataFrame(records)
    df.to_csv(DATA_LAKE / output_name, index=False)
    return df


df_test  = extract_metadata(TEST_IMAGES,  "metadata_test.csv")
df_train = extract_metadata(TRAIN_IMAGES, "metadata_train.csv")


db, db_name, coll_dict = setup_mongodb()
collection = coll_dict["products"]
now = datetime.now()

def upload_df_to_mongo(df, source_name):
    ops = []
    for _, row in df.iterrows():
        doc = row.to_dict()
        doc["source"] = source_name
        doc["upload_time"] = now

        ops.append(
            UpdateOne(
                {"product_id": doc["product_id"], "path": doc["path"]},
                {"$set": doc},
                upsert=True
            )
        )
    
    if ops:
        collection.bulk_write(ops)
        print(f"Inserted/Updated {len(ops)} documents from {source_name}")

upload_df_to_mongo(df_train, "train")
upload_df_to_mongo(df_test,  "test")

count = collection.count_documents({})
print("Total documents:", count)

if count:
    print("\nExample document:")
    print(collection.find_one())