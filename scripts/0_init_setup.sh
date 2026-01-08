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
    echo "--- Starting 'setup-venv script' ---"
    python3 $ROOT/src/0_setup_venv.py "$@"
    echo "
    echo "===== END ENV_SETUP [$(date '+%Y-%m-%d %H:%M:%S')] ===="
    
} 2>&1 | tee -a "$LOGFILE"

