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

def clean_text(text, f_names=None):
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

def check_latest_products2(df_dict, coll_name):
    # load MongoDB
    _, _, coll_dict = dh.setup_mongodb()
    
    collection = coll_dict.get(coll_name)
    if collection is None:
        print(f"⚠️ No collection '{coll_name}' found in db")
        return df_dict  # einfach alles zurückgeben

    df_db = dh.load_cursor(coll_name, ["productid","upload_time (image)","upload_time (text)"])
    for col in ["upload_time (image)","upload_time (text)"]:
        if col in df_db.columns:
            df_db[col] = pd.to_datetime(df_db[col], errors='coerce')

    # --- minimaler Eingriff: force all ---
    need_update = {}
    for name, df in df_dict.items():
        need_update[name] = df.copy()  # alles nehmen, ungefiltert
        print(f"Preparing to update all products for '{name}' ({len(df)} rows).")
    
    return need_update

def merge_duplicate_products(coll_name="products", overwrite=False):
    """
    Debug-Version: zeigt exakt, warum Dokumente nicht gemerged werden.
    """

    from pprint import pprint
    

    # Mongo Setup
    db, db_name, coll_dict = dh.setup_mongodb()
    col = coll_dict.get(coll_name)

    print("\n=== Loading documents ===")
    docs = list(col.find({}))
    print(f"Loaded: {len(docs)} documents")

    # --- ANALYZE KEYS ---
    print("\n=== Checking which product-ID keys exist ===")
    key_counts = {"productid": 0, "product_id": 0, "none": 0}

    for doc in docs:
        if "productid" in doc:
            key_counts["productid"] += 1
        elif "product_id" in doc:
            key_counts["product_id"] += 1
        else:
            key_counts["none"] += 1

    pprint(key_counts)

    # --- GROUP BY VALUE ---
    print("\n=== Checking value overlap ===")

    seen = {}
    collision_counter = 0

    for doc in docs:
        if "productid" in doc:
            pid = doc["productid"]
        elif "product_id" in doc:
            pid = doc["product_id"]
        else:
            pid = None

        if pid not in seen:
            seen[pid] = [doc]
        else:
            seen[pid].append(doc)
            collision_counter += 1

    print(f"Found {collision_counter} duplicate product IDs")

    # Show example duplicate
    for pid, lst in seen.items():
        if len(lst) > 1:
            print("\n--- Example duplicate ---")
            print(f"productid = {pid}, count = {len(lst)}")
            pprint(lst)
            break
    else:
        print("NO duplicates detected → merge cannot happen!")
        return []

    # --- PERFORM MERGE ---
    print("\n=== Performing merge ===")
    merged = {}

    for doc in docs:

        if "productid" in doc:
            pid = doc["productid"]
        elif "product_id" in doc:
            pid = doc["product_id"]
        else:
            continue

        new_doc = doc.copy()
        new_doc.pop("_id", None)

        if "product_id" in new_doc and "productid" not in new_doc:
            new_doc["productid"] = new_doc.pop("product_id")

        if pid not in merged:
            merged[pid] = new_doc
        else:
            merged[pid].update(new_doc)

    merged_docs = list(merged.values())
    print(f"After merge: {len(merged_docs)} docs")

    if overwrite:
        print("Overwriting collection...")
        col.delete_many({})
        col.insert_many(merged_docs)
        print("Write complete.")

    return merged_docs

