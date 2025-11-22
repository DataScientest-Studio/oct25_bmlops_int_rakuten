##
import warnings
from bs4 import MarkupResemblesLocatorWarning

# must be executed before importing or using BeautifulSoup to exclude warnings in output
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
warnings.filterwarnings("ignore", module="bs4")
warnings.filterwarnings("ignore", module="lxml")
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

from bs4 import BeautifulSoup
import html
import unicodedata
import pandas as pd
import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import re
import gc

##########################
# IMAGE FUNCTION
#########################

def extract_product_id(filename):
    match = re.search(r"product_(\d+)", filename)
    return match.group(1) if match else None

base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
preprocess = preprocess_input
def get_mobilenet_embeddings(img_paths, batch_size=16):
    embeddings = []
    n = len(img_paths)
    
    for i in range(0, n, batch_size):
        batch_paths = img_paths[i:i+batch_size]
        batch_arrays = []
        
        for path in batch_paths:
            try:
                img = Image.open(path).convert("RGB").resize((224, 224))
                img_array = np.array(img, dtype=np.float32)
                batch_arrays.append(img_array)
            except Exception as e:
                print(f"Fehler bei {path}: {e}")
        
        if not batch_arrays:
            continue
        
        batch_arrays = np.stack(batch_arrays, axis=0)
        batch_arrays = preprocess(batch_arrays)
        
        
        batch_features = base_model.predict(batch_arrays, verbose=0)
        
        
        batch_features = batch_features / np.linalg.norm(batch_features, axis=1, keepdims=True)
        
        embeddings.extend(batch_features)
        
        
        del batch_arrays
        del batch_features
        gc.collect()
    
    return embeddings
##########################
# TEXT FUNCTION
#########################

# "CLEANING" functions
allowed_pattern = re.compile(r"^[\wÀ-ÖØ-öø-ÿ0-9\s.,;:!?%€$'\"()\-–—°/&#+]+$")

def check_chars(text):
    if not isinstance(text, str) or not text.strip():
        return True
        
    return bool(allowed_pattern.match(text))

def clean_text(text):
    if not isinstance(text, str):
        return ""

    # remove HTML
    text = BeautifulSoup(text, "lxml").get_text(separator=" ")

    # decode HTML entities (&amp; -> &)
    text = html.unescape(text)

    # normalise unicode (e.g. consistent „é“)
    text = unicodedata.normalize("NFKC", text)

    # remove steering signs, multiple spaces
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    # keep only allowed chars
    text = "".join(ch for ch in text if allowed_pattern.match(ch) or ch.isspace())

    return text

def check_products(df_dict, collection):
    docs = list(collection.find({}, {"_id": 0,
                                "productid": 1,
                                "upload_time (image)": 1,
                                "upload_time (text)": 1}))
    
    if not docs:
        print("No documents found in MongoDB.")
    exit()

    df_db = pd.DataFrame(docs)
    df_db["upload_time (image)"] = pd.to_datetime(df_db["upload_time (image)"], errors='coerce')
    df_db["upload_time (text)"] = pd.to_datetime(df_db["upload_time (text)"], errors='coerce')

    to_update = {}
    for name, df in df_dict.items():
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

        old_products = df[df["timestamp"] < cutoff]["productid"].tolist()    
        updated_image = df[df["timestamp"] < df_db["upload_time (image))"]]["productid"].tolist()    
        updated_text = df[df["timestamp"] < df_db["upload_time (text)"]]["productid"].tolist()    
        
        need_update = set(old_products + updated_image + updated_text)
        if need_update:
            to_update[df] = list(need_update) 
            print(f"Updates needed for '{name}': {len(need_update)} products.")
        else:
            print(f"No updates needed for '{name}'.")

    for name, products in to_update.items():
        df = df_dict[f"{name}"]
        df_reduced = df[df["productid"].isin(products)]
        df_dict[f"{name}"] = df_reduced 

    return df_dict