## setup_helper.py
# imports
# from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import io
from pathlib import Path
# import importlib
# import argparse
import inspect 
from datetime import datetime 
import click
from functools import wraps

# from datetime import datetime
# import subprocess
# import sys
from .settings import session


def load_env_vars(files=None):
    """
    Load environment variables from .env files if available.
    """
    env_list = [".env.session"]

    if not session.env_loaded:
        env_list.append(".env")
        
    if files:
        if isinstance(files, Path):
            env_list.append(files)
        
        if isinstance(files, list):
            for f in files:           
                if isinstance(f, (str, Path)):
                    env_list.append(f)
                else:
                    print(f"Invalid data type: {f} is {type(f)}")
    
    for env in env_list:
        env_path = find_dotenv(filename=env)
        if env_path:
            load_dotenv(env_path)
            print(f"Variables from {env} loaded")

        if env == ".env":
            session.env_loaded = True
            session.save_session()
 
    
    #         f_path = find_dotenv(filename=".env.session")

    # session_path = find_dotenv(filename=".env.session")
    # if session_path and os.path.exists(session_path):
    #     load_dotenv(session_path, override=True)
    #     print("Variables from .env.session loaded")
    
    

def shorten_path(path, n=3):
    p = Path(path).parts
    return "/".join(p[-n:])


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
    env = session.env
    print(f"Using env: {env}")
    # print("[DEBUG] LOCAL_ROOT =", os.getenv("LOCAL_ROOT"))

    if env == "all":
        # mount with GoogleDrive
        try:
            from google.colab import drive
            drive.mount('/content/drive')

        except ImportError:
            # !uv add google.colab
            # from google.colab import drive
            raise RuntimeError("Colab environment required for --env all")

        ROOT = os.getenv("COLAB_ROOT")
        DATA = os.getenv("COLAB_DATA")
        VENV = os.getenv("COLAB_VENV")

    else:
        ROOT = os.getenv("LOCAL_ROOT")
        DATA = os.getenv("LOCAL_DATA")
        VENV = os.getenv("LOCAL_VENV")
    
    session.root = Path(ROOT) if ROOT else ""
    session.data = Path(DATA) if DATA else ""
    session.venv = Path(VENV) if VENV else ""
    session.save_session()

    print("Paths loaded")


def cli_or_api(func):
    sig = inspect.signature(func)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)

        # Prüfen, ob irgendein Argument wirklich "gesetzt" ist
        has_provided = False
        for name, param in sig.parameters.items():
            if name in bound.arguments:
                val = bound.arguments[name]
                # Default-Wert bestimmen
                default = None if param.default is inspect._empty else param.default

                # "gesetzt" = nicht None und ungleich Default
                if val is not None and val != default:
                    has_provided = True
                    break

        # Case (1): API call
        if has_provided:
            return func(*args, **kwargs)

        # Case (2): CLI call (no argmuents passed)
        params = {}
        for name, param in sig.parameters.items():           
            default = None if param.default is inspect._empty else param.default
            annotation = str if param.annotation is inspect._empty else param.annotation

            params[name] = click.prompt(
                    f"Enter value for {name}",
                    type=annotation,
                    default=default,
                    show_choices=True
                )

        return func(**params)
    
    return wrapper


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

        #     if name not in bound.arguments:
        #         default = param.default if param.default is not inspect._empty \
        #                                 else None
        #         typ = param.annotation if param.annotation is not inspect._empty \
        #                                 else str

        #         bound.arguments[name] = click.prompt(
        #             f"Enter value for {name}",
        #             type=typ,
        #             default=default,
        #         )

# def load_args():
#     """
#     Load variables passed as input from shell command. 
#     """
#     # detect jupyter
#     if "ipykernel" in sys.modules:
#         print("[INFO] Jupyter detected — skipping argparse.")
#         class DummyArgs:
#             env = "core"
#             n_neighbors = 5
#             query_pid = None
#             msg = ""

#         args = DummyArgs()

#     else:    
#         # define parsed arguments
#         parser = argparse.ArgumentParser()
#         # parser.add_argument("--env", choices=["core", "heavy_+", "dev_+", "all"], default="core")
#         # parser.add_argument("--branch", type=str, default="phase_1_es")
#         parser.add_argument("--db", choices=["mongo_db"], default="mongo_db")
#         parser.add_argument("--preview", type=bool, default=True)
#         parser.add_argument("--neigh", type=int, default=5)
#         parser.add_argument("--qpid", type=int, default=None)
#         parser.add_argument("--msg", "-m", choices=["", "auto", "tmp"], 
#                             default="auto")
#                             # help="Commit message for git push",
#                             # default=f"Auto-commit: Several minor improvements, no major change ({datetime.now().isoformat(timespec='seconds')}" )
        
#         args, unknown = parser.parse_known_args()

#         if unknown:
#             print(f"[INFO] Ignoring unknown CLI arguments: {unknown}")
    
#     return args


def get_latest_training_folder(root):
    dirs = [d for d in root.iterdir() if d.is_dir()]
    if not dirs:
        print("No similarity matrix directories found.")
        return None
    return max(dirs, key=lambda d: d.name)

