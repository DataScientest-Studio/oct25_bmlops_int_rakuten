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
from rich.progress import Progress

import re
import gc

# import .setup_helper as sh
from . import database_helper as dbh
# from .settings import sessionS


##########################
# IMAGE FUNCTION
#########################

def extract_product_id(filename):
    match = re.search(r"product_(\d+)", filename)
    return match.group(1) if match else None


def get_mobilenet_embeddings(img_paths, batch_size=16):
    try: 
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    except ImportError:
        raise ImportError("tensorflow.keras.applications is not installed.")
    
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

## cleaning data (using RegEx + BeautifulSoup)
def data_cleaning(df_dict):
    text_col = ["description", "designation"]

    df_cleaned = {}
    for name, df in df_dict.items():
        df_clean = df.copy()

        print(f"{'='*45}\n📘 CHECKING AND CLEANING: '{name}'\n{'='*45}\n")
        for col in text_col:
            if col not in df_clean.columns:
                print(f"⚠️  Column '{col}' not found in {name}, skipping.\n")
                continue

            df_clean[f"is_valid_{col}"] = df_clean[col].apply(check_chars)
            invalid_pre = df_clean.loc[~df_clean[f"is_valid_{col}"], col]

            print(f"🔍 BEFORE Cleaning column '{col}' in '{name}': {len(invalid_pre)} invalid entries ({len(invalid_pre)/len(df_clean):.2%})")
            if len(invalid_pre) > 0:
                exemple = invalid_pre.iloc[0]
                print("-->  Example:", exemple[:120] if isinstance(exemple, str) else exemple)

            print(f"\n🧽 START Cleaning column '{col}' in '{name}'")
            df_clean[f"clean_{col}"] = df_clean[col].apply(clean_text)

            df_clean[f"is_valid_2_{col}"] = df_clean[f"clean_{col}"].apply(check_chars)
            invalid_post = df_clean.loc[~df_clean[f"is_valid_2_{col}"], col]
            # invalid_post = df.loc[df[f"clean_{col}"].str.contains(r"<[^>]+>|&[a-z]+;", regex=True, na=False), col]
            print(f"\n✅ AFTER Cleaning column '{col}' in '{name}': {len(invalid_post)} invalid entries ({len(invalid_post)/len(df_clean):.2%})")
            if len(invalid_post) > 0:
                exemple_2 = invalid_post.iloc[0]
                print("-->  Example:", exemple[:120] if isinstance(exemple_2, str) else exemple_2)

        df_cleaned[f'{name}'] = df_clean # print()
    
    return df_cleaned


def check_latest_products(df_dict, coll_name):
    # load MongoDB
    _, _, coll_dict = dbh.setup_mongodb()
    
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

    df_db = dbh.load_cursor(collection, cols_needed)

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

# -------------------------------
# Create embeddings from text
# -------------------------------

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
    # lazy imports
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError("sentence_transformers is not installed.")
    
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
