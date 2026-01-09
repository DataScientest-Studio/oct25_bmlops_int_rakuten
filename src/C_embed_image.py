from pymongo import UpdateOne
from pprint import pprint
from datetime import datetime

def image_embed():
    import os
    from pathlib import Path
    import pandas as pd
    import numpy as np
    from tqdm import tqdm
    from PIL import Image
    import torch
    from transformers import CLIPProcessor, CLIPModel

    from utils.db_helper import setup_mongodb

    # ------------------------------------------------------------------
    # Paths / Env
    # ------------------------------------------------------------------
    DATA = Path(os.getenv("LOCAL_DATA"))

    DATA_DONE = DATA / "data_done"
    DATA_PROCESSED = DATA / "data_processed"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Load latest metadata_images.csv
    # ------------------------------------------------------------------
    metadata_files = list(DATA_DONE.glob("*_metadata_images.csv"))
    if not metadata_files:
        raise FileNotFoundError("No *_metadata_images.csv found in data_done")

    latest_metadata_file = max(metadata_files, key=lambda p: p.stat().st_mtime)
    print(f"Using metadata file: {latest_metadata_file}")

    metadata_df = pd.read_csv(latest_metadata_file)

    # ---- column normalization ----
    if "product_id" in metadata_df.columns:
        metadata_df.rename(columns={"product_id": "productid"}, inplace=True)

    required_cols = {"productid", "path"}
    missing = required_cols - set(metadata_df.columns)
    if missing:
        raise ValueError(f"Missing columns in metadata: {missing}")

    img_paths = metadata_df["path"].astype(str).tolist()

    # ------------------------------------------------------------------
    # CLIP Model & Processor
    # ------------------------------------------------------------------
    device = torch.device("cpu")
    model_name = "openai/clip-vit-base-patch32"

    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)

    model.eval()
    model.to(device)

    # ------------------------------------------------------------------
    # Embedding Function
    # ------------------------------------------------------------------
    def get_embeddings(image_paths, batch_size=16):
        embeddings = []

        for i in tqdm(range(0, len(image_paths), batch_size), desc="Calculate Embeddings"):
            batch_paths = image_paths[i:i + batch_size]
            images = []

            for p in batch_paths:
                try:
                    img = Image.open(p).convert("RGB")
                    images.append(img)
                except Exception as e:
                    print(f"Error loading {p}: {e}")
                    images.append(None)

            valid_idx = [i for i, img in enumerate(images) if img is not None]
            if not valid_idx:
                embeddings.extend([None] * len(batch_paths))
                continue

            valid_images = [images[i] for i in valid_idx]
            inputs = processor(images=valid_images, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                batch_emb = model.get_image_features(**inputs).cpu().numpy()

            batch_emb = batch_emb / np.linalg.norm(batch_emb, axis=1, keepdims=True)

            emb_iter = iter(batch_emb)
            for img in images:
                embeddings.append(next(emb_iter) if img is not None else None)

        return embeddings

    # ------------------------------------------------------------------
    # Calculate embeddings
    # ------------------------------------------------------------------
    embeddings = get_embeddings(img_paths)

    valid_idx = [i for i, e in enumerate(embeddings) if e is not None]
    df_emb = metadata_df.iloc[valid_idx].copy()
    df_emb["embedding"] = [embeddings[i] for i in valid_idx]

    df_emb["embedding_img"] = df_emb["embedding"].apply(
        lambda x: ",".join(map(str, x))
    )

    out_file = DATA_PROCESSED / "df_images_with_embeddings.csv"
    df_emb.to_csv(out_file, index=False)
    print(f"{out_file.name} saved.")

    # ------------------------------------------------------------------
    # MongoDB Upload
    # ------------------------------------------------------------------
    db, db_name, coll_dict = setup_mongodb()
    collection = coll_dict["products"]

    upload_embeddings(df_emb, collection)

    print("Total documents:", collection.count_documents({}))
    pprint(collection.find_one())

def upload_embeddings(df, collection, embedding_col="embedding_img"):
    records = df[["productid", embedding_col]].to_dict(orient="records")
    ops = []

    for r in records:
        ops.append(UpdateOne(
            {"productid": float(r["productid"])},
            {"$set": {embedding_col: r[embedding_col]},
             "$currentDate": {"lastModified": True}},
            upsert=False
        ))

    if ops:
        res = collection.bulk_write(ops)
        print(f"Updated documents: {res.modified_count}")