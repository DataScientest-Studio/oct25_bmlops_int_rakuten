##
# imports 
from pymongo import UpdateOne
import tensorflow as tf
import os
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np
# from tensorflow.keras.applications import resnet50
import re
from tqdm import tqdm

from utils.setup_helper import setup_mongodb, load_env_vars
from utils.ETL_preprocess_helper import get_resnet_embedding

# paths
ROOT, DATA, VENV = load_env_vars()

IMAGES = DATA / "unzipped_images" / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

TEST_IMAGES = IMAGES / "test"
TEST_IMAGES.mkdir(parents=True, exist_ok=True)

# DATA_PROCESSED = DATA / "data_processed"
# DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# DATA_LAKE = DATA / "data_lake"
# DATA_LAKE.mkdir(parents=True, exist_ok=True)

# load metadata_df
metadata_path = IMAGES / "image_metadata.csv"
metadata_df = pd.read_csv(metadata_path)

# prepare df for embedding
# df["text"] = (
#     df["clean_designation"].fillna("").astype(str).str.strip()
#     + " "
#     + df["clean_description"].fillna("").astype(str).str.strip()
#             ).str.strip()
        
# print(f"created column 'text' from 'clean_designation' and 'clean_description'. \n")

# ## using ResNet50 for image embeddings
# model = SentenceTransformer('all-MiniLM-L6-v2')
# texts = df["text"].tolist()

embeddings = []
batch_size = 256

df2 = metadata_df.copy()
df2['embedding'] = df2['path'].progress_apply(lambda p: get_resnet_embedding(base_path / p))

df_emb = df2[df2['embedding'].notnull()].copy()
print(f"Calculated Embeddings: {len(df_emb)} / {len(df2)}")

# with Progress() as progress:
#     task = progress.add_task(f"Start embedding with {len(texts)} texts...", total=len(texts))
#     for i in range(0, len(texts), batch_size):
#         batch = texts[i:i+batch_size]
#         emb = model.encode(batch, convert_to_numpy=True, normalize_embeddings=True)
#         embeddings.append(emb)
#         progress.update(task, advance=len(batch))

# Embedding-Matrix
embedding_matrix = np.vstack(df_emb['embedding'].values).astype("float32")

# embedding_matrix = np.vstack(embeddings) 
# # alternative???: batch-weise arbeiten + in Liste sammeln

print(f"--> embeddings shape:\t", embedding_matrix.shape)


# connect to MongoDB + load data from collection
db, collection = setup_mongodb()

# cursor = collection.find({}, 
#                         {"_id": 0, 
#                         "productid": 1,
#                         "image_id": 1, 
#                         # "source": 1
#                         })
    
# docs = list(cursor)
# df = pd.DataFrame(docs)

# if not docs:
#     print(f"No documents found in MongoDB.")
#     continue

#Saving as CSV
save_dir = base_path / "unzipped_images" / "images"

# Store Embedding as string to ensure CSV-compatibility
df2['embedding_str'] = df2['embedding'].apply(
    lambda x: ",".join(map(str, x)) if x is not None else None
)

# Store Dataframe
df2.to_csv(save_dir / "df_with_embeddings.csv", index=False)
print("df_with_embeddings.csv stored.")

# Store Embedding-Matrix
np.save(save_dir / "embedding_matrix.npy", embedding_matrix)
print("embedding_matrix.npy stored.")

# try:
#     df.to_csv(f"{DATA_PROCESSED}/df_embedded.csv", index=False)
#     print(f"Saved embeddings to {DATA_PROCESSED}/df_text_embed.csv")
# except Exception as e:
#     print(f"Error saving 'df_text_embed': {e}")

# save embeddings back to MongoDB
records = df[["productid", "image_embed"]].to_dict(orient="records")

ops = []

for record in records:
    ops.append(UpdateOne(
        {"productid": record["productid"]},
        {"$set": {"image_embed": record["image_embed"]},
         "$currentDate": {"lastModified": True }}
    ))
    
results = collection.bulk_write(ops)      # prefer 'bulk_write' for multiple updates (> 85k records)
print("Modified count:", results.modified_count)
