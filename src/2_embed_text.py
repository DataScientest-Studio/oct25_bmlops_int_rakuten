##
# imports 
import importlib
import os
import pandas as pd 
import numpy as np
from rich.progress import Progress
from pymongo import UpdateOne
from datetime import datetime  

import utils.setup_helper as sh 
import utils.db_helper as dh 
from utils.settings import session

importlib.reload(sh)
importlib.reload(dh)


def main():
    # load env variables from .env and .env.session
    sh.load_env_vars()

    # load paths
    sh.get_paths()
    DATA = session.data

    DATA_PROCESSED = DATA / "processed"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    DATA_LAKE = DATA / "data_lake"
    DATA_LAKE.mkdir(parents=True, exist_ok=True)

    # load collection from MongoDB + load data from collection
    coll_name = "products"
    cols_needed = ["clean_designation", "clean_description",
                      "productid"]

    # workflow
    df = dh.load_cursor(coll_name, cols_needed)
    if df is None:
        return None
    
    df_prep = prepare_embed(df)
    df_emb = embed_text(df_prep)
    upload_embeds(df_emb, coll_name)


def prepare_embed(df_in):
    print("Start preparing df for embeddings")
    df = df_in.copy()

    # prepare df for embedding
    df["text"] = (
        df["clean_designation"].fillna("").astype(str).str.strip()
        + " "
        + df["clean_description"].fillna("").astype(str).str.strip()
                ).str.strip()
            
    print("created column 'text' from 'clean_designation' and 'clean_description'.")
    return df


def embed_text(df_in):
    print("Start creating embeddings from 'text'")
    from sentence_transformers import SentenceTransformer
    
    # path = os.path.join(df_in, "df_test_embedded.csv")
    # df_pre = pd.read_csv(path)
    # df = df_pre.head(10).copy()
    df = df_in.copy()
    
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

    print(f"Finished creating embeddings\n--> embeddings shape:\t", embeddings.shape)

    df["text_embed"] = list(embeddings)

    return df

    
def upload_embeds(df, coll_name):
    print("Starting upload of 'text_embed'")
    records = df[["productid", "text_embed"]].to_dict(orient="records")
    ops = []

    now_emb = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for record in records:
        ops.append(UpdateOne(
            {"productid": int(record["productid"])},
            {"$set": {"text_embed": record['text_embed'].tolist(),
                      "upload_time (image)": now_emb},
            "$currentDate": {"lastModified": True }}
        ))
    
    collection = dh.load_collection(coll_name)
    results = collection.bulk_write(ops, ordered=False)      # prefer 'bulk_write' for multiple updates (> 85k records)
    print("Finished upload of 'text_embed'")
    print(f"Modified count:\t{results.modified_count} entries")
    doc = collection.find_one()
    for key, value in doc.items():
        print(f"{key}:\t{value}")


if __name__ == "__main__":
    main()
