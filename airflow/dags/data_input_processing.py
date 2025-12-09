## data_input_processing.py
# imports
# import os
import sys
sys.path.insert(0, "/opt/airflow/src")
sys.path.insert(0, "/opt/airflow/src/utils")

from pathlib import Path
from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.sensors.filesystem import FilePatternSensor
# from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
from airflow.sensors.python import PythonSensor

from A_new_file_check import new_file_check
from A_fetch_files import fetch_files
from B_ETL_text import text_etl
from C_embed_text import text_embed


# defining paths
DATA_INPUT = Path("/opt/airflow/data/data_input")
DATA_LAKE = Path("/opt/airflow/data/data_lake")
DATA_DONE = Path("/opt/airflow/data/data_done")

types_allowed = [".csv", 
                 # ".json"
                 ]

# functions
def _any_file_exists(**context):
    folder = DATA_INPUT
    files = [str(f) for f in folder.iterdir()
             if f.suffix.lower() in types_allowed]
    
    return bool(files) #  if files else False

# defining DAG
@dag(
    dag_id="data_processing_pipeline", 
    tags=["franke", "rakuten", "recommender"],
    schedule_interval="@monthly",
    start_date=datetime(2025, 12, 4),
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(seconds=10)
    }
)


def data_processing_pipeline():

    # sensor checks for new files 
    wait_for_file = PythonSensor(
            task_id="wait_for_file",
            python_callable = _any_file_exists, 
            poke_interval=10,
            timeout=60 * 60,   
            mode="poke"
    )
            
    # task 1: 
    @task
    def run_fetch_files():
        files = fetch_files(DATA_INPUT)
        return [str(f) for f in files]
    
    # task 2: check content of new files 
    @task
    def run_new_file_check(files):
       return new_file_check(files=files, path=DATA_LAKE)

    # task 2: ETL text  
    @task
    def run_text_etl(files):
        return text_etl(files)


    # task 3: create embeddings from text
    @task
    def run_text_embed(_):
        return text_embed()

    # define dependencies
    fetched = run_fetch_files()
    checked = run_new_file_check(fetched)
    etl_text = run_text_etl(checked)
    run_text_embed(etl_text)
    
    wait_for_file >> fetched

pipeline = data_processing_pipeline()
    