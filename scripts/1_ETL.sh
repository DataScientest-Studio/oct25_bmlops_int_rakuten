#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/1_etl.log"

# run etl scripts (text + image) and log output
{
    echo "===== START ETL - TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/1_etl_text.py

    echo "===== END ETL - TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1

{
    echo "===== START ETL - IMAGE [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/1_etl_image.py

    echo "===== END ETL - IMAGE [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1
