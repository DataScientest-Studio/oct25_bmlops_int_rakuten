## 
# imports
from pathlib import Path
import utils.setup_helper as sh 
from utils.settings import session
import utils.file_helper as fh 

def fetch_files(src_path=None, dst_path=None, file_type=None):
    if not src_path or not dst_path:
        # # load env variables from .env and .env.session
        # sh.load_env_vars()

        # # load paths from .env
        # sh.get_paths()
        # # print("[DEBUG] ROOT loaded =", session.root)
        # # ROOT = Path(session.root)
        # DATA = Path(session.data)

        # INPUT = DATA / "data_input"
        # INPUT.mkdir(parents=True, exist_ok=True) 

        # path = INPUT
        print("At least one file path is  not given.")

    if not file_type:
        file_type = [".csv", 
                    ".zip", 
                     # ".json"
                     ]

    folder = Path(src_path)
    # print(f"[DEBUG] src_path ({src_path}); dst_path ({dst_path})")
    files = [str(f) for f in folder.iterdir() \
             if f.suffix.lower() in file_type]
    
    if not files:
        print("No new files found")
        return []
    
    files_new = []
    for f in files:
        f_moved = fh.move_file(f, Path(dst_path))
        files_new.append(str(f_moved))

    print(f"Found {len(files)} files in 'data_input' folder and moved them to folder 'data_lake'")
    return files_new


if __name__ == "__main__":
    fetch_files()
