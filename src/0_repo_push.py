##
# imports
import subprocess
from pathlib import Path
import os
from datetime import datetime

from utils.setup_helper import setup_mongodb, load_env_vars
from utils.git_helper import run_git, commit_auto, commit_with_template

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------
ROOT, DATA, VENV, args = load_env_vars()

URL_REPO = os.getenv("URL_REPO")
BRANCH = os.getenv("BRANCH")

repo_path = Path(ROOT)

# ----------------------------------------------------------
# Commit Message
# ----------------------------------------------------------


# ----------------------------------------------------------
# Git Workflow
# ----------------------------------------------------------
print("🔍 Staging changes...")
run_git(["add", "."], cwd=repo_path)

print("📝 Creating commit...")
if args.msg == "auto": # or (args.msg is None):
    commit = commit_auto(repo_path)
    # commit_msg = f"Auto-commit ({datetime.now().isoformat(timespec='seconds')})" # : Several minor improvements, no major change 
    # commit = run_git(["commit", "-m", commit_msg], cwd=repo_path, silent=False)

elif args.msg == "tmp":
    commit = commit_with_template(repo_path)
    # commit_msg = args.msg # run_git(["commit"])
    # commit = run_git(["commit", "-m", args.msg], cwd=repo_path, silent=False)

else:
    commit = run_git(["commit"], cwd=repo_path, silent=False)
    # commit_msg = "Auto-commit"
    # print(f"❌ no valid value for '--msg'")

# commit = run_git(["commit", "-m", commit_msg], cwd=repo_path)

if "nothing to commit" in commit.stdout: # or ""):
    print("ℹ️  Nothing to commit. Working directory clean.")
    exit(0)

print("✅ Commit created.")

print(f"⬆️  Pushing to origin/{BRANCH}...")
push = run_git(["push", "origin", BRANCH], cwd=repo_path)

if push.returncode == 0:
    print("✅ Push successful.")
    exit(0)

# ----------------------------------------------------------
# Push failed → Rebase logic
# ----------------------------------------------------------
print("⚠️ Push rejected. Attempting rebase...")

# Fetch remote updates
run_git(["fetch", "origin", BRANCH], cwd=repo_path)

# Rebase local on remote
rebase = run_git(["rebase", f"origin/{BRANCH}"], cwd=repo_path)

if rebase.returncode != 0:
    print("❌ Rebase failed. Manual conflict resolution required.")
    exit(1)

print("🔄 Rebase successful. Retrying push...")
final_push = run_git(["push", "origin", BRANCH], cwd=repo_path)

if final_push.returncode == 0:
    print("🎉 Push after rebase successful.")
else:
    print("❌ Push failed even after rebase.")

##########


