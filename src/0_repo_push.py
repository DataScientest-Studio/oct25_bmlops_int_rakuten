##
# imports
# import subprocess
from pathlib import Path
import importlib
import os
# from datetime import datetime

import utils.setup_helper as sh
import utils.git_helper as gh 

importlib.reload(sh)
importlib.reload(gh)
 
def main():
    # Configuration
    sh.load_env_vars()

    ROOT = Path(os.getenv("SESSION_ROOT"))
    URL_REPO = os.getenv("SESSION_URL_REPO")
    BRANCH = os.getenv("SESSION_BRANCH")

    repo_path = Path(ROOT)

    args = sh.load_args()

    ensure_branch(BRANCH, repo_path)
    output = stage_commit(args, repo_path, BRANCH)
    if output == "error":
        rebase(BRANCH, repo_path)


def stage_commit(args, repo, branch):
    # Git Workflow
    print("🔍 Staging changes...")
    gh.run_git(["add", "-A"], cwd=repo)

    output = create_commit(args, repo)
    if "nothing to commit" in output:
        print("ℹ️  Nothing to commit. Working directory clean.")
        return "commit"

    else:
        print("✅ Commit created.")
        status = gh.run_git_capture(["status", "--porcelain"], cwd=repo)
        if status.stdout:
            print("⚠️ Detected uncommitted changes. Staging all...")
            gh.run_git(["add", "-A"], cwd=repo)
            output = create_commit(args, repo)

        print("🔁 Pulling latest changes (rebase)...")
        gh.run_git(["pull", "--rebase", "origin", branch], cwd=repo)

        print(f"⬆️  Pushing to origin/{branch}...")
        push = gh.run_git(["push", "--set-upstream", "origin", branch], cwd=repo)

        if push.returncode == 0:
            print("✅ Push successful.")
            return "pushed"
        else: 
            return "error"

def rebase(branch, repo):
    # Push failed → Rebase logic
    print("⚠️ Push rejected. Attempting rebase...")

    # Fetch remote updates
    gh.run_git(["fetch", "origin", branch], cwd=repo)

    # Rebase local on remote
    rebase = gh.run_git(["rebase", f"origin/{branch}"], cwd=repo)

    if rebase.returncode != 0:
        print("❌ Rebase failed. Manual conflict resolution required.")
        exit(1)

    print("🔄 Rebase successful. Retrying push...")
    final_push = gh.run_git(["push", "origin", branch], cwd=repo)

    if final_push.returncode == 0:
        print("🎉 Push after rebase successful.")
    else:
        print("❌ Push failed even after rebase.")


def ensure_branch(branch, repo):
    print(f"Ensuring branch '{branch}' exists...")

    local = branch_exists_local(branch, repo)
    remote = branch_exists_remote(branch, repo)

    if local:
        print(f"✔ Branch '{branch}' exists locally.")
        gh.run_git(["checkout", branch], cwd=repo)
        return

    if remote:
        print(f"✔ Branch '{branch}' exists on remote. Creating local tracking branch.")
        gh.run_git(["checkout", "-b", branch, f"origin/{branch}"], cwd=repo)
        return

    print(f"✔ Branch '{branch}' does not exist. Creating new branch.")
    gh.run_git(["checkout", "-b", branch], cwd=repo)


def branch_exists_local(branch, repo):
    result = gh.run_git_capture(["branch", "--list", branch], 
                        cwd=repo)
    
    return branch in result.stdout


def branch_exists_remote(branch, repo):
    result = gh.run_git_capture(["git", "ls-remote", "--heads", "origin", branch], 
                        cwd=repo)
    output = result.stdout or ""
    return bool(output.strip())


def create_commit(args, repo):
    print("📝 Creating commit...")
    if args.msg == "auto": # or (args.msg is None):
        commit = gh.commit_auto(repo)
        # commit_msg = f"Auto-commit ({datetime.now().isoformat(timespec='seconds')})" # : Several minor improvements, no major change 
        # commit = run_git(["commit", "-m", commit_msg], cwd=repo_path, silent=False)

    elif args.msg == "tmp":
        commit = gh.commit_with_template(repo)
        # commit_msg = args.msg # run_git(["commit"])
        # commit = run_git(["commit", "-m", args.msg], cwd=repo_path, silent=False)

    else:
        commit = gh.run_git(["commit"], cwd=repo, silent=False)
        # commit_msg = "Auto-commit"
        # print(f"❌ no valid value for '--msg'")
    
    output = commit.stdout or ""
    return output

if __name__ == "__main__":
    main()


