##
# imports 
import utils.ETL_preprocess_helper as eph 
import utils.database_helper as dbh 
import utils.file_helper as fh 
import utils.setup_helper as sh 
import utils.data_helper as dh 
from utils.settings import session
# from src.A_new_file_check import new_file_check

def text_etl(files=None, path=None):
    # if not files:
    #     files = new_file_check()

    if not files:
        print("No file paths were passed as input.")
        return None
    
    if not path:
        # load env variables from .env and .env.session
        sh.load_env_vars()

        # load paths
        sh.get_paths()
        DATA = session.data 
        
        DATA_LAKE = DATA / "data_lake"
        DATA_LAKE.mkdir(parents=True, exist_ok=True)

        DATA_DONE = DATA / "data_done"
        DATA_DONE.mkdir(parents=True, exist_ok=True)

        # DATA_ERROR = DATA / "data_error"
        # DATA_ERROR.mkdir(parents=True, exist_ok=True)
    else:
        DATA_LAKE, DATA_DONE = path

    # workflow  
    df_dict = fh.data_preview(files)
    if not df_dict:
        print("Files cannot be found. Please check the input.")
        return None
        
    dfs_to_update = dh.check_latest_products(df_dict, "products")
    if not dfs_to_update:
        print("✅ Database is up-to-date")
        return None
    
    cleaned_dfs = eph.clean_text(dfs_to_update)
    dfs = fh.merge_dfs(cleaned_dfs)
    if not dfs:
        return None
                
    dbh.upload_data_mongoDB(dfs) 
                

if __name__ == "__main__":
    text_etl()
