#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/0_setup_env.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
ENV_MODE="$1" 

# run setup script and log output
{
    echo ""
    echo "===== START ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ====" 
    echo "--- Starting venv and installing 'dotenv' ---"
    if [ "${ENV_MODE:-local}" != "colab" ]; then 
        source .venv/bin/activate 
    fi

    uv pip install python-dotenv 
    echo ""
    echo "--- Starting 'setup-env script' ---"
    python3 $ROOT/src/0_setup_env.py --env "$ENV_MODE"

    echo "===== END ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} 2>&1 | tee -a "$LOGFILE"

