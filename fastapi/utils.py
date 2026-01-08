import json
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

import numpy as np

import pandas as pd
from sklearn import model_selection 
from datetime import datetime
import io
from dotenv import load_dotenv, find_dotenv
import joblib
from pathlib import Path
import os
import logging

# from evidently.ui.workspace import Workspace



def load_env_vars(f_name=".env"):
    """
    Load environment variables from an .env file if available.
    """

    # running_in_docker = Path("/.dockerenv").exists()

    # if running_in_docker:
    #     env_file = Path(".env.docker")
    # else:
    #     env_file = Path(".env")

    env_path = find_dotenv(filename=f_name)
    if env_path:
        load_dotenv(env_path)
        print("Variables from .env loaded")
    
    else:
        print("No .env file was found")



def get_workspace(workspace_name):

    try:
        return Workspace(workspace_name)
        # print(f"✅ Workspace '{workspace_name}' already exists.")
    
    except Exception:
        print(f"⚠️ Workspace '{workspace_name}' not found. Creating it...")
        ws = Workspace.create(workspace_name)
        # ws.open(workspace_name)
        print(f"✅ Workspace '{workspace_name}' created.")
        return ws


def get_project(workspace, project_name, project_description):
    # Check if project already exists
    for p in workspace.list_projects():
        if p.name == project_name:
            project = p
            
            return project

    # Create a new project if it doesn't exist
    project = workspace.create_project(project_name)
    project.description = project_description

    return project


def add_report(workspace_name, project_name, project_description, report):
    """
    Adds a report to a project in a workspace.
    This function will be useful to you
    """
    ws = get_workspace(workspace_name)
    proj = get_project(ws, project_name, project_description) 
    # Add report to the project
    ws.add_report(proj.id, report)

    print(f"New report added to project '{project_name}' from workspace '{workspace_name}'.\n")


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


def load_df(f_path=None):

    """
HEAD:
            Unnamed: 0  instant      dteday  season  yr  mnth  hr  holiday  weekday  workingday  weathersit  temp   atemp   hum  windspeed  casual  registered  cnt
0  2011-01-01 00:00:00        1  2011-01-01       1   0     1   0        0        6           0           1  0.24  0.2879  0.81        0.0       3          13   16
1  2011-01-01 01:00:00        2  2011-01-01       1   0     1   1        0        6           0           1  0.22  0.2727  0.80        0.0       8          32   40
2  2011-01-01 02:00:00        3  2011-01-01       1   0     1   2        0        6           0           1  0.22  0.2727  0.80        0.0       5          27   32
3  2011-01-01 03:00:00        4  2011-01-01       1   0     1   3        0        6           0           1  0.24  0.2879  0.75        0.0       3          10   13
4  2011-01-01 04:00:00        5  2011-01-01       1   0     1   4        0        6           0           1  0.24  0.2879  0.75        0.0       0           1    1
    """

    if not f_path:
        DATA = os.getenv("DATA")    
        f_path = Path(DATA) / "df_raw.csv"

        # load df
        raw_data = pd.read_csv(f_path) #, index_col=0)
        raw_data["Unnamed: 0"] = pd.to_datetime(raw_data["Unnamed: 0"], 
                                                errors="raise")
        raw_data = raw_data.set_index("Unnamed: 0")
    
    else:
        raw_data = pd.read_csv(f_path, index_col=0)

    return raw_data


def prepare_data(feature_dict, ref_period, eda=False, f_path=None):
    # Feature selection
    num_feats = feature_dict["num_feat"]
    cat_feats = feature_dict["cat_feat"]
    target = feature_dict["target"]

    # print(f"[DEBUG] num_feats: {num_feats}")
    # print(f"[DEBUG] cat_feats: {cat_feats}")
    # print(f"[DEBUG] target: {target}")

    raw_data = load_df(f_path)

    if eda:
        df_preview(raw_data)   

    # split data into "reference" and "current"
    raw_data = raw_data.sort_index()
    raw_data.index = pd.to_datetime(raw_data.index)

    start, end = pd.to_datetime(ref_period)

    reference = raw_data.loc[(raw_data.index >= start) & (raw_data.index <= end)]
    if reference.empty:
        raise ValueError(
            f"No data in reference period {ref_period}. "
            f"Index range: {raw_data.index.min()} - {raw_data.index.max()}"
        )

    # train-test-split
    X = reference[num_feats + cat_feats]
    y = reference[target]

    if X.shape[0] == 0:
        raise ValueError("prepare_training(): Dataset is empty after filtering. "
        "Check ref_period, feature selection and target availability.")
    
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
                            X, y, 
                            test_size=0.3,
                            random_state=123
                                )

    split_data = dict(zip(["X", "X_train", "X_test", "y", "y_train", "y_test"], 
                            [X, X_train, X_test, y, y_train, y_test]))

    return split_data

