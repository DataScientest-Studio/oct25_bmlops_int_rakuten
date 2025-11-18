##
# imports 
import os
from pathlib import Path
import subprocess 

from utils.setup_helper import setup_mongodb, load_env_vars

# select environment + load environment variables from .env file
ROOT, DATA, VENV, _ = load_env_vars()

# start venv
try:
    subprocess.run(["source", f"{VENV}/bin/activate"])
    print("✅ Venv was started successfully")
except Exception as e:
    print("❌ Error when activating venv")

# defining paths
DATA_PATH = ROOT / "data"
DATA_PATH.mkdir(parents=True, exist_ok=True)

# repo settings
URL_REPO = os.getenv("URL_REPO")
BRANCH = os.getenv("BRANCH") # or "main"

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
        stderr=subprocess.DEVNULL
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
            stderr=subprocess.DEVNULL
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

print("\nInstalling required packages...")
subprocess.run(
    [str(VENV / "bin" / "pip"), "install", "-r", str(ROOT / "requirements.txt")],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=True
)

print("✅ Packages installed.")
print("\nSetup complete.")

db, collection = setup_mongodb()