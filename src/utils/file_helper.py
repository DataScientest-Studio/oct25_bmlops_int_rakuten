## file_helper.py
# imports
import os
from pathlib import Path
import pickle
import shutil
from dataclasses import dataclass
from typing import List, Optional
import zipfile
from enum import Enum

import pandas as pd

from . import setup_helper as sh
from . import data_helper as dh

##########
def move_file(file: Path, target_folder: Path, source_folder: Path=None):
    file = Path(file)

    if file.is_absolute():
        src = file

    elif source_folder:
        src = Path(source_folder) / file

    else:
        raise FileNotFoundError(
            f"Relative filename '{file}' received but no source_folder was provided. "
            "Provide source_folder OR pass absolute paths."
        )    

    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
    
    target_folder.mkdir(parents=True, exist_ok=True)
    dst = Path(target_folder) / src.name

    if dst.exists():
        dst.unlink()

    shutil.move(str(src), str(dst))
    return dst


class ExtractStatus(Enum):
    DONE = "done"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class ExtractResult:
    status: ExtractStatus
    # if Python: 3.10+
    # files: list[Path] | None = None
    # folders: list[Path] | None = None

    # if Python: <3.10
    files: Optional[List[Path]] = None
    folders: Optional[List[Path]] = None


def unzip_images(f_names, extract_dir):
    
    img_files, img_folders = list_files_and_folders(extract_dir)
    
    if img_files or img_folders:
        print(f"No files unzipped. Folder 'extract_dir' already contains {len(img_files)} files and {img_folders} folders .")        
        return ExtractResult(status=ExtractStatus.SKIPPED) 
    
    for zip_file in f_names:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        print(f"Unzipped file: {zip_file} to {extract_dir}")

    files_unzipped, folders_unzipped = list_files_and_folders(extract_dir)

    print(f"Unzipped {len(files_unzipped)} files and {folders_unzipped} folders to:", extract_dir)
    
    return ExtractResult(
            status=ExtractStatus.DONE,
            files=files_unzipped,
            folders=folders_unzipped
                    )   



def list_files_and_folders(path):
    files = [f for f in path.iterdir() if f.is_file()]
    folders = [f for f in path.iterdir() if f.is_dir()]

    return files, folders

def save_pickle(file, path, folder=None):

    if not folder:
        file_path = Path(f"{path}.pkl")

    else:
        file_path = Path(f"{folder}/{path}.pkl")

    try:
        # save as pickle
        with open(file_path, "wb") as f:
            pickle.dump(file, f)
        
        print("[SUCCESS] File saved")
    except Exception as e:
        print("[ERROR] Saving file as pkl.", e)


def save_pickle2(obj, file_path):
    folder = os.path.dirname(file_path)

    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        print(f"[SUCCESS] File saved → {file_path}")
    except Exception as e:
        print("[ERROR] Saving file as pkl:", e)


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

def merge_dfs2(dict_df: dict):
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
                                        on='Unnamed: 0',
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

    df_dict = load_dfs(f_names, folder)

    if len(df_dict) == 0:
        return None 
    
    else:
        for name, df in df_dict.items():
            sh.log_header(f"EDA RAW DATA ({Path(name).name})")
            # print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
            print("SHAPE:\t", df.shape)
            print("INFO\n", sh.info_as_string(df))
            print(f"HEAD:\n{df.head(5)}\n")

        return df_dict

def load_dfs(f_names, folder=None):
    df_dict = {}
    
    if isinstance(f_names, (str, Path)):
        f_names = [f_names]
        
    for f in f_names:
        name = Path(f).name

        if folder:
            f_path = Path(folder) / name
        else:
            f_path = name

        print(f"[DEBUG] trying to load: {f_path}\n f={f}; folder={folder}")

        try:  
            df = pd.read_csv(f_path)            
            df_dict[f_path] = df
            
        except Exception as e:
            print(f"⚠️ Loading df '{name}' from {f_path}: Error occured:\n{e}")
        
    return df_dict





    