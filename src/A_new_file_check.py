#imports
from pathlib import Path
import utils.file_helper as fh 
import utils.setup_helper as sh 
import utils.data_helper as dh 
from utils.settings import session


# function for comparing the new data with the data already existing in the MongoDb-Collection
# unfortenately, this funtion return True, but doesnt work properly, so it doesnt have an impact on the ETL-DAG
def new_file_check(f_names=None, folder=None):
    # Check if any file paths were passed
    if not f_names:
        print("No file paths were passed as input.")
        return None
    # If no folder provided, use default DATA_LAKE folder from environment/session
    if not folder:
        sh.load_env_vars()

        sh.get_paths()
        DATA = session.data 

        # Ensure DATA_LAKE exists
        DATA_LAKE = Path(DATA) / "data_lake"
        DATA_LAKE.mkdir(parents=True, exist_ok=True)

        folder = DATA_LAKE

    # Separate files by type
    csv_files = [f for f in f_names if Path(f).suffix.lower() == ".csv"]
    zip_files = [f for f in f_names if Path(f).suffix.lower() == ".zip"]

    # Generate previews for CSV files
    df_dict = fh.data_preview(csv_files, folder)
    if not df_dict:
        print("Files cannot be found. Please check the input.")
        return None
    
    # Check which products in CSV files are new or need updating
    need_update = dh.check_latest_products(df_dict, "products")

    # Attach corresponding ZIP image files to the update info
    need_update["img_files"] = zip_files
    
    return need_update

    
    
        
        
        