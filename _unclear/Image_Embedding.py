import tensorflow as tf
import os
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np
from tensorflow.keras.applications import resnet50
import re
from tqdm import tqdm

base_path = Path(r"C:\Users\User\Desktop\MLOps")

csv_path = base_path / "unzipped_images" / "images" / "image_metadata.csv"

df = pd.read_csv(csv_path)

# Load Model
base_model = resnet50.ResNet50(weights="imagenet", include_top=False, pooling="avg")
preprocess = resnet50.preprocess_input

def get_resnet_embedding(img_path):
    try:
        # Load and preprocess Image
        img = Image.open(img_path).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess(img_array)

        # calculate Embedding
        features = base_model.predict(img_array, verbose=0)
        emb = features[0]
        emb = emb / np.linalg.norm(emb)  # L2-Normalisierung
        return emb
    except Exception as e:
        print(f"Error at {img_path}: {e}")

tqdm.pandas(desc="Calculating ResNet50 Embeddings")

df2 = df.copy()
df2['embedding'] = df2['path'].progress_apply(lambda p: get_resnet_embedding(base_path / p))

df_emb = df2[df2['embedding'].notnull()].copy()
print(f"Calculated Embeddings: {len(df_emb)} / {len(df2)}")

# Embedding-Matrix
embedding_matrix = np.vstack(df_emb['embedding'].values).astype("float32")


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

#Load CSV
load_dir = base_path / "unzipped_images" / "images"

# --- 1. DataFrame ---
df_loaded = pd.read_csv(load_dir / "df_with_embeddings.csv")

# --- 2. Retransform Embedding-Strings into numpy-vectors---
df_loaded['embedding'] = df_loaded['embedding_str'].apply(
    lambda s: np.fromstring(s, sep=",") if isinstance(s, str) else None
)

# --- 3. Embedding-Matrix ---
embedding_matrix_loaded = np.load(load_dir / "embedding_matrix.npy")