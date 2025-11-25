#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/0_setup_env.log"

# define environment mode (as named flags; better than positionals)
# while [[ "$#" -gt 0 ]]; do
#     case $1 in
#         --env) ENV_MODE="$2"; shift ;;
#         --branch) BRANCH="$2"; shift ;;
#         --db) DB="$2"; shift ;;
#         *) echo "Unknown parameter: $1"; exit 1 ;;
#     esac
#     shift
# done

# run setup script and log output
{
    echo ""
    echo "===== START ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ====" 
    echo "--- Installing 'dotenv' ---"
    uv pip install python-dotenv 
    echo ""
    echo "--- Starting 'setup-venv script' ---"
    python3 $ROOT/src/0_setup_venv.py "$@"
    # echo ""
    # echo "--- Starting 'git_auto_pull script' ---"
    # python3 $ROOT/src/0_git_auto_pull.py "$@"
    # echo ""
    echo "--- Starting 'db_check script' ---"
    python3 $ROOT/src/0_db_check.py "$@"
    echo "===== END ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    
} 2>&1 | tee -a "$LOGFILE"

