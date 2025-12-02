#!/usr/bin/env bash

# exit on error
set -e

# define paths
ROOT="$(cd "$(dirname "$0")/.." && pwd)" 

mkdir -p "$ROOT/logs"
LOGFILE="$ROOT/logs/0_setup_env.log"

# run setup script and log output
{
    echo ""
    echo "===== START ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ====" 
    echo "--- Installing 'dotenv' ---"
    uv pip install python-dotenv 
    echo ""
    echo "--- Starting 'setup-venv script' ---"
    python3 $ROOT/src/0_setup_venv.py "$@"
    echo ""
    echo "--- Starting 'git_auto_pull script' ---"
    python3 $ROOT/src/0_git_auto_pull.py "$@"
    echo ""
    echo "--- Starting 'db_check script' ---"
    python3 $ROOT/src/0_db_check.py "$@"
    echo "===== END ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    
} 2>&1 | tee -a "$LOGFILE"

