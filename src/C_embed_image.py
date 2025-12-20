import tensorflow as tf
import os
from pathlib import Path
from PIL import Image
import pandas as pd
import re
from pathlib import Path
import numpy as np
from tqdm import tqdm
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import gc
from pprint import pprint
from utils.settings import session
from utils.setup_helper import load_env_vars, get_paths
from utils.db_helper import setup_mongodb
from utils.ETL_preprocess_helper import get_mobilenet_embeddings
from pymongo import UpdateOne
from datetime import datetime


def image_embed():
    # load env variables from .env and .env.session
    # load_env_vars()

ROOT = Path(os.getenv("LOCAL_ROOT"))
DATA = Path(os.getenv("LOCAL_DATA"))
VENV = Path(os.getenv("LOCAL_VENV"))

# ROOT, DATA, VENV, _ = load_env_vars()

IMAGES = DATA / "unzipped_images" / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

TEST_IMAGES = IMAGES / "test_image"
TEST_IMAGES.mkdir(parents=True, exist_ok=True)

TRAIN_IMAGES = IMAGES / "train_image"
TRAIN_IMAGES.mkdir(parents=True, exist_ok=True)

DATA_PROCESSED = DATA / "data_processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

DATA_LAKE = DATA / "data_lake"
DATA_LAKE.mkdir(parents=True, exist_ok=True)

metadata_path_train = DATA_LAKE / "metadata_train.csv"
metadata_df_train = pd.read_csv(metadata_path_train)

metadata_path_test = DATA_LAKE / "metadata_test.csv"
metadata_df_test = pd.read_csv(metadata_path_test)

base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
preprocess = preprocess_input

img_paths_train = [DATA / p for p in metadata_df_train['path'].values]
img_paths_test = [DATA / p for p in metadata_df_test['path'].values]

embeddings_train = []
for i in tqdm(range(0, len(img_paths_train), 16), desc="Calculate Embeddings"):
    batch_paths_train = img_paths_train[i:i+16]
    batch_embeddings_train = get_mobilenet_embeddings(batch_paths_train, batch_size=16)
    embeddings_train.extend(batch_embeddings_train)

valid_idx_train = [i for i, e in enumerate(embeddings_train) if e is not None]
df_emb_train = metadata_df_train.iloc[valid_idx_train].copy()
df_emb_train['embedding'] = [embeddings_train[i] for i in valid_idx_train]

print(f"Calculated Embeddings: {len(df_emb_train)} / {len(metadata_df_train)}")

# convert Embeddings into strings 
df_emb_train['embedding_str'] = df_emb_train['embedding'].apply(
    lambda x: ",".join(map(str, x)) if x is not None else None
)

# store DataFrame 
df_emb_train.to_csv(DATA_PROCESSED / "df_train_with_embeddings.csv", index=False)
print("df_train_with_embeddings.csv saved.")

embeddings_test = []
for i in tqdm(range(0, len(img_paths_test), 16), desc="Calculate Embeddings"):
    batch_paths_test = img_paths_test[i:i+16]
    batch_embeddings_test = get_mobilenet_embeddings(batch_paths_test, batch_size=16)
    embeddings_test.extend(batch_embeddings_test)

valid_idx_test = [i for i, e in enumerate(embeddings_test) if e is not None]
df_emb_test = metadata_df_test.iloc[valid_idx_test].copy()
df_emb_test['embedding'] = [embeddings_test[i] for i in valid_idx_test]

print(f"Calculated Embeddings: {len(df_emb_test)} / {len(metadata_df_test)}")

# convert Embeddings into strings 
df_emb_test['embedding_img'] = df_emb_test['embedding'].apply(
    lambda x: ",".join(map(str, x)) if x is not None else None
)

# store DataFrame 
df_emb_test.to_csv(DATA_PROCESSED / "df_test_with_embeddings.csv", index=False)
print("df_test_with_embeddings.csv saved.")



def upload_embeddings(df, collection, embedding_col="embedding_img"):
    """
    Upload embeddings to MongoDB.
    df: DataFrame containing at least 'product_id' and embedding_col
    collection: pymongo collection
    embedding_col: column in df to upload ('embedding_str' or 'embedding')
    """
    # Erstelle Records für MongoDB
    records = df[["productid", embedding_col]].to_dict(orient="records")

    ops = []
    now = datetime.now()

    for record in records:
        ops.append(UpdateOne(
            {"productid": str(record["productid"])},           # Match-Filter
            {"$set": {embedding_col: record[embedding_col]},
             "$currentDate": {"lastModified": True}},     # Aktualisiere lastModified
            upsert=False                                  # Falls Produkt noch nicht existiert
        ))
    
    if ops:
        results = collection.bulk_write(ops)
        print(f"Modified/Inserted count: {results.modified_count + len(results.upserted_ids)}")

db, db_name, coll_dict = setup_mongodb()
collection = coll_dict["products"]  

upload_embeddings(df_emb_train, collection, embedding_col="embedding_img")
upload_embeddings(df_emb_test, collection, embedding_col="embedding_img")

count = collection.count_documents({})
print("Total documents:", count)

if count:
    print("\nExample document:")
    pprint(collection.find_one())