def df_preview(df):   
    # df preview
    log_header(f"EDA RAW DATA")
    
    # print(f"\n{'='*30}\n--- EDA RAW DATA '{f}' ---") 
    print("SHAPE:\t", df.shape)
    print("INFO\n", info_as_string(df))
    print(f"HEAD:\n{df.head(5)}\n")
    print(f"{'='*30}\n--- END OF EDA ---\n{'='*30}\n")


def get_latest_file(folder=None, extension=None):
    if not folder:
        MODEL = os.getenv("MODEL")
        folder = Path(MODEL)
        folder.mkdir(exist_ok=True, parents=True)

    if not folder:
        raise RuntimeError(
            "Environment variable 'MODEL' is not set. "
            "Cannot load ML model."
        )

    if not extension:
        extension = [".joblib"]

    candidates = [str(f) for f in folder.iterdir()
                    if f.suffix.lower() in extension]
    
    # list(folder.glob("*.joblib"))
    latest_file = max(candidates, key=lambda d: Path(d).name)
    file= joblib.load(latest_file)

    print(f"Loaded File '{latest_file}'.")
    return file


def regression_metrics(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    y_true = y_true[mask]
    y_pred = y_pred[mask]

    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mape": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100),
        "r2": float(r2_score(y_true, y_pred)),
    }


def get_metric_class(report, 
                    metric_class="RegressionQualityMetric"):

    # Column drift?
    # (1) DataDriftPreset
    # (2) DataSetDriftMetric
    #     ColumnDriftMetric
    #     DataDriftTable
    # 
    # 🎯 Target Drift
    # (1) TargetDriftPreset
    # (2) RegressionTargetDriftMetric
    #     ClassificationTargetDriftMetric

    # 🤖 Prediction / Model Drift
    # (1) RegressionPreset / ClassificationPreset
    # (2) RegressionQualityMetric
    #     ClassificationQualityMetric

    report_dict = report.as_dict()  

    
    # logging.info("report:\n%s", 
    #              json.dumps(report.as_dict(), indent=2))
      
    results = None
    
    for m in report_dict.get("metrics", []):
        if m.get("metric") == metric_class:
            results = m.get("result", {})
        # return metric.get("result", {}).get("metrics", {}).get(metrics, None)
            
    return results

def get_metrics(report, 
                metric_class="RegressionQualityMetric", 
                metrics=None): 
    
    results = get_metric_class(report, 
                            metric_class)
    
    if not results:
        return None, None
            
    if metrics is None:
        metrics = ["rmse", 
                    "mean_abs_perc_error",
                   "mean_abs_error",
                   "r2_score"]
    
    metrics_ref = {}
    metrics_curr = {}    

    for metric in metrics:
        metrics_ref[metric] = results.get("reference", {}).get(f"{metric}", None)
        metrics_curr[metric] = results.get("current", {}).get(f"{metric}", None)

    return metrics_ref, metrics_curr
        

def extract_evidently_report(report, report_name, report_type=None):
    # transform to dict
    report_dict = report.as_dict() 

    #  extract keys + values
    print(f"Report: {report_name}\t (key --> value)")
    for key, value in report_dict.items():
        if not isinstance(value, (list, dict)):
            print(f"- {key} --> {value}")
        else:
            print(f"- {key}")

        if isinstance(value, list):
            for i, val in enumerate(value):
                if len(val) == 1:
                    print(f" - list_{i}: {val}")
                else:
                    print(f" - list_{i} (list element - dtype / length: {type(val)} / {len(val)}):")
                    for o, (k, v) in enumerate(val.items()):
                        if len(v) == 1:
                            print(f"  - element_{o}: {k} --> {v}")
                        else:
                            print(f"  - element_{o}: {k} (value  - dtype / length: {type(v)} / {len(v)}): ")
                            if isinstance(v, str):
                                print(f"\t--> {v}")
                                continue

                            for p, (k_1, v_1) in enumerate(v.items()):
                                if isinstance(v_1, (float, int)):
                                    print(f"  - subelement_{p}: {k_1} --> integer + floats")
                                    continue

                                if v_1 is None: 
                                    print(f"   - subelement_{p}: {k_1} --> None")
                                    continue

                                if len(v_1) == 1:
                                    print(f"   - subelement_{p}: {k_1} --> {v_1}")
                                else:
                                    print(f"   - subelement_{p}: {k_1} (value  - dtype / length: {type(v_1)} / {len(v_1)}):")


                            #     print(f"   - subelement_{p}: {v_1 if len(v_1) == 1 else f'length: {len(v_1)}'}")
                    print()

        if isinstance(value, dict):
            for j, (name, val_new) in enumerate(value.items()):
                if len(val_new) == 1:
                    print(f" - dict_{j}: {name} --> {val_new}")
                else:
                    print(f" - dict_{j}: {name}")
                    for k, val_newer in enumerate(val_new):
                        print(f"  - element_{k}: {val_newer if len(val_newer) == 1 else f'length {len(val_newer)}'}")

    print(f"{25*'='}")
