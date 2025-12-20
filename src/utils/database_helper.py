## database_helper.py
# imports 
import os
from datetime import datetime
import pandas as pd
from pymongo import UpdateOne
from datetime import datetime 

from . import setup_helper as sh

# 
def load_cursor(coll_name, cols_needed):
    
    collection = load_collection(coll_name)
    if collection is None:
        return None
    
    projection = {"_id": 0} 

    if cols_needed:
        for col in cols_needed:
            projection[col] = 1

    cursor = collection.find({}, projection) 
    docs = list(cursor)

    if not docs or len(docs) == 0:
        print("No documents found in MongoDB.")
        return None 

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
    
    collection = None
    for key, value in coll_dict.items():
        print(f"[DEBUG]:\nkey --> {key}\nvalue --> {value}")
        if key == coll_name:
            collection = value
        
    if collection is None:
        print(f"Collection '{coll_name}' could not be found.")
        return None
    
    return collection



def upload_embeds(df, coll_name):
    print("Starting upload of 'text_embed'")
    records = df[["productid", "embed_text"]].to_dict(orient="records")
    ops = []

    now_emb = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for record in records:
        ops.append(UpdateOne(
            {"productid": record["productid"]},
            {"$set": {"text_embed": record["embed_text"],
                      "upload_time (image)": now_emb},
            "$currentDate": {"lastModified": True }}
        ))
    
    collection = load_collection(coll_name)
    results = collection.bulk_write(ops, ordered=False)      # prefer 'bulk_write' for multiple updates (> 85k records)
    print("Finished upload of 'text_embed'")
    print(f"Modified count:\t{results.modified_count} entries")



def upload_text_data(df, coll_name="products"):
    """
    Docstring for upload_data_mongoDB
    
    :param df: Description
    :param coll_name: Description
    """
    # load MongoDB collection
    collection = load_collection(coll_name)

    # loading data into MongoDB
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    allowed_cols = ['_id', 'prdtypecode', 
                    'designation', 'clean_designation',
                    'description', 'clean_description',
                    'productid', 'imageid',
                    "upload_time (text)",
                    "upload_time (image)"
                    ]

    existing = [col for col in allowed_cols if col in df.columns]
            
    data = df[existing].copy()
    data["upload_time (text)"] = now

    records = []

    for row in df.to_dict("records"):
        productid = int(row["productid"])

        records.append(UpdateOne(
                            {"productid": productid},
                            {"$set": row,
                            "$currentDate": {"lastModified": True }},
                            upsert=True
                            ))

    if records: 
        collection.bulk_write(records, ordered=False)
    
    print(f"Inserted/updated {len(records)} records .\n\t--> cols: {existing}\n")

    print(f"\n{'='*60}\n--- DB CHECK AFTER DATA LOAD ---\n{'='*60}")
    count = collection.count_documents({})
    print(f"\nNumber of entries:\t{count}") #, collection.count_documents({}))

    if count > 0:
        print("\nExemple document:")
        doc = collection.find_one()
        for key, value in doc.items():
            print(f"{key}:\t{value}")

    # if not names:
    #     names = ["df_train", "df_test"]

    #     for name, df in zip(names, 
    #                         dfs):
    #         # df = pd.read_csv(f"{DATA_PROCESSED}/{f}_clean.csv", index_col=0)
            
    #     else:
    #         print("\nNo entries found in the collection.")
    
    # else: 
    #     print("Function probably not yet suitable for that input. Please check.")
    #     # return None 
 

def upload_img_metadata(df, source_name, coll_name, now):
    ops = []
    for _, row in df.iterrows():
        doc = row.to_dict()
        doc["source"] = source_name
        doc["upload_time"] = now

        ops.append(UpdateOne(
                {"product_id": doc["product_id"], 
                 "path": doc["path"]},
                {"$set": doc,
                "$currentDate": {"lastModified": True }},
                upsert=True
                            ))

    if len(ops) == 0:
        print("No metadata to add")

    collection = load_collection(coll_name)
    
    collection.bulk_write(ops)
    print(f"Inserted/Updated {len(ops)} documents from {source_name}")
    
    count = collection.count_documents({})
    print("Total documents:", count)
    print("\nExample document:")
    print(collection.find_one())