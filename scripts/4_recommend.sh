#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/4_recommend_cont_RecSys.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
ENV_MODE="${1:-local}"
N_NEIGHBORS="${2:-5}"

# run setup script and log output
{
    echo "===== START RECOMMENDATION [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/4_recommend.py --env "$ENV_MODE" --n_neighbors "$N_NEIGHBORS"

    echo "===== END RECOMMENDATION [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1

