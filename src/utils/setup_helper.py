##
# imports
# from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
import argparse
# from datetime import datetime
# import subprocess
import sys
from utils.settings import session


def load_args():
    """
    Load variables passed as input from shell command. 
    """
    # detect jupyter
    if "ipykernel" in sys.modules:
        print("[INFO] Jupyter detected — skipping argparse.")
        class DummyArgs:
            env = "core"
            n_neighbors = 5
            query_pid = None
            msg = ""

        args = DummyArgs()

    else:    
        # define parsed arguments
        parser = argparse.ArgumentParser()
        # parser.add_argument("--env", choices=["core", "heavy_+", "dev_+", "all"], default="core")
        # parser.add_argument("--branch", type=str, default="phase_1_es")
        parser.add_argument("--db", choices=["mongo_db"], default="mongo_db")
        parser.add_argument("--preview", type=bool, default=True)
        parser.add_argument("--neigh", type=int, default=5)
        parser.add_argument("--qpid", type=int, default=None)
        parser.add_argument("--msg", "-m", choices=["", "auto", "tmp"], 
                            default="auto")
                            # help="Commit message for git push",
                            # default=f"Auto-commit: Several minor improvements, no major change ({datetime.now().isoformat(timespec='seconds')}" )
        
        args, unknown = parser.parse_known_args()

        if unknown:
            print(f"[INFO] Ignoring unknown CLI arguments: {unknown}")
    
    return args


def load_env_vars():
    """
    Load environment variables from a .env file if available.
    """
    env_path = find_dotenv()
    session_path = find_dotenv(filename=".env.session")

    if env_path:
        load_dotenv(env_path)
        print("Variable from .env loaded")
    
    if session_path:
        load_dotenv(session_path)
        print("Variable from .env.session loaded")
    
    # else:
    #     print("No .env file found. Please ensure environment variables are set.")

def get_paths():        
    # load environment variables
    env = session.env
    print(f"Using env: {env}")
    # print("[DEBUG] LOCAL_ROOT =", os.getenv("LOCAL_ROOT"))

    if env == "heavy":
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
    
    session.root = ROOT
    session.data = DATA
    session.venv = VENV
    session.save_session()

    print("Paths loaded")
    # return ROOT, DATA, VENV



    # # load environment variables
    # if args.env == "colab":
    #     # mount with GoogleDrive
    #     try:
    #         from google.colab import drive
    #         drive.mount('/content/drive')

    #     except ImportError:
    #         # !uv add google.colab
    #         # from google.colab import drive
    #         raise RuntimeError("Colab environment required for --env colab")

    #     ROOT = Path(os.getenv("COLAB_ROOT"))
    #     DATA = Path(os.getenv("COLAB_DATA"))
    #     VENV = Path(os.getenv("COLAB_VENV"))

    # else:
    #     ROOT = Path(os.getenv("LOCAL_ROOT")).resolve()
    #     DATA = Path(os.getenv("LOCAL_DATA"))
    #     VENV = Path(os.getenv("LOCAL_VENV"))
    
    # return ROOT, DATA, VENV, args


def setup_mongodb(db_name: str = None, 
                  collection_name: str = None, 
                  mongo_uri: str = None,
                  verbose=False):
    """
    Connect to MongoDB using either function arguments or environment variables.
    """
    # lazy imports
    try:
        from pymongo import MongoClient
    except ImportError:
        raise ImportError("pymongo is not installed.")

    # load .env und .env.session if available
    load_env_vars()

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

    coll_dict = {}

    if isinstance(collection_name, list):    
        for col in collection_name:
            coll_dict[col] = db[collection_name] #.create_index("productid", unique=True)
    else:
        coll_dict[collection_name] = db[collection_name] #.create_index("productid", unique=True)
        # collection
    
    if verbose:
        mongoDB_check(db, db_name, coll_dict)
    
    return db, db_name, coll_dict

def mongoDB_check(db, db_name, coll_dict):        
    print(f"{len(db.list_collection_names())} collections in database {db_name}.")

    for name, col in coll_dict.items():
        print(f"\n{'='*60}")
        print(f"--- CHECK 'MongoDB ({db_name} / {name})' ---")
        print(f"{'='*60}")
        count = col.count_documents({})
        print(f"\nNumber of entries:\t{count}") #, collection.count_documents({}))

        if count > 0:
            print(f"\nExemple document:")
            doc = col.find_one()
            for key, value in doc.items():
                print(f"{key}:\t{value}")
        else:
            print("\nNo entries found in the collection.")


def load_collection(coll_name):
    """
    Docstring for load_collection
    
    :param coll_name: Description
    """
    _, _, coll_dict = setup_mongodb()
    
    collection = None
    for key, value in coll_dict.items():
        if key == coll_name:
            collection = value
        
    if collection:
        return collection
    else:
        print(f"Collection {coll_name} could not be found.")
        return None

def shorten_path(path, n=3):
    p = Path(path).parts
    return "/".join(p[-n:])


def get_latest_training_folder(root):
    dirs = [d for d in root.iterdir() if d.is_dir()]
    if not dirs:
        print("No similarity matrix directories found.")
        return None
    return max(dirs, key=lambda d: d.name)

