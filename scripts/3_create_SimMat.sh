#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/3_sm_cont.log"

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
    echo "===== START CREATING SIMILARITY MATRICES [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/2_embed_text.py --env "${ENV_MODE}" --n_neighbors "${N_NEIGHBORS}"

    echo "===== END CREATING SIMILARITY MATRICES [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
    
} >> "$LOGFILE" 2>&1