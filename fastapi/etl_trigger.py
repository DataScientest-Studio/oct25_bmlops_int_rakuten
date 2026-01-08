from fastapi import FastAPI, HTTPException, Response, Request
import requests
import os
import logging
import time
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, Gauge

import utils

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----- load env-variables -----------
utils.load_env_vars(f_name=".env.docker")   # for docker deployment
 
ws_name = os.getenv("WORKSPACE_NAME")
proj_name = os.getenv("PROJECT_NAME")
proj_desc = os.getenv("PROJECT_DESCRIPTION")

# --- FastAPI App Initialization ---
app = FastAPI()

# --- Prometheus Metrics Definitions ---

api_request_total = Counter(name="api_requests_total", 
                            documentation="Total number of API requests", 
                            labelnames=['endpoint', 'method', 'status_code'], 
                            # registry=registry
                            )

api_request_duration_seconds = Histogram(name="api_request_duration_seconds", 
                                        documentation="API request duration in seconds", 
                                        labelnames=['endpoint', 'method', 'status_code'], 
                                        # buckets=(0.005, 0.01, 0.025), 
                                        # registry=registry
                                        )


# --- Global Variables for Model and Data ---
AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
DAG_ID = "data_processing_pipeline"

# --- Pydantic Models for API Input/Output ---


# --- API Endpoints ---
@app.get("/")
def root():
    return {"message": "FastAPI ETL Trigger Active"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/trigger-etl")
def trigger_etl():
    start_time = time.time()
    status_code = "200"

    try:
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
    
    except HTTPException as e:
        status_code = str(e.status_code)
        raise

    except Exception as e:
        logger.error(f"Error during trigger: {e}")
        status_code = "500"
        raise HTTPException(status_code=500, 
                            detail=f"Triggering ETL-pipeline failed due to an internal error: {e}")
    finally:
        end_time = time.time()
        duration = end_time - start_time
        api_request_duration_seconds.labels(
                                        endpoint="/trigger-etl", 
                                        method="POST", 
                                        status_code=str(status_code)
                                        ).observe(duration)
        api_request_total.labels(
                            endpoint="/trigger-etl", 
                             method="POST", 
                             status_code=str(status_code)
                             ).inc()


@app.get("/metrics")
async def metrics():
    """
    Expose Prometheus metrics.
    """
    return Response(generate_latest(), media_type="text/plain")

# -------------------------
# Potential dynamic input (--> conf:)
# -------------------------
# "filename": "products_2024_12.csv",     # welche Dateien

# "only_text": true,                      # welche Daten
# "process_text": true,                   
# "process_images": false

# "debug_mode": false                     

# "force_etl": true                       # etl-Prozess erzwingen
# "force_reprocess": true                 # kompletten Prozess erzwingen

# "export_to_s3": true                    # Export?

# "embedding_model": "all-MiniLM-L6-v2"   # welches MOell nutzen?
# "threshold": 0.8                        # welche HyperParameter?

# "max_missing": 0.2,                     # Datenvalidierung
# "drop_duplicates": true

# "cleaning_level": "strict"              # steuerung verschiedener Modi

# "write_mode": "overwrite"               # Parameter für DB, VErsionierung, Tabelle,...
# "collection": "products_raw"

# "send_slack": true                      # Alert-Trigger verwalten

# "run_tag": "customer_upload_123"        # Info für Grafana_tracking-DB