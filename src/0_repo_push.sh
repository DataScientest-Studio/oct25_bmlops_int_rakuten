#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/0_repo_push.log"

# load environment variables from .env file if it exists
# if [ -f "$ROOT/.env" ]; then
#     set -o allexport
#     source .env
#     set +o allexport
# fi 

# define environment mode
# ENV_MODE="${1:-local}"
MSG="${1}"

# run setup script and log output
{
    echo "===== START REPO PUSH [$(date '+%Y-%m-%d %H:%M:%S')] ====" 

    python3 -u $ROOT/src/0_repo_push.py --msg "$MSG"

    echo "===== END REPO PUSH [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    echo ""
} >> "$LOGFILE" 2>&1

