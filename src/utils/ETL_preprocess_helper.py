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
from tensorflow.keras.applications import resnet50
import re

##########################
# IMAGE FUNCTION
#########################

def extract_product_id(filename):
    match = re.search(r"product_(\d+)", filename)
    return match.group(1) if match else None


def get_resnet_embedding(img_path):
    # load ResNet50 (base_model)
    base_model = resnet50.ResNet50(weights="imagenet", include_top=False, pooling="avg")
    preprocess = resnet50.preprocess_input
    
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