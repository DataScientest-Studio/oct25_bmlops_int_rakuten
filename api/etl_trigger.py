import os
import logging
import time
from datetime import datetime

import requests
from fastapi import APIRouter, HTTPException, Response
from prometheus_client import Counter, Histogram, generate_latest

from utils.setup_helper import load_env_vars
print(">>> etl_trigger router loaded")
# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Env ---
load_env_vars()

# --- Router ---
router = APIRouter(prefix="/etl", tags=["ETL"])

# --- Metrics ---
api_request_total = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["endpoint", "method", "status_code"]
)

api_request_duration_seconds = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["endpoint", "method", "status_code"]
)

# --- Airflow Config ---
AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
DAG_ID = "data_processing_pipeline"


@router.post("/trigger")
def trigger_etl():
    start_time = time.time()
    status_code = "200"

    try:
        dag_run_id = f"api_trigger_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        response = requests.post(
            f"{AIRFLOW_URL}/dags/{DAG_ID}/dagRuns",
            auth=("airflow", "airflow"),
            json={
                "dag_run_id": dag_run_id,
                "conf": {"source": "knn-api"}
            },
            timeout=10
        )

        if response.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=response.text)

        return {
            "status": "Pipeline triggered",
            "dag_run_id": dag_run_id
        }

    except Exception as e:
        status_code = "500"
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        duration = time.time() - start_time
        api_request_duration_seconds.labels(
            "/etl/trigger", "POST", status_code
        ).observe(duration)

        api_request_total.labels(
            "/etl/trigger", "POST", status_code
        ).inc()


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")