# imports 
from datetime import datetime
from pathlib import Path
import shutil
import utils.file_helper as fh
import utils.ETL_preprocess_helper as eph
import utils.database_helper as dbh 

def image_etl(img_path, dst_folder, product_dict=None):
    """
    Main ETL function for processing image ZIPs and extracting metadata.

    Parameters:
    - img_path: Path to folder containing image ZIPs
    - dst_folder: Folder to save extracted metadata CSVs
    - product_dict: Dictionary indicating which images need updating (optional)

    Returns:
    - dict with keys:
        - 'status': processing status ("done" or "skipped")
        - 'processed_files': dict mapping folder/file category -> list of file paths
        - 'processed_folders': list of folders processed
    """

    print("[DEBUG] img_path:", img_path)
    print("[DEBUG] img_update:", product_dict.get("img_update") if product_dict else None)

    # Determine which images need to be updated
    update = product_dict.get("img_update") if product_dict else None
    if not update:
        update = "all"
        print("All image columns are up-to-date or no dict was passed as input.")

    # Ensure source folder exists
    folder = Path(img_path)
    folder.mkdir(parents=True, exist_ok=True)

    # Prepare extraction folder
    extract_dir = folder / "unzipped_images"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    # Ensure destination folder exists
    dst_folder = Path(dst_folder)
    dst_folder.mkdir(parents=True, exist_ok=True)

    # Timestamp for filenames / metadata CSVs
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[DEBUG] Looking in folder:", folder)
    print("[DEBUG] All files in folder:", list(folder.iterdir()))

    # Determine which ZIP files to process
    f_names = []
    if isinstance(update, dict) and update.get("img_files"):
        f_names = update.get("img_files", [])
    if not f_names:
        print("[DEBUG] Fallback: take all ZIPs in folder")
        f_names = list(folder.glob("*.zip"))

    print("ZIP files to unzip:", f_names)

    # If no files, skip processing
    if not f_names:
        print("No image zip files to process.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }

    # Filter only ZIP files
    zip_files = [f for f in f_names if Path(f).suffix.lower() == ".zip"]

    # Unzip image files
    result = fh.unzip_images(f_names=zip_files, extract_dir=extract_dir)
    if result.status is fh.ExtractStatus.SKIPPED:
        print("Skipping unzip – 'extract_dir' already contains other files and/or folders.")
        return {
            "status": "skipped",
            "processed_files": [],
            "processed_folders": []
        }

    # Separate CSV metadata files from non-CSV files
    files_unzip = result.files if result.files else []
    csv_files_unzip = [f for f in files_unzip if f.suffix.lower() == ".csv"]
    other_files_unzip = [f for f in files_unzip if f.suffix.lower() != ".csv"]

    print(f"Unzipped files: found {len(files_unzip)} files")
    print(f"\tcsv --> {len(csv_files_unzip)}")
    print(f"\tnon-csv --> {len(other_files_unzip)}")

    # Process subfolders if present
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

            # Extract metadata from CSV files
            save_path = dst_folder / f"{now}_metadata_{name}.csv"
            df = eph.extract_metadata(folder, save_path)

            metadata[name] = df
            other_files[name] = [str(f) for f in non_csv_files]  

    # Process CSVs directly inside extract_dir
    if len(csv_files_unzip) > 0:
        save_path = dst_folder / f"{now}_metadata_images.csv"
        df = eph.extract_metadata(folder, save_path)
        metadata["csv_files_unzip"] = df

    # Upload all extracted metadata to MongoDB
    for name, df in metadata.items():
        dbh.upload_img_metadata(df, name, coll_name="products", now=now)

    # Prepare list of processed folders
    processed_folders = []
    if result.folders:
        processed_folders = [str(f) for f in result.folders]

    # Return summary
    return {
        "status": result.status.value if result.status else "done",
        "processed_files": {k: [str(f) for f in v] for k, v in (result.files or {}).items()},
        "processed_folders": processed_folders
    }
   
if __name__ == "__main__":
    image_etl()



