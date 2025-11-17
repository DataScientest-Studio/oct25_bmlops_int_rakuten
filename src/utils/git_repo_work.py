
import subprocess
from pathlib import Path
import os

from utils.setup_helper import setup_mongodb, load_env_vars()


## 
def git_push_rebase(repo_path, commit_message, branch="main"):
    repo_path = Path(repo_path)

    def run_git(cmd, silent=True):
        """Run git commands safely."""
        return subprocess.run(
            ["git"] + cmd,
            cwd=str(repo_path),
            stdout=(subprocess.DEVNULL if silent else subprocess.PIPE),
            stderr=(subprocess.DEVNULL if silent else subprocess.PIPE),
            text=True,
            check=False
        )

    print("🔍 Staging changes...")
    run_git(["add", "."], silent=True)

    print("📝 Creating commit...")
    commit = run_git(["commit", "-m", commit_message], silent=False)

    if "nothing to commit" in (commit.stdout or ""):
        print("ℹ️  Nothing to commit. Working directory clean.")
    else:
        print("✅ Commit created.")

    print(f"⬆️  Pushing to origin/{branch}...")
    push = run_git(["push", "origin", branch], silent=False)

    if push.returncode == 0:
        print("✅ Push successful.")
        return

    # Handle push failure → Probably non-fast-forward
    print("⚠️ Push rejected. Attempting rebase...")

    # Fetch remote updates
    run_git(["fetch", "origin", branch])

    # Rebase local on remote
    rebase = run_git(["rebase", f"origin/{branch}"], silent=False)

    if rebase.returncode != 0:
        print("❌ Rebase failed. Manual conflict resolution required.")
        return

    print("🔄 Rebase successful. Retrying push...")
    final_push = run_git(["push", "origin", branch], silent=False)

    if final_push.returncode == 0:
        print("🎉 Push after rebase successful.")
    else:
        print("❌ Push failed even after rebase. Manual intervention needed.")

##########

ROOT, DATA, VENV, _ = load_env_vars()

URL_REPO = os.getenv("URL_REPO")
BRANCH = os.getenv("BRANCH")

msg = "Creating necessary folders + files to fulfill requirements of 'phase_1"

git_push_rebase(URL_REPO, commit_message=msg, branch=BRANCH)

