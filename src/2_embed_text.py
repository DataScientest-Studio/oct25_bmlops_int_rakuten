##
# imports 
import pandas as pd 
from sentence_transformers import SentenceTransformer
import numpy as np
from rich.progress import Progress
from pymongo import UpdateOne

from utils.setup_helper import setup_mongodb # , load_env_vars

# paths
# ROOT, DATA, VENV = load_env_vars()

# DATA_PROCESSED = DATA / "data_processed"
# DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# DATA_LAKE = DATA / "data_lake"
# DATA_LAKE.mkdir(parents=True, exist_ok=True)

# connect to MongoDB + load data from collection
db, collection = setup_mongodb()

cursor = collection.find({}, 
                        {"_id": 0, 
                        "clean_designation": 1, 
                        "clean_description": 1,
                        "productid": 1,
                        # "source": 1
                        })
    
docs = list(cursor)
df = pd.DataFrame(docs)

if not docs:
    print(f"No documents found in MongoDB.")
    continue

# prepare df for embedding
df["text"] = (
    df["clean_designation"].fillna("").astype(str).str.strip()
    + " "
    + df["clean_description"].fillna("").astype(str).str.strip()
            ).str.strip()
        
print(f"created column 'text' from 'clean_designation' and 'clean_description'. \n")

## using SBERT for text embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
texts = df["text"].tolist()

embeddings = []
batch_size = 256

with Progress() as progress:
    task = progress.add_task(f"Start embedding with {len(texts)} texts...", total=len(texts))
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, convert_to_numpy=True, normalize_embeddings=True)
        embeddings.append(emb)
        progress.update(task, advance=len(batch))

embeddings = np.vstack(embeddings)

print(f"--> embeddings shape:\t", embeddings.shape)

df["text_embed"] = list(embeddings)

# try:
#     df.to_csv(f"{DATA_PROCESSED}/df_embedded.csv", index=False)
#     print(f"Saved embeddings to {DATA_PROCESSED}/df_text_embed.csv")
# except Exception as e:
#     print(f"Error saving 'df_text_embed': {e}")

# save embeddings back to MongoDB
records = df[["productid", "text_embed"]].to_dict(orient="records")

ops = []

for record in records:
    ops.append(UpdateOne(
        {"productid": record["productid"]},
        {"$set": {"text_embed": record["text_embed"]},
         "$currentDate": {"lastModified": True }}
    ))
    
results = collection.bulk_write(ops)      # prefer 'bulk_write' for multiple updates (> 85k records)
print("Modified count:", results.modified_count)
