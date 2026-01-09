#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/3_data_sample_split.log"


# define environment mode
MODE="${1}"
NUM="${2}"

# run etl scripts (text + image) and log output

if [ $MODE == "split" ]; then 
    {
        echo "===== START DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

        python3 $ROOT/src/3_data_sample_split.py --mode $MODE="split"

        echo "===== END DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
        echo ""
    } >> "$LOGFILE" 2>&1

elif [ $MODE == "sample" ]; then
    {
        echo "===== START DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

        python3 $ROOT/src/3_data_sample_split.py --mode $MODE="split"

        echo "===== END DATA SPLIT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
        echo ""
    } >> "$LOGFILE" 2>&1