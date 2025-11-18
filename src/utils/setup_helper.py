##

# imports
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
import argparse
from datetime import datetime
import subprocess


def load_env_vars():
    """
    Load environment variables from a .env file if available.
    Load variables passed as input from shell command. 
    """
    # define parsed arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["local", "colab"], default="local")
    parser.add_argument("--n_neighbors", type=int, default=5)
    parser.add_argument("--query_pid", type=int, default=None)
    parser.add_argument("--msg", "-m", choices=["auto", "tmp"], 
                        default="")
                        # help="Commit message for git push",
                        # default=f"Auto-commit: Several minor improvements, no major change ({datetime.now().isoformat(timespec='seconds')}" )
    args = parser.parse_args()
    
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        print("No .env file found. Please ensure environment variables are set.")

    # load environment variables
    if args.env == "colab":
        # mount with GoogleDrive
        try:
            from google.colab import drive
            drive.mount('/content/drive')

        except ImportError:
            # !uv add google.colab
            # from google.colab import drive
            raise RuntimeError("Colab environment required for --env colab")

        ROOT = Path(os.getenv("COLAB_ROOT"))
        DATA = Path(os.getenv("COLAB_DATA"))
        VENV = Path(os.getenv("COLAB_VENV"))

    else:
        ROOT = Path(os.getenv("LOCAL_ROOT")).resolve()
        DATA = Path(os.getenv("LOCAL_DATA"))
        VENV = Path(os.getenv("LOCAL_VENV"))
    
    return ROOT, DATA, VENV, args


def setup_mongodb(db_name: str = None, collection_name: str = None, mongo_uri: str = None):
    """
    Connect to MongoDB using either function arguments or environment variables.
    """
    # load .env if available
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)

    # connect to MongoDB
    if db_name is None:
        db_name = os.getenv("DB_NAME")
    
    if collection_name is None:
        collection_name = os.getenv("COLLECTION_NAME")
    
    if mongo_uri is None:
        mongo_uri = os.getenv("MONGO_URI")

    if not db_name or not collection_name or not mongo_uri:
        raise ValueError("Both arguments 'db_name', 'collection_name' and 'mongo_uri' must be provided.", 
                         "Pass them as input or environment variables.")

    # Connect to MongoDB                  
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    collection.create_index("productid", unique=True)
    
    print(f"\n{'='*60}")
    print(f"--- CHECK 'MongoDB ({db_name} / {collection_name})' ---")
    print(f"{'='*60}")
    count = collection.count_documents({})
    print(f"\nNumber of entries:\t{count}") #, collection.count_documents({}))

    if count > 0:
        print(f"\nExemple document:")
        doc = collection.find_one()
        for key, value in doc.items():
            print(f"{key}:\t{value}")
    else:
        print("\nNo entries found in the collection.")

    return db, collection


def get_latest_training_folder(root):
    dirs = [d for d in root.iterdir() if d.is_dir()]
    if not dirs:
        print("No similarity matrix directories found.")
        return None
    return max(dirs, key=lambda d: d.name)

