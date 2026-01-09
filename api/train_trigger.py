from fastapi import APIRouter, HTTPException
from datetime import datetime
import requests
import time
import logging
print(">>> train_trigger router loaded")
router = APIRouter(prefix="/train", tags=["Training"])

logger = logging.getLogger(__name__)

AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
DAG_ID = "train_knn_with_mlflow"

@router.post("/trigger")
def trigger_train():
    start_time = time.time()
    dag_run_id = f"api_trigger_train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
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

        return {"status": "Training DAG triggered", "dag_run_id": dag_run_id}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        duration = time.time() - start_time
