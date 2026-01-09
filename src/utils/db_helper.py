## db_helper.py
# imports 
import os

import pandas as pd

import utils.setup_helper as sh


# 
def load_cursor(coll_name, cols_needed):
    
    collection = load_collection(coll_name)
    if collection is None:
        return pd.DataFrame()
    
    if not cols_needed:
        projection = {"_id": 0} 
    else:
        projection = {"_id": 0}   
        for col in cols_needed:
            projection[col] = 1

    cursor = collection.find({}, projection) 
    docs = list(cursor)

    if not docs:
        print("No documents found in MongoDB.")
        return pd.DataFrame()

    return pd.DataFrame(docs)


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
    sh.load_env_vars()

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
    print("Collections loaded:", coll_dict.keys())
    collection = None
    print(f"Looking for collection: '{coll_name}' in {list(coll_dict.keys())}")
    for key, value in coll_dict.items():
        if key == coll_name:
            collection = value
        
    if collection is None:
        print(f"Collection {coll_name} could not be found.")
        return None
    
    return collection

        
