#!/usr/bin/env bash

# exit on error
set -e

# echo "DEBUG: SCRIPT REACHED"

# define paths
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"

mkdir -p "$PROJECT_ROOT/logs"
LOGFILE="$PROJECT_ROOT/logs/0_mlflow.log"

# import env variables from .env
{
  if [ -f "$PROJECT_ROOT/.env" ]; then
      echo "Loading environment variables from $PROJECT_ROOT/.env"
      set -o allexport
      source "$PROJECT_ROOT/.env"
      set +o allexport
  fi
} >> "$LOGFILE" 2>&1

# fallback if no .env file is present
MLFLOW_DB=${MLFLOW_DB:-"sqlite:///mlflow/db/mlflow.db"} 
ARTIFACT_DIR=${ARTIFACT_DIR:-"./mlflow/artifacts"}

# shorten path to last 2–3 parts for logging
short_db=$(echo "$MLFLOW_DB" | awk -F'/' '{print $(NF-2)"/"$(NF-1)"/"$NF}')
short_artifacts=$(echo "$ARTIFACT_DIR" | awk -F'/' '{print $(NF-1)"/"$NF}')

# run script
{
  echo ""
  echo "===== START MLFLOW_SERVER_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
  echo "DB: .../$short_db"
  echo "Artifacts: .../$short_artifacts"

  # SQLite --> only local + one user access possible
  exec mlflow server \
    --backend-store-uri $MLFLOW_DB \
    --default-artifact-root $ARTIFACT_DIR \
    --host 127.0.0.1 \
    --port 5000 \
     >> "$LOGFILE" 2>&1 &
  
  echo "MLflow server started with PID $!"
  echo "===== END MLFLOW_SERVER_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
  echo ""

}  >> "$LOGFILE" 2>&1
