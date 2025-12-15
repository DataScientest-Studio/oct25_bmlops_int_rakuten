##
# imports 
# from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd

import utils.ETL_preprocess_helper as eph 
import utils.database_helper as dbh 
import utils.file_helper as fh 

# import utils.setup_helper as sh 
# import utils.data_helper as dh 
# from utils.settings import session
# from src.A_new_file_check import new_file_check

def text_general_etl(f_names, src_folder, dst_folder, product_dict):
    update = product_dict["txt_update"]
    
    if not update:
        print("✅ All text columns are up-to-date or ⚠️ no dict was passed as input.")
        return None
    
    df_dict = fh.load_dfs(f_names, src_folder)
    print(f"[DEBUG]: number of dfs in df_dict: {len(df_dict.values())}")

    text_df = {}
    for df_name, df in df_dict.items():
        if update == "all":
            text_df[df_name] = df 
        else:
            for f_name, product_id in update.items():
                if df_name == f_name:
                    text_df[f_name] = df[df["productid"].isin(product_id)].copy()
        
    print(f"[DEBUG]: number of dfs in df_dict: {len(text_df.values())}")
    cols_allowed = ['Unnamed: 0', 'prdtypecode', 
                    'designation', 'clean_designation',
                    'description', 'clean_description',
                    'productid', 'imageid',
                    "upload_time (text)",
                    "upload_time (image)"
                    ]
    
    rename_dict = {"Unnamed: 0": "_id"}

    # workflow  
    cleaned_df = eph.data_cleaning(text_df)
    print(f"[DEBUG]: number of dfs in cleaned_df: {len(cleaned_df.values())}")

    renamed_df ={}
    for name, df in cleaned_df.items():
        renamed_df[name] = eph.filter_rename_columns(df, cols_allowed, rename_dict)
    
    print(f"[DEBUG]: number of dfs in renamed_df: {len(renamed_df.values())}")
    
    merged_df = fh.merge_dfs(renamed_df)

    for df_name in df_dict.keys():
        _ = fh.move_file(df_name, dst_folder, src_folder)

    dbh.upload_text_data(merged_df)
    # --> load to DB

    
    # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # merge_path = f"{dst_folder}/{now}_text_merge.csv"
    # df_merged.to_csv(merge_path)
    
    return True
    
if __name__ == "__main__":
    text_general_etl()
