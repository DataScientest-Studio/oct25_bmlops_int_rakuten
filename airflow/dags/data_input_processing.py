## data_input_processing.py
# imports
import os
from pathlib import Path

from datetime import datetime, timedelta
# from airflow import DAG
from airflow.operators.python import PythonSensor
from airflow.sensors.filesystem import FilePatternSensor
from airflow.operators.python import PythonOperator

from src.A_new_file_check import new_file_check
from src.B_ETL_text import text_etl
from src.C_embed_text import text_embed


# defining paths
DATA_INPUT = "/opt/airflow/data/input"
DATA_LAKE = ""
DATA_DONE = ""

# functions
def _any_file_exists(**context):
    folder = Path(DATA_INPUT)
    files = [str(f) for f in folder.iterdir()
             if f.suffix.lower() in [".csv", ".json"]]
    
    return files if files else False

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
            
    # task 1: check content of new files 
    @task
    def run_new_file_check(files):
       return new_file_check(files)

    # task 2: ETL text  
    @task
    def run_text_etl(files_checked):
        return text_etl(files_checked)


    # task 3: create embeddings from text
    @task
    def  run_text_embed(data):
        return text_embed(data)

    # define dependencies
    files_checked = run_new_file_check(wait_for_file, DATA_LAKE, False)
    run_text_etl(files_checked, path=(DATA_LAKE, DATA_DONE))
    run_text_embed(text_etl_result)
    

pipeline = data_processing_pipeline()
    