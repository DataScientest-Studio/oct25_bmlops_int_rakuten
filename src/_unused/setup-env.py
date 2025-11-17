## clone Git repo (or update loacl version)
import os
from pathlib import Path
import subprocess

PROJECT_ROOT = Path("/home/robfra/0_Portfolio_Projekte/Rakuten_Classification")
DATA = Path("/mnt/chromeos/GoogleDrive/MyDrive/1_Projekte_Datensätze/1_Projekte/2_Rakuten_Classification/data")      # local path on my Chromebook
# ROOT = Path("/content/drive/MyDrive/1_Projekte_Datensätze/1_Projekte/2_Rakuten_Classification")               # path for Google Colab
URL_REPO = "https://github.com/DataScientest-Studio/oct25_bmlops_int_rakuten.git"
BRANCH = "phase_1"

DATA.mkdir(parents=True, exist_ok=True)
# REPO_FOLDER = PROJECT_ROOT / "oct25_bmlops_int_rakuten"

if not (PROJECT_ROOT / ".git").exists():
    # Clone repository
    print("🔄 Cloning repository...")
    subprocess.run(
        ["git", "clone", "-b", BRANCH, "--single-branch", URL_REPO, str(PROJECT_ROOT)],
        check=True,
    )
    print("✅ CLONING successful")
else:
    # Fetch and update repository
    print("🔍 Repository found, checking for updates...")
    subprocess.run(["git", "-C", str(PROJECT_ROOT), "fetch"], check=True)
    result = subprocess.run(
        ["git", "-C", str(PROJECT_ROOT), "status", "-uno"],
        capture_output=True,
        text=True
    )
    if "Your branch is behind" in result.stdout:
        subprocess.run(["git", "-C", str(PROJECT_ROOT), "pull"], check=True)
        print("✅ UPDATE successful")
    else:
        print("✅ No update necessary")

print(f"\n{'='*30}\n--- CHECK 'GIT_FOLDER' ---\n{'='*30}")   #
!ls -l {REPO_FOLDER}
# print(f"{'='*30}\n--- SHAPE ---\n{'='*30}\n")
# print(df_good_bad.shape)

print("\nInstalling required packages...")
# !source {}
print("\nSetup complete.")