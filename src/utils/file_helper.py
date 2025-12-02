## file_helper.py
# imports
import os
from pathlib import Path
from datetime import datetime
import pickle

import pandas as pd



##########


def save_pickle(file, path, folder=None):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not folder:
        file_path = os.path.join([path, ".pkl"])

    else:
        file_path = os.path.join([folder, path, ".pkl"])

    try:
        # save as pickle
        with open(file_path, "wb") as f:
            pickle.dump(file, f)
        
        print("[SUCCESS] File saved")
    except:
        print("[ERROR] Saving file as pkl.")


def read_csv(file_path):

    f_path = Path(file_path)
    pd.read_csv("file_path")