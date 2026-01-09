# import zipfile
# from PIL import Image
# import pandas as pd
# import os
from datetime import datetime
# from pymongo import UpdateOne

# from utils.settings import session
# from utils.ETL_preprocess_helper import extract_product_id
# from utils.setup_helper import load_env_vars
# from utils.db_helper import setup_mongodb
# from pathlib import Path

# imports 
from pathlib import Path
import shutil
import utils.file_helper as fh
import utils.ETL_preprocess_helper as eph
import utils.database_helper as dbh 

# import utils. 
# import utils.
# import utils.
# import utils.setup_helper as sh 
# import utils.data_helper as dh 
# from utils.settings import session 

def image_etl_alt(img_path, dst_folder, product_dict=None):
    print("[DEBUG] img_path:", img_path)
    print("[DEBUG] img_update:", product_dict["img_update"])
    update = product_dict.get("img_update") if product_dict else None
    print("[DEBUG] img_update:", update)

    # 1️⃣ Kein Update vorhanden → überspringen
    if not update:
        print("✅ All image columns are up-to-date or ⚠️ no dict was passed as input.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }
        
    # defining paths + configuration
    folder = Path(img_path)
    folder.mkdir(parents=True, exist_ok=True)

    extract_dir = folder / "unzipped_images"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    dst_folder = Path(dst_folder)
    dst_folder.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # img_dfs = {}
    # for df_name, df in update.items():
    #     for f_name, product_id in product_dict.items():
    #         if df_name == f_name:
    #             img_dfs[f_name] = df[df["productid"].isin(product_id)].copy()
    
    ## workflow  
    # (1) unzip images
    #f_names = update["img_files"] if "img_files" in update else []
    #if not f_names or len(f_names) == 0:
    #    print("No image zip files to process.")
    #    return
    f_names = []
    if isinstance(update, str) and update.lower() == "all":
        f_names = list(folder.glob("*.zip"))  # alle ZIP-Dateien im img_path
    elif isinstance(update, dict):
        f_names = update.get("img_files", [])

    if not f_names:
        print("No image zip files to process.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }
    
    zip_files = [f for f in f_names if Path(f).suffix.lower() == ".zip"]
    result = fh.unzip_images(f_names=zip_files, extract_dir=extract_dir)

    if result.status is fh.ExtractStatus.SKIPPED:
        print("Skipping unzip – 'extract_dir' already contains other files and/or folders.")
        return

    # (2) extract unzipped files (e.g. metadata)
    files_unzip = result.files if result.files else []
    csv_files_unzip = [f for f in files_unzip if f.suffix.lower() == ".csv"]
    other_files_unzip = [f for f in files_unzip if f.suffix.lower() != ".csv"]

    print(f"Unzipped files: found {len(files_unzip)} files")
    print(f"\tcsv --> {len(csv_files_unzip)}")
    print(f"\tnon-csv --> {len(other_files_unzip)}")   # {len(other_files)} non-csv files.")

    folders = result.folders if result.folders else []

    metadata = {}
    other_files = {}
    if len(folders) > 0:
        folder_names = [f.name for f in folders if Path(f).is_dir()]

        for name, folder in zip(folder_names, folders):
            files = [f for f in folder.iterdir() if f.is_file()] #  result.files if result.files else []
            csv_files = [f for f in files if f.suffix.lower() == ".csv"]
            non_csv_files = [f for f in files if f.suffix.lower() != ".csv"]
            
            # print(f"Folder '{name}': found {len(files)} files (csv: {len(csv_files)};\tnon-csv: {len(other_files)})   {len(other_files)} non-csv files.")

            print(f"Folder '{name}': found {len(files)} files")
            print(f"\tcsv --> {len(csv_files)}; considered as metadata, thus saved locally")
            print(f"\tnon-csv --> {len(other_files)}") 

            save_path = dst_folder / f"{now}_metadata_{name}.csv"
            df = eph.extract_metadata(folder,  save_path)

            metadata[name] = df
            other_files[name] = non_csv_files

    if len(csv_files_unzip) > 0:
        save_path = dst_folder / f"{now}_metadata_images.csv"
        df = eph.extract_metadata(folder,  save_path)

        metadata["csv_files_unzip"] = df 

    # Metadaten-dfs noch mergen!?
    for name, df in metadata.items():
        dbh.upload_img_metadata(df, name, coll_name="products", now=now)

        result = fh.ExtractResult(
            status=fh.ExtractStatus.SKIPPED,
            files=None,
            folders=None   
                )

    if len(other_files) > 0:
        result = fh.ExtractResult(
            status=fh.ExtractStatus.DONE,
            files=other_files,
            folders=None   
                )
            
    return result




def image_etl(img_path, dst_folder, product_dict=None):
    print("[DEBUG] img_path:", img_path)
    print("[DEBUG] img_update:", product_dict.get("img_update") if product_dict else None)
    update = product_dict.get("img_update") if product_dict else None

    if not update:
        update = "all"
        print("✅ All image columns are up-to-date or ⚠️ no dict was passed as input.")

    # defining paths + configuration
    folder = Path(img_path)
    folder.mkdir(parents=True, exist_ok=True)

    extract_dir = folder / "unzipped_images"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    dst_folder = Path(dst_folder)
    dst_folder.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # workflow (1) unzip images
    #f_names = update.get("img_files", [])
    #if not f_names:
    #    f_names = list(Path(img_path).glob("*.zip"))
    print("[DEBUG] Looking in folder:", folder)
    print("[DEBUG] All files in folder:", list(folder.iterdir()))

    #f_names = []
    #if not update or update == "all":
     #   f_names = list(folder.glob("*.zip"))

    #if isinstance(update, str) and update.lower() == "all":
    #    f_names = list(folder.glob("*.zip"))  # alle ZIP-Dateien im img_path
    #elif isinstance(update, dict):
    #    f_names = update.get("img_files", [])

    f_names = []
    if isinstance(update, dict) and update.get("img_files"):
        f_names = update.get("img_files", [])

# Variante 2: fallback auf "alle ZIPs im Ordner"
    if not f_names:
        print("[DEBUG] Fallback: take all ZIPs in folder")
        f_names = list(folder.glob("*.zip"))

    print("ZIP files to unzip:", f_names)

    if not f_names:
        print("No image zip files to process.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }

    zip_files = [f for f in f_names if Path(f).suffix.lower() == ".zip"]
    result = fh.unzip_images(f_names=zip_files, extract_dir=extract_dir)

    if result.status is fh.ExtractStatus.SKIPPED:
        print("Skipping unzip – 'extract_dir' already contains other files and/or folders.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }

    # workflow (2) extract unzipped files (metadata)
    files_unzip = result.files if result.files else []
    csv_files_unzip = [f for f in files_unzip if f.suffix.lower() == ".csv"]
    other_files_unzip = [f for f in files_unzip if f.suffix.lower() != ".csv"]

    print(f"Unzipped files: found {len(files_unzip)} files")
    print(f"\tcsv --> {len(csv_files_unzip)}")
    print(f"\tnon-csv --> {len(other_files_unzip)}")

    folders = result.folders if result.folders else []

    metadata = {}
    other_files = {}
    if len(folders) > 0:
        folder_names = [f.name for f in folders if Path(f).is_dir()]

        for name, folder in zip(folder_names, folders):
            files = [f for f in folder.iterdir() if f.is_file()]
            csv_files = [f for f in files if f.suffix.lower() == ".csv"]
            non_csv_files = [f for f in files if f.suffix.lower() != ".csv"]

            print(f"Folder '{name}': found {len(files)} files")
            print(f"\tcsv --> {len(csv_files)}; considered as metadata, thus saved locally")
            print(f"\tnon-csv --> {len(non_csv_files)}")

            save_path = dst_folder / f"{now}_metadata_{name}.csv"
            df = eph.extract_metadata(folder, save_path)

            metadata[name] = df
            other_files[name] = [str(f) for f in non_csv_files]  # serialisierbar machen

    if len(csv_files_unzip) > 0:
        save_path = dst_folder / f"{now}_metadata_images.csv"
        df = eph.extract_metadata(folder, save_path)
        metadata["csv_files_unzip"] = df

    # Upload Metadaten
    for name, df in metadata.items():
        dbh.upload_img_metadata(df, name, coll_name="products", now=now)
    processed_folders = []
    if result.folders:
    # result.folders ist eine Liste von Path-Objekten
        processed_folders = [str(f) for f in result.folders]
    # Ergebnis für Airflow serialisierbar machen
    return {
        "status": result.status.value if result.status else "done",
        "processed_files": {k: [str(f) for f in v] for k, v in (result.files or {}).items()},
        "processed_folders": processed_folders
    }
   
if __name__ == "__main__":
    image_etl()
