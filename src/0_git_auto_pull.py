## 0_git_pull.py

# imports 
import os
import sys
import click
import importlib
# import subprocess

import utils.setup_helper as sh 
import utils.git_helper as gh 
from utils.settings import session

importlib.reload(sh)
importlib.reload(gh)

@click.command()
def main():
    # load env variables from .env and .env.session
    sh.load_env_vars()
    sh.get_paths()

    ROOT = session.root
    URL_REPO = os.getenv("URL_REPO")

    # configuration
    BRANCH = click.prompt("Enter branch name", 
                            type=str, 
                            default=os.getenv("BRANCH"))
    
    print(f"[INPUT] branch = {BRANCH}")

    session.branch = BRANCH
    session.save_session()

    # workflow
    demand = pre_repo_check(ROOT, BRANCH)
    if demand == None:
        print("--> Repo cannot be cloned or pulled.")

    else:
        if demand == "clone":
            clone_repo(BRANCH, URL_REPO, ROOT)
        elif demand == "pull":
            pull_repo(ROOT)
        
        post_repo_check(ROOT)
    
    
def pre_repo_check(root, branch_expected):
    #print("\n🔍 Running safety checks...\n")
    print(f"\n{'='*10} PRE-FETCH CHECK {'='*10}\n")

    # check local branch
    git_dir = root / ".git"
    if not git_dir.exists():
        print("Repo not found → need to clone.")
        return "clone"

    # local branch + check vs. expected branch
    branch_loc = show_local_branch(root)

    print(f"[BRANCH] Local: {branch_loc}")
    print(f"[BRANCH] Expected: {branch_expected}")
    if branch_loc != branch_expected:
        print("❌ Local branch does not match expected branch.")
        print(f"👉 Run: git checkout {branch_expected}")
        print("   or adjust your BRANCH env / CLI argument.")
        # sys.exit(1)
        return None

    else:
        # checking tracking branch
        check_tracking(root)

        # check status of commits and ahead/behind
        check_result = check_commits(root)
        print("\n✅ PRE-FETCH CHECK COMPLETED")

        if check_result:
            return "pull"
        else:
            return None
        

def show_local_branch(root):
    result = gh.run_git_capture(["branch", "--show-current"], 
                                    cwd=root)
    # branch_loc = branch_loc_res.stdout.strip()
   

    if result.returncode != 0:
        print("❌ Cannot determine local branch.")
        return None

    branch_loc = (result.stdout or "").strip()

    if not branch_loc:
        print("❌ No branch checked out (detached HEAD?).")
        return None
    
    return branch_loc


def check_tracking(root):
    try:
        # checking tracking branch
        return_code, tracking = has_upstream(root)
        
        if return_code != 0: #  or not branch_track:
            print("❌ No tracking/upstream branch set! Cannot pull safely.")
            print("👉 Fix with:")
            print("   git branch --set-upstream-to=origin/<branch> <branch>")
            return None

        branch_track = tracking.stdout.strip()
        
        # if branch_track is None:
        #     print("❌ Cannot pull — no upstream branch configured.")
        #     sys.exit(1)

        print(f"[BRANCH] Tracking: {branch_track}")
        return branch_track

    except Exception as e:
        print(f"❌ Error occured: {e}")
        return None

def check_commits(root):
    # checking tracking branch
    return_code, _ = has_upstream(root)
        
    if return_code != 0:
        print("❌ Cannot check commits — no upstream set.")
        return None
    
    # check for uncommitted changes 
    status = gh.run_git_capture(["status", "--porcelain"], cwd=root).stdout.strip()
    if status:
        print("⚠️  Uncommitted changes detected:")
        print(status)
        print("👉 Commit or stash before pulling.")
        return None 
        # sys.exit(1)
    else:
        print("[STATUS] No local changes.")
        

    # ahead/behind check
    try:
        ahead_behind = gh.run_git_capture(
            ["rev-list", "--left-right", "--count", "HEAD...@{u}"],
            cwd=root
        ).stdout.strip()

        ahead, behind = map(int, ahead_behind.split())
        print(f"[SYNC] Ahead: {ahead}, Behind: {behind}")

        if ahead > 0 and behind > 0:
            print("🚨 Divergent history detected — cannot pull safely!")
            return None 
            # sys.exit(1)

    except Exception as e:
        print(f"❌ Error occured: {e}")
        return None 


def clone_repo(branch, repo_url, root):
    print(f"🔄 Cloning repository from '{branch}'...")
    gh.run_git(
            ["clone", 
             "-b", 
             branch, 
             repo_url, 
             str(root)], 
             cwd=root.parent
            )
    print("✅ CLONING successful")


def pull_repo(root):
    print("🔄 Pulling latest changes...")
    gh.run_git(["pull", "--rebase"], cwd=root)  # "-C", str(root), 
    print("✅ Repo updated.")


def post_repo_check(root):
    print(f"\n{'='*10} POST-FETCH CHECK {'='*10}")   #
    gh.run_git(
        ["ls", "-l", str(root)], cwd=root)
    print("\n✅ POST-FETCH CHECK COMPLETED")


def has_upstream(root):
    """Return True if the current branch has an upstream."""
    res = gh.run_git_capture(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=root
    )
    return res.returncode, res


if __name__ == "__main__":
    main()



    # git_dir = root / ".git"

    # if not git_dir.exists():
    #     # Clone repository
    #     
    
    # # Fetch and update repository
    # print("🔍 Repository found, checking for updates...")
    # status = subprocess.run(
    #         ["git", "-C", str(root), "status", "-uno"], 
    #         capture_output=True,
    #         check=True,
    #         text=True,
    #                     )

    # if "behind" in status.stdout and "modified" not in status.stdout:
    #     print(f"🔄 Pulling updates from {branch}...")
    #     subprocess.run(["git", "-C", str(root), "pull"], check=True)
    #     print("✅ Update complete")
            
    # else:
    #     