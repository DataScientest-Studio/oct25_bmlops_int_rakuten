## file_helper.py
# imports
import os
from pathlib import Path
from datetime import datetime
import pickle
import shutil
import numpy as np
import pandas as pd

from . import setup_helper as sh
from . import data_helper as dh

##########
def move_file(file: Path, target_folder: Path):
    src = Path(file)

    target_folder.mkdir(parents=True, exist_ok=True)

    dst = Path(target_folder) / src.name
    if dst.exists():
        dst.unlink()

    shutil.move(str(file), str(dst))
    return dst


def save_pickle(file, path, folder=None):
    # now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not folder:
        file_path = os.path.join([path, ".pkl"])

    else:
        file_path = os.path.join([folder, path, ".pkl"])

    try:
        # save as pickle
        with open(file_path, "wb") as f:
            pickle.dump(file, f)
        
        print("[SUCCESS] File saved")
    except:
        print("[ERROR] Saving file as pkl.")


def merge_dfs(dict_df: dict):
    """
    Docstring for merge_dfs
    
    :param dict_df: Description
    """
    ## merge data frames
    dfs = list(dict_df.values()) 
    
    df_merged = dfs[0]
    if len(dfs) > 1:
        for df in dfs[1:]:
            df_merged = df_merged.merge(df, 
                                        on='productid',
                                        how='outer')

    sh.log_header(f"CHECK MERGED DF")
    print("SHAPE:\t", df_merged.shape)
    print("INFO\n", sh.info_as_string(df_merged))
    print(f"HEAD:\n{df_merged.head(5)}\n")

    return df_merged
    

def column_check(df, cols=None):
    if not cols:
        cols = ["designation",
                "description",
                "productid",
                "imageid"]
    
    existing = [c for c in cols if c in df.columns]
    missing = [c for c in cols if c not in df.columns]
    
    print(f"[INFO] Missing columns: {missing or None}")

    return df[existing].copy 

def data_preview(f_names=None, folder=None):
    """
    Docstring for data_preview
    
    :param folder: Description
    :param f_names: Description
    """
    ## data preview
    if not f_names:
        f_names = ["X_test_update", "X_train_update", "Y_train_CVw08PX"]

    if not folder:
        print("No folder path provided")

    df_dict = {}
    for f in f_names:
        f_path = os.path.join(folder, f"{f}.csv")
        try:
            df = pd.read_csv(f_path)
            df_checked = column_check(df)
 
            # df = df.rename(columns={"Unnamed: 0": "id"}) 
            # df["now"] = now_etl 
            df_dict[f] = df_checked
            sh.log_header("EDA RAW DATA")
            # print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")

        except Exception as e:
            print(f"⚠️ Loading {f} from {f_path}: Error occured:\n{e}")

    return df_dict if len(df_dict) > 0 else None