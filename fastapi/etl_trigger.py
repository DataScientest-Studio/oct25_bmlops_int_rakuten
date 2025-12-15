from fastapi import FastAPI
import requests
from datetime import datetime

AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
DAG_ID = "data_processing_pipeline"

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI ETL Trigger Active"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/trigger-etl")
def trigger_etl():
    dag_run_id = f"api_trigger_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    response = requests.post(
        f"{AIRFLOW_URL}/dags/{DAG_ID}/dagRuns",
        auth=("airflow", "airflow"),   # Airflow credentials
        json={
            "dag_run_id": dag_run_id,
            "conf": {"comment": "PLACEHOLDER -- dynamic input"}
        })

    if response.status_code != 200:
        return {"error": response.text}

    return {
        "status": "Pipeline triggered",
        "dag_run_id": dag_run_id
    }
