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

def text_etl(f_names, src_folder, dst_folder, product_dict=None):
    update = product_dict["txt_update"]
    if not update:
        print("✅ All text columns are up-to-date or ⚠️ no dict was passed as input.")
        return None
    
    df_dict = fh.load_dfs(f_names, src_folder)

    text_df = {}
    for df_name, df in df_dict.items():
        if update == "all":
            text_df[df_name] = df 
        else:
            for f_name, product_id in update.items():
                if df_name == f_name:
                    text_df[f_name] = df[df["productid"].isin(product_id)].copy()

        _ = fh.move_file(df_name, dst_folder)
    
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
    renamed_df = eph.filter_rename_columns(cleaned_df, cols_allowed, rename_dict)
    merged_df = fh.merge_dfs(renamed_df)

    dbh.upload_text_data(merged_df)
    
    return True
    
if __name__ == "__main__":
    text_etl()

# Traceback (most recent call last):
#   File "/home/airflow/.local/lib/python3.8/site-packages/airflow/models/taskinstance.py", line 433, in _execute_task
#     result = execute_callable(context=context, **execute_callable_kwargs)
#   File "/home/airflow/.local/lib/python3.8/site-packages/airflow/decorators/base.py", line 241, in execute
#     return_value = super().execute(context)
#   File "/home/airflow/.local/lib/python3.8/site-packages/airflow/operators/python.py", line 199, in execute
#     return_value = self.execute_callable()
#   File "/home/airflow/.local/lib/python3.8/site-packages/airflow/operators/python.py", line 216, in execute_callable
#     return self.python_callable(*self.op_args, **self.op_kwargs)
#   File "/opt/airflow/dags/data_input_processing.py", line 82, in run_text_etl
#     return text_etl(f_names=files,
#   File "/opt/airflow/src/B_ETL_text.py", line 48, in text_etl
#     renamed_df = eph.filter_rename_columns(cleaned_df, cols_allowed, rename_dict)
#   File "/opt/airflow/src/utils/ETL_preprocess_helper.py", line 189, in filter_rename_columns
#     allowed = [col for col in df.columns if col in cols_allowed]
# AttributeError: 'dict' object has no attribute 'columns'
