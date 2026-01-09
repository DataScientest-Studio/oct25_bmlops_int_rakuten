## file_helper.py
# imports
import os
from pathlib import Path
from datetime import datetime
import pickle
import shutil
import numpy as np
import pandas as pd
import zipfile
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from functools import reduce
from . import setup_helper as sh
from . import data_helper as dh



##########

def save_pickle2(obj, file_path):
    # Ordner extrahieren
    folder = os.path.dirname(file_path)

    # Ordner erstellen falls nötig
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        print(f"[SUCCESS] File saved → {file_path}")
    except Exception as e:
        print("[ERROR] Saving file as pkl:", e)


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

def merge_dfs(df_dict: dict) -> pd.DataFrame:
    """
    Merge multiple DataFrames on '_id' using outer joins.
    Overlapping columns are coalesced (first non-null wins).

    Expected:
    - Each DF has column '_id'
    """

    if not df_dict:
        raise ValueError("merge_dfs received empty df_dict")

    dfs = list(df_dict.values())

    # -------------------------------
    # Guard: _id must exist
    # -------------------------------
    for i, df in enumerate(dfs):
        if "_id" not in df.columns:
            raise ValueError(
                f"DataFrame #{i} missing required '_id' column. "
                f"Columns: {list(df.columns)}"
            )

    # -------------------------------
    # Merge step-by-step
    # -------------------------------
    df_merged = dfs[0].copy()

    for i, df in enumerate(dfs[1:], start=1):
        print(
            f"[DEBUG] Merging DF {i}/{len(dfs)-1} "
            f"(rows={len(df)}) at {datetime.utcnow()}"
        )

        df_merged = df_merged.merge(
            df,
            on="_id",
            how="outer",
            suffixes=("", "_dup"),
        )

        # -------------------------------
        # Coalesce duplicate columns
        # -------------------------------
        dup_cols = [c for c in df_merged.columns if c.endswith("_dup")]

        for dup in dup_cols:
            base = dup.replace("_dup", "")
            if base in df_merged.columns:
                df_merged[base] = df_merged[base].combine_first(
                    df_merged[dup]
                )
                df_merged.drop(columns=[dup], inplace=True)

    # -------------------------------
    # Final sanity checks
    # -------------------------------
    required_cols = ["_id", "productid"]

    missing = [c for c in required_cols if c not in df_merged.columns]
    if missing:
        raise ValueError(
            f"Final merged DF missing required columns: {missing}. "
            f"Columns present: {list(df_merged.columns)}"
        )

    print("==================================================")
    print(f"[DEBUG] FINAL MERGED DF @ {datetime.utcnow()}")
    print("SHAPE:\t", df_merged.shape)
    print("COLUMNS:\t", list(df_merged.columns))
    print("==================================================")

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
    # für Python 3.10+
    # files: list[Path] | None = None
    # folders: list[Path] | None = None

    # für Python <3.10
    files: Optional[List[Path]] = None
    folders: Optional[List[Path]] = None


def unzip_images(f_names, extract_dir):
    # zip_file = Path(src_folder) / "images.zip"
    
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

    # else:
    #     print(f"No files unzipped. Folder 'extract_dir' already contains {len(img_files)} files and {img_folders} folders .")
    #     return None, None 


def list_files_and_folders(path):
    files = [f for f in path.iterdir() if f.is_file()]
    folders = [f for f in path.iterdir() if f.is_dir()]

    return files, folders