#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/1_etl.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
ENV_MODE="${1:-local}"

# run etl scripts (text + image) and log output
{
    echo "===== START ETL - TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/1_etl_text.py --env "$ENV_MODE"

    echo "===== END ETL - TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1

{
    echo "===== START ETL - IMAGE [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/1_etl_image.py --env "$ENV_MODE"

    echo "===== END ETL - IMAGE [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1
