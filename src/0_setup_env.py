##
# imports 
import os
from pathlib import Path
import subprocess 
import sys
from datetime import datetime

from utils.setup_helper import load_env_vars

# select environment + load environment variables from .env file
ROOT, DATA, VENV, args = load_env_vars()

LOGS = ROOT / "logs" 
LOGFILE = LOGS / "0_setup_env_python.log"


# defining paths
DATA_PATH = ROOT / "data"
DATA_PATH.mkdir(parents=True, exist_ok=True)

# repo settings
URL_REPO = os.getenv("URL_REPO")
BRANCH = os.getenv("BRANCH") # or "main"

print(f"ℹ️ Using Python interpreter: {sys.executable}")

# Installing packages
print("\nInstalling required packages...")
if args.env == "colab":
    cmd = ["uv", "sync", "--group", "heavy", "--group", "dev"]
    
elif args.env == "dev":
    cmd = ["uv", "sync", "--group", "dev"]
    
else:
    cmd = ["uv", "sync"]
 
with open(LOGFILE, "a") as log:
    try:
        subprocess.run(cmd,
                       cwd=str(ROOT), 
                        stdout=log, #subprocess.DEVNULL,
                        stderr=log, #subprocess.DEVNULL,
                        check=True
                        )
    except subprocess.CalledProcessError as e:
        print(f"❌ [{datetime.now()}] uv sync failed (exit code {e.returncode}).")
        print("⚠️ Check pyproject.toml dependency groups or conflicting versions.\n")
        sys.exit(1)

print(f"✅ Packages installed ({args.env}).")

from utils.setup_helper import setup_mongodb

## clone Git repo (or update existing version)
if not (ROOT / ".git").exists():
    # Clone repository
    print("🔄 Cloning repository...")
    subprocess.run(
        ["git", "clone", "-b", BRANCH, "--single-branch", URL_REPO, str(ROOT)],
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
        check=True,
    )
    print("✅ CLONING successful")
else:
    # Fetch and update repository
    print("🔍 Repository found, checking for updates...")
    subprocess.run(
        ["git", "-C", str(ROOT), "fetch"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
        check=True)
    
    result = subprocess.run(
        ["git", "-C", str(ROOT), "status", "-uno"],
        capture_output=True,
        text=True
    )
    if "behind" in result.stdout:
        subprocess.run(
            ["git", "-C", str(ROOT), "pull"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            check=True)
        
        print("✅ UPDATE successful")
    else:
        print("✅ No update necessary")

print(f"\n{'='*30}\n--- CHECK 'REPO' ---\n{'='*30}")   #
subprocess.run(
    ["ls", "-l", str(ROOT)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=True
        )

# print(f"{'='*30}\n--- SHAPE ---\n{'='*30}\n")
# print(df_good_bad.shape)

print("\nSetup complete.")

coll_dict = setup_mongodb(verbose=True)
# db = coll_dict.keys()
# collection = coll_dict.values()