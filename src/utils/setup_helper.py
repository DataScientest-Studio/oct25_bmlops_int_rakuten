##
# imports
# from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import io
from pathlib import Path
import importlib
import argparse
from datetime import datetime 

# from datetime import datetime
# import subprocess
import sys
from utils.settings import session


def load_args():
    """
    Load variables passed as input from shell command. 
    """
    # detect jupyter
    if "ipykernel" in sys.modules:
        print("[INFO] Jupyter detected — skipping argparse.")
        class DummyArgs:
            env = "core"
            n_neighbors = 5
            query_pid = None
            msg = ""

        args = DummyArgs()

    else:    
        # define parsed arguments
        parser = argparse.ArgumentParser()
        # parser.add_argument("--env", choices=["core", "heavy_+", "dev_+", "all"], default="core")
        # parser.add_argument("--branch", type=str, default="phase_1_es")
        parser.add_argument("--db", choices=["mongo_db"], default="mongo_db")
        parser.add_argument("--preview", type=bool, default=True)
        parser.add_argument("--neigh", type=int, default=5)
        parser.add_argument("--qpid", type=int, default=None)
        parser.add_argument("--msg", "-m", choices=["", "auto", "tmp"], 
                            default="auto")
                            # help="Commit message for git push",
                            # default=f"Auto-commit: Several minor improvements, no major change ({datetime.now().isoformat(timespec='seconds')}" )
        
        args, unknown = parser.parse_known_args()

        if unknown:
            print(f"[INFO] Ignoring unknown CLI arguments: {unknown}")
    
    return args


def load_env_vars():
    """
    Load environment variables from a .env file if available.
    """
    env_path = find_dotenv()
    session_path = find_dotenv(filename=".env.session")

    if session_path:
        load_dotenv(session_path)
        print("Variable from .env.session loaded")

    if session.env_loaded:
        return None
    
    if env_path:
        load_dotenv(env_path)
        print("Variable from .env loaded")
        session.env_loaded = True
    

def info_as_string(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


def log_header(title, log=None):
    if log:
        log.write("\n")
        log.write("=" * 50)
        log.write(f"--- {title} --- {datetime.now():%Y-%m-%d %H:%M:%S} ---")
        log.write("=" * 50 + "\n")

    else:
        print("\n")
        print("=" * 50 + "\n")
        print(f"--- {title} --- {datetime.now():%Y-%m-%d %H:%M:%S} ---\n")
        print("=" * 50 + "\n")

def get_paths():        
    from utils.settings import session
    env = session.env
    print(f"Using env: {env}")
    # print("[DEBUG] LOCAL_ROOT =", os.getenv("LOCAL_ROOT"))

    if env == "heavy":
        # mount with GoogleDrive
        try:
            from google.colab import drive
            drive.mount('/content/drive')

        except ImportError:
            # !uv add google.colab
            # from google.colab import drive
            raise RuntimeError("Colab environment required for --env colab")

        ROOT = Path(os.getenv("COLAB_ROOT"))
        DATA = Path(os.getenv("COLAB_DATA"))
        VENV = Path(os.getenv("COLAB_VENV"))

    else:
        ROOT = Path(os.getenv("LOCAL_ROOT")).resolve()
        DATA = Path(os.getenv("LOCAL_DATA"))
        VENV = Path(os.getenv("LOCAL_VENV"))
    
    session.root = ROOT
    session.data = DATA
    session.venv = VENV
    session.save_session()

    print("Paths loaded")
    # return ROOT, DATA, VENV



    # # load environment variables
    # if args.env == "colab":
    #     # mount with GoogleDrive
    #     try:
    #         from google.colab import drive
    #         drive.mount('/content/drive')

    #     except ImportError:
    #         # !uv add google.colab
    #         # from google.colab import drive
    #         raise RuntimeError("Colab environment required for --env colab")

    #     ROOT = Path(os.getenv("COLAB_ROOT"))
    #     DATA = Path(os.getenv("COLAB_DATA"))
    #     VENV = Path(os.getenv("COLAB_VENV"))

    # else:
    #     ROOT = Path(os.getenv("LOCAL_ROOT")).resolve()
    #     DATA = Path(os.getenv("LOCAL_DATA"))
    #     VENV = Path(os.getenv("LOCAL_VENV"))
    
    # return ROOT, DATA, VENV, args


def shorten_path(path, n=3):
    p = Path(path).parts
    return "/".join(p[-n:])


def get_latest_training_folder(root):
    dirs = [d for d in root.iterdir() if d.is_dir()]
    if not dirs:
        print("No similarity matrix directories found.")
        return None
    return max(dirs, key=lambda d: d.name)

