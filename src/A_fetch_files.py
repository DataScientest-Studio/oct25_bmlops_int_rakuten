## 
# imports
from pathlib import Path
import src.utils.setup_helper as sh 
from utils.settings import session

def fetch_files(path=None, file_type=None):
    if not path:
        # load env variables from .env and .env.session
        sh.load_env_vars()

        # load paths from .env
        sh.get_paths()
        # print("[DEBUG] ROOT loaded =", session.root)
        # ROOT = Path(session.root)
        DATA = Path(session.data)

        INPUT = DATA / "data_input"
        INPUT.mkdir(parents=True, exist_ok=True) 

        path = INPUT

    #     LAKE = DATA / "data_lake"
    #     LAKE.mkdir(parents=True, exist_ok=True)
    # else: 
    #     LAKE = path
    
    

    # if cli is True:
    # Look for files in folder

    if not file_type:
        file_type = [".csv", ".json"]

    folder = Path(path)
    files = [f for f in folder.iterdir() if f.suffix.lower() in file_type]

    return files


if __name__ == "__main__":
    fetch_files()