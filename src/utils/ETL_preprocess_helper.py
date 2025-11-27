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

import re
import gc

import utils.setup_helper as sh
import utils.db_helper as dh
from utils.settings import session


##########################
# IMAGE FUNCTION
#########################

def extract_product_id(filename):
    match = re.search(r"product_(\d+)", filename)
    return match.group(1) if match else None


def get_mobilenet_embeddings(img_paths, batch_size=16):
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    base_model = MobileNetV2(weights="imagenet", 
                             include_top=False, 
                             pooling="avg")
    preprocess = preprocess_input
    
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
    text = "".join(ch for ch in text 
                   if allowed_pattern.match(ch) or ch.isspace())

    return text

def check_latest_products(df_dict, coll_name):
    # load MongoDB
    _, _, coll_dict = dh.setup_mongodb()
    
    collection = None
    for key, value in coll_dict.items():
        if key == coll_name:
            collection = value
    
    cols_needed = ["productid",
                   "upload_time (image)",
                   "upload_time (text)"]
    
    if collection is None:
        print(f"⚠️ No collection '{coll_name}' found in db")
        return None

    df_db = dh.load_cursor(collection, cols_needed)

    time_cols = ["upload_time (image)", "upload_time (text)"]

    for col in df_db.columns:
        if col in time_cols:
            df_db[col] = pd.to_datetime(df_db[col], errors='coerce')

    to_update = {}
    for name, df in df_dict.items():
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
        df["now"] = pd.to_datetime(df["now"], errors='coerce')

        old_image = []
        old_text = []
        if "upload_time (image)" in df.columns:
            old_image = df_db[df_db["upload_time (image))"] < cutoff]["productid"].tolist()    
        if "upload_time (text)" in df.columns:
            old_text = df_db[df_db["upload_time (text))"] < cutoff]["productid"].tolist()    

        # outdated_image = df[df["upload_time (image))"] < df_db["upload_time (image))"]]["productid"].tolist()    
        # outdated_text = df[df["upload_time (text))"] < df_db["upload_time (text)"]]["productid"].tolist()    
        
        need_update = set(old_image + old_text 
                          # + outdated_image + outdated_text
                          )
        if need_update:
            to_update[name] = list(need_update) 
            print(f"Updates needed for '{name}': {len(need_update)} products.")
        else:
            print(f"No updates needed for '{name}'.")

    need_update = {}
    for name, products in to_update.items():
        df = df_dict[f"{name}"]
        df_reduced = df[df["productid"].isin(products)]
        need_update[f"{name}"] = df_reduced 

    return need_update

