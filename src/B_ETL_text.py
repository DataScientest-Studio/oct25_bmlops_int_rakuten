##
# imports 
# from pathlib import Path

import utils.ETL_preprocess_helper as eph 
# import utils.database_helper as dbh 
import utils.file_helper as fh 
# import utils.setup_helper as sh 
# import utils.data_helper as dh 
# from utils.settings import session
# from src.A_new_file_check import new_file_check

def text_etl(df_dict, product_dict=None):
    if not product_dict:
        print("✅ All text columns are up-to-date or ⚠️ no dict was passed as input.")
        return None
    
    text_dfs = {}
    for df_name, df in df_dict.items():
        for f_name, product_id in product_dict.items():
            if df_name == f_name:
                text_dfs[f_name] = df[df["productid"].isin(product_id)].copy()
    
    # workflow  
    cleaned_dfs = eph.data_cleaning(text_dfs)
    df_merged = fh.merge_dfs(cleaned_dfs)
    
    # if not dfs:
    #     return None

    return df_merged

                
if __name__ == "__main__":
    text_etl()
