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

    from utils.settings import session
    from utils.setup_helper import load_env_vars, get_paths
    from utils.db_helper import setup_mongodb

    # ------------------------------------------------------------------
    # Paths / Env
    # ------------------------------------------------------------------
    ROOT = Path(os.getenv("LOCAL_ROOT"))
    DATA = Path(os.getenv("LOCAL_DATA"))

    IMAGES = DATA / "data_lake" / "unzipped_images" / "images"
    DATA_PROCESSED = DATA / "data_processed"
    DATA_LAKE = DATA / "data_lake"
    DATA_DONE = DATA / "data_done"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    metadata_df_train = pd.read_csv(DATA_LAKE / "metadata_train.csv")
    metadata_df_test = pd.read_csv(DATA_LAKE / "metadata_test.csv")

    img_paths_train = [DATA_LAKE / p for p in metadata_df_train["path"].values]
    img_paths_test = [DATA_LAKE / p for p in metadata_df_test["path"].values]

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
                    p = str(p).replace("\\", "/")
                    img = Image.open(p).convert("RGB")
                    images.append(img)
                except Exception as e:
                    print(f"Fehler bei {p}: {e}")
                    images.append(None)

            # Filter out None images
            valid_idx = [i for i, img in enumerate(images) if img is not None]
            if not valid_idx:
                embeddings.extend([None] * len(batch_paths))
                continue

            valid_images = [images[i] for i in valid_idx]
            inputs = processor(images=valid_images, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                batch_emb = model.get_image_features(**inputs).cpu().numpy()

            # L2-Normalize embeddings
            batch_emb = batch_emb / np.linalg.norm(batch_emb, axis=1, keepdims=True)

            emb_iter = iter(batch_emb)
            for img in images:
                embeddings.append(next(emb_iter) if img is not None else None)

        return embeddings

    # ------------------------------------------------------------------
    # Train embeddings
    # ------------------------------------------------------------------
    embeddings_train = get_embeddings(img_paths_train)

    valid_idx_train = [i for i, e in enumerate(embeddings_train) if e is not None]
    df_emb_train = metadata_df_train.iloc[valid_idx_train].copy()
    df_emb_train["embedding"] = [embeddings_train[i] for i in valid_idx_train]

    df_emb_train["embedding_img"] = df_emb_train["embedding"].apply(
        lambda x: ",".join(map(str, x))
    )

    df_emb_train.to_csv(DATA_PROCESSED / "df_train_with_embeddings.csv", index=False)
    print("df_train_with_embeddings.csv saved.")

    # ------------------------------------------------------------------
    # Test embeddings
    # ------------------------------------------------------------------
    embeddings_test = get_embeddings(img_paths_test)

    valid_idx_test = [i for i, e in enumerate(embeddings_test) if e is not None]
    df_emb_test = metadata_df_test.iloc[valid_idx_test].copy()
    df_emb_test["embedding"] = [embeddings_test[i] for i in valid_idx_test]

    df_emb_test["embedding_img"] = df_emb_test["embedding"].apply(
        lambda x: ",".join(map(str, x))
    )

    df_emb_test.to_csv(DATA_PROCESSED / "df_test_with_embeddings.csv", index=False)
    print("df_test_with_embeddings.csv saved.")

    # ------------------------------------------------------------------
    # MongoDB Upload
    # ------------------------------------------------------------------
    db, db_name, coll_dict = setup_mongodb()
    collection = coll_dict["products"]

    upload_embeddings(df_emb_train, collection)
    upload_embeddings(df_emb_test, collection)

    print("Total documents:", collection.count_documents({}))
    pprint(collection.find_one())


def upload_embeddings(df, collection, embedding_col="embedding_img"):
    records = df[["productid", embedding_col]].to_dict(orient="records")
    ops = []

    for r in records:
        ops.append(UpdateOne(
            {"productid": str(r["productid"])},
            {"$set": {embedding_col: r[embedding_col]},
             "$currentDate": {"lastModified": True}},
            upsert=False
        ))

    if ops:
        res = collection.bulk_write(ops)
        print(f"Updated documents: {res.modified_count}")