## 
# imports
from pathlib import Path
import utils.setup_helper as sh 
from utils.settings import session
import utils.file_helper as fh 

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

    if not file_type:
        file_type = [".csv", 
                     # ".json"
                     ]

    folder = Path(path)
    files = [str(f) for f in folder.iterdir() if f.suffix.lower() in file_type]
    
    if not files:
        print("No new files found")
        return None
    
    files_new = []
    for f in files:
        # check for columns
        # to be added
        f_moved = fh.move_file(f, path)
        files_new.append(str(f_moved))

    print(f"Found {len(files)} files in 'data_input' folder and moved them to folder 'data_lake'")
    return files_new


if __name__ == "__main__":
    fetch_files()