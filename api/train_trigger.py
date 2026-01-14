from fastapi import APIRouter, HTTPException
from datetime import datetime
import requests
import time
import logging
# Log message to confirm router module is loaded
print(">>> train_trigger router loaded")

# Create a router for training-related endpoints
router = APIRouter(prefix="/train", tags=["Training"])

# Initialize module-level logger
logger = logging.getLogger(__name__)


# Airflow configuration
AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
DAG_ID = "train_knn_with_mlflow"

# Trigger training DAG endpointst("/trigger")
@router.post("/trigger")
def trigger_train():
    """
    Triggers the Airflow DAG responsible for training the KNN model.

    - Generates a unique dag_run_id
    - Calls the Airflow REST API to start the DAG
    - Returns the DAG run identifier if successful
    """
    # Record start time for execution duration tracking
    start_time = time.time()

    # Generate a unique DAG run ID using the current timestamp
    dag_run_id = f"api_trigger_train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # Send POST request to Airflow to trigger the DAG
        response = requests.post(
            f"{AIRFLOW_URL}/dags/{DAG_ID}/dagRuns",
            auth=("airflow", "airflow"),
            json={
                "dag_run_id": dag_run_id,
                "conf": {"source": "knn-api"}
            },
            timeout=10
        )
        # Airflow returns 200 or 201 on successful DAG trigger
        if response.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=response.text)
        
        # Success response
        return {"status": "Training DAG triggered", "dag_run_id": dag_run_id}

    except Exception as e:
        # Log and propagate errors as HTTP 500
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Measure total execution time (currently not returned)
        duration = time.time() - start_time
