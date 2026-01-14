## imports 
import ast
from pathlib import Path
import utils.ETL_preprocess_helper as eph 
import utils.database_helper as dbh 
import utils.file_helper as fh 


def text_general_etl(f_names, src_folder, dst_folder, product_dict):
    """
    General text ETL pipeline.

    product_dict["txt_update"] can be:
    - "all"          → update everything
    - dict           → partial update {filename: [product_ids]}
    - empty / None   → nothing to do
    """
    #Read & validate update instructions
    raw_update = product_dict.get("txt_update")

    print("[DEBUG] raw txt_update value:", raw_update)
    print("[DEBUG] raw txt_update type:", type(raw_update))

    # If update instruction is a string, try to deserialize it
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

    # Normalize dictionary keys to strings
    if isinstance(update, dict):
        update = {
            str(Path(k)): v
            for k, v in update.items()
        }

    print("[DEBUG] parsed txt_update:", update)
    print("[DEBUG] parsed txt_update type:", type(update))

    print("[DEBUG] txt_update value:", update)
    print("[DEBUG] txt_update type:", type(update))

    # If no updates required, skip processing
    if not update:
        print("All text columns are up-to-date or no update required.")
        return None

    # Determine update mode: full or partial
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

    # Load input CSVs as DataFrames
    df_dict = fh.load_dfs(f_names, src_folder)
    print(f"[DEBUG] number of dfs loaded: {len(df_dict)}")

    # Select rows to process based on update_mode
    text_df = {}

    if update_mode == "all":
        # process everything
        text_df = df_dict.copy()

    elif update_mode == "partial":
        # process only specified product_ids
        for f_name, product_ids in update.items():
            if f_name not in df_dict:
                print(f"File '{f_name}' not found in loaded dfs → skipped.")
                continue

            df = df_dict[f_name]

            if "productid" not in df.columns:
                print(f"File '{f_name}' has no 'productid' column → skipped.")
                continue

            text_df[f_name] = df[
                df["productid"].isin(product_ids)
            ].copy()

    print(f"[DEBUG] number of dfs after filtering: {len(text_df)}")

    if not text_df:
        print("No text data selected for processing.")
        return None

    # Cleaning & feature preparation
    # Allowed columns to retain
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

    # Clean data
    cleaned_df = eph.data_cleaning(text_df)
    print(f"[DEBUG] number of dfs after cleaning: {len(cleaned_df)}")

    # Filter allowed columns and rename
    renamed_df = {}
    for name, df in cleaned_df.items():
        renamed_df[name] = eph.filter_rename_columns(
            df, cols_allowed, rename_dict
        )

    print(f"[DEBUG] number of dfs after renaming: {len(renamed_df)}")

    # Merge multiple DataFrames into a single one for MongoDB upload
    merged_df = fh.merge_dfs(renamed_df)

    # Upload to MongoDB
    dbh.upload_text_data(merged_df)

    print("Text ETL finished successfully.")
    return True
    
if __name__ == "__main__":
    text_general_etl()