#imports 
import importlib

import utils.ETL_preprocess_helper as eph 
import utils.setup_helper as sh 
import utils.database_helper as dbh 
from utils.settings import session

importlib.reload(sh)
importlib.reload(dbh)

def text_embed(coll_name=None, cols_needed=None):
    """
    ETL pipeline for text embeddings of product data.

    Steps:
    1. Load environment variables and paths.
    2. Load product data from MongoDB.
    3. Prepare text for embedding (cleaning, combining columns, etc.).
    4. Generate embeddings.
    5. Upload embeddings back to MongoDB.
    """
    #Load environment variables & paths
    sh.load_env_vars()

    sh.get_paths()
    DATA = session.data

    DATA_PROCESSED = DATA / "processed"
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    DATA_LAKE = DATA / "data_lake"
    DATA_LAKE.mkdir(parents=True, exist_ok=True)

    #Default parameters
    if not coll_name:   
        coll_name = "products"
    
    if not cols_needed:
       cols_needed = ["clean_designation", "clean_description",
                      "productid"]

    # Load product data from MongoDB
    df = dbh.load_cursor2(coll_name, cols_needed)
    if df is None:
        return None
    
    # Prepare text for embedding
    df_prep = eph.prepare_embed(df)

    # Generate embeddings
    df_emb = eph.embed_text(df_prep)
    print(df_emb.columns)
    print(df_emb.head())

    # Upload embeddings to MongoDB
    dbh.upload_embeds(df_emb, coll_name)

if __name__ == "__main__":
    text_embed()
