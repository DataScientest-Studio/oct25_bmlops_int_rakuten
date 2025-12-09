# imports 
from pathlib import Path

import utils.ETL_preprocess_helper as eph 
import utils.database_helper as dbh 
import utils.file_helper as fh 
import utils.setup_helper as sh 
import utils.data_helper as dh 
from utils.settings import session

def new_file_check(f_names=None, folder=None):
    if not f_names:
        print("No file paths were passed as input.")
        return None
    
    if not folder:
        # load env variables from .env and .env.session
        sh.load_env_vars()

        # load paths
        sh.get_paths()
        DATA = session.data 
        
        DATA_LAKE = Path(DATA) / "data_lake"
        DATA_LAKE.mkdir(parents=True, exist_ok=True)

        folder = DATA_LAKE

    # workflow  
    df_dict = fh.data_preview(f_names, folder)
    if not df_dict:
        print("Files cannot be found. Please check the input.")
        return None
        
    update_text, update_image = dh.check_latest_products(df_dict, "products")
    
    if update_text and update_image:
        print("⚠️ Database needs an update.")
        if update_text:
            print("⚠️ Text columns are not up-to-date")
        
        if update_image:
            print("⚠️ Image columns are not up-to-date")
        
        return update_text, update_image
    
    else: 
        print("✅ Database is up-to-date")
        return None, None
    
        
        
        