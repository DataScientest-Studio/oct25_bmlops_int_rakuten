#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/2_preprocess.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
ENV_MODE="${1:-local}"

# run setup script and log output
{
    echo "===== START EMBEDDING TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/2_embed_text.py 

    echo "===== END EMBEDDING TEXT [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
    echo "===== START EMBEDDING IMAGES [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 $ROOT/src/2_embed_text.py 

    echo "===== END EMBEDDING IMAGES [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
    
} >> "$LOGFILE" 2>&1