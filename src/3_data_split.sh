#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/3_data_split.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
# ENV_MODE="${1:-local}"

# run etl scripts (text + image) and log output
{
    echo "===== START DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/3_data_split.py

    echo "===== END DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1

