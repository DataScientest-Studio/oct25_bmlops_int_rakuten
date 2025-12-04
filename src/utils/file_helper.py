## file_helper.py
# imports
import os
from pathlib import Path
from datetime import datetime
import pickle
import shutil

import pandas as pd



##########


def save_pickle(file, path, folder=None):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
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


def read_csv(file_path):

    f_path = Path(file_path)
    pd.read_csv("file_path")



def move_file(file: Path, target_folder: Path):
    target_folder.mkdir(parents=True, exist_ok=True)
    new_path = target_folder / file.name
    shutil.move(str(file), str(new_path))
    return new_path



def df_preview(path, f_names=None):
    """
    Docstring for data_preview
    
    :param lake: Description
    :param f_names: Description
    """
    ## data preview
    if not f_names:
        f_names = ["X_test_update", "X_train_update", "Y_train_CVw08PX"]

    now_etl = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_dict = {}
    for f in f_names:
        f_path = os.path.join(path, f"{f}.csv")
        try:
            df = pd.read_csv(f_path)
            df = df.rename(columns={"Unnamed: 0": "id"}) 
            df["now"] = now_etl 
            df_dict[f] = df
            sh.log_header("EDA RAW DATA")
            # print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")

        except Exception as e:
            print(f"⚠️ Loading {f}: Error occured:\n{e}")

    return df_dict if len(df_dict) > 0 else None


def merge_dfs(dfs, names=None):
    """
    Docstring for merge_dfs
    
    :param dfs: Description
    :param names: Description
    """
    ## merge data frames
    if not names:
        names = ["df_train", "df_test"]

        df_train = pd.merge(dfs["X_train_update"], 
                            dfs["Y_train_CVw08PX"], 
                            on='id',
                            how='outer')

        df_test = dfs["X_test_update"].copy()
        df_test['prdtypecode'] = np.nan

        for name, df in zip(names,
                        [df_train, df_test]): 
            sh.log_header(f"CHECK MERGED DF ('{name}')")
            # print(f"\n{'='*30}\n--- CHECK MERGED DF ('{name}') ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")
        
        return [df_train, df_test]

    else: 
        print("Function probably not yet suitable for that input. Please check.")
        return None 

