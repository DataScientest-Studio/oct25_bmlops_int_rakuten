##
# imports 
# from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import ast
from pathlib import Path
import utils.ETL_preprocess_helper as eph 
import utils.database_helper as dbh 
import utils.file_helper as fh 

# import utils.setup_helper as sh 
# import utils.data_helper as dh 
# from utils.settings import session
# from src.A_new_file_check import new_file_check

def text_general_etl(f_names, src_folder, dst_folder, product_dict):
    """
    General text ETL pipeline.

    product_dict["txt_update"] can be:
    - "all"          → update everything
    - dict           → partial update {filename: [product_ids]}
    - empty / None   → nothing to do
    """

    # ------------------------------------------------------------------
    # 1. Read & validate update instruction
    # ------------------------------------------------------------------
    raw_update = product_dict.get("txt_update")

    print("[DEBUG] raw txt_update value:", raw_update)
    print("[DEBUG] raw txt_update type:", type(raw_update))

# --- Fix: deserialize if string ---
    if isinstance(raw_update, str):
        if raw_update == "all":
            update = "all"
        else:
            try:
                update = ast.literal_eval(raw_update)
            except Exception as e:
                raise ValueError(
                    f"txt_update could not be parsed from string: {raw_update}"
                ) from e
    else:
        update = raw_update

# --- Normalize Path keys ---
    if isinstance(update, dict):
        update = {
            str(Path(k)): v
            for k, v in update.items()
        }

    print("[DEBUG] parsed txt_update:", update)
    print("[DEBUG] parsed txt_update type:", type(update))

    print("[DEBUG] txt_update value:", update)
    print("[DEBUG] txt_update type:", type(update))

    if not update:
        print("✅ All text columns are up-to-date or no update required.")
        return None

    if update == "all":
        update_mode = "all"
    elif isinstance(update, dict):
        update_mode = "partial"
    else:
        raise TypeError(
            f"Unexpected type for txt_update: {type(update)} "
            f"(value={update})"
        )

    print(f"[DEBUG] update_mode resolved to: {update_mode}")

    # ------------------------------------------------------------------
    # 2. Load input DataFrames
    # ------------------------------------------------------------------
    df_dict = fh.load_dfs(f_names, src_folder)
    print(f"[DEBUG] number of dfs loaded: {len(df_dict)}")

    # ------------------------------------------------------------------
    # 3. Select rows to process
    # ------------------------------------------------------------------
    text_df = {}

    if update_mode == "all":
        # process everything
        text_df = df_dict.copy()

    elif update_mode == "partial":
        for f_name, product_ids in update.items():
            if f_name not in df_dict:
                print(f"⚠️ File '{f_name}' not found in loaded dfs → skipped.")
                continue

            df = df_dict[f_name]

            if "productid" not in df.columns:
                print(f"⚠️ File '{f_name}' has no 'productid' column → skipped.")
                continue

            text_df[f_name] = df[
                df["productid"].isin(product_ids)
            ].copy()

    print(f"[DEBUG] number of dfs after filtering: {len(text_df)}")

    if not text_df:
        print("⚠️ No text data selected for processing.")
        return None

    # ------------------------------------------------------------------
    # 4. Cleaning & feature preparation
    # ------------------------------------------------------------------
    cols_allowed = [
        "_id",
        "Unnamed: 0",
        "prdtypecode",
        "designation",
        "clean_designation",
        "description",
        "clean_description",
        "productid",
        "imageid",
        "upload_time (text)",
        "upload_time (image)",
    ]

    rename_dict = {"Unnamed: 0": "_id"}

    cleaned_df = eph.data_cleaning(text_df)
    print(f"[DEBUG] number of dfs after cleaning: {len(cleaned_df)}")

    renamed_df = {}
    for name, df in cleaned_df.items():
        renamed_df[name] = eph.filter_rename_columns(
            df, cols_allowed, rename_dict
        )

    print(f"[DEBUG] number of dfs after renaming: {len(renamed_df)}")

    # ------------------------------------------------------------------
    # 5. Merge & persist
    # ------------------------------------------------------------------
    merged_df = fh.merge_dfs(renamed_df)

    #for df_name in text_df.keys():
    #    fh.move_file(df_name, dst_folder, src_folder)

    dbh.upload_text_data(merged_df)

    print("✅ Text ETL finished successfully.")
    return True
    
if __name__ == "__main__":
    text_general_etl()

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
