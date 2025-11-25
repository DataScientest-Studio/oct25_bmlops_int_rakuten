##
# imports
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def run_git(cmd, cwd, silent=False):
    print(f"[GIT CMD] git {' '.join(cmd)}")
    result = subprocess.run(
        ["git"] + cmd,
        cwd=str(cwd),
        stdout=(sys.stdout if not silent else subprocess.DEVNULL),
        stderr=(sys.stderr if not silent else subprocess.DEVNULL),
        text=True,
        check=False, 
        allow_fail=True      
    )

    output = result.stdout or ""

    if output != "":
        print(result.stdout)
    if output != "":
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed with code {result.returncode}")

    return result

def run_git_capture(cmd, cwd=None):
    print(f"[GIT CMD] git {' '.join(cmd)}")
    result = subprocess.run(
        ["git"] + cmd,
        cwd=str(cwd),
        text=True,
        check=True,
        capture_output=True
    )
    output = result.stdout or ""
    if output != "":
        print(result.stdout)
    if output != "":
        print(result.stderr)

    return result


def auto_detect_tags(files):

    tags = []

    # embeddings
    if any("embed" in f.lower() for f in files):
        tags.append("Embeddings updated")

    # faiss
    if any("faiss" in f.lower() for f in files):
        tags.append("FAISS index updated")

    # etl
    if any("etl" in f.lower() for f in files):
        tags.append("ETL pipeline changed")

    # models
    if any("model" in f.lower() or "checkpoint" in f.lower() for f in files):
        tags.append("Model or checkpoint updated")

    # data
    if any("data" in f.lower() for f in files):
        tags.append("Data files changed")

    # notebooks
    if any(f.endswith(".ipynb") for f in files):
        tags.append("Notebook updates")

    if not tags:
        tags.append("General updates")

    return tags


def create_template_file(repo_path: Path):

    template_path = repo_path / "commit_msg.txt"

    template = (
        "# Write your commit message below.\n"
        "# Lines starting with # will be ignored by git.\n"
        "#\n"
        "# Suggestions based on recent changes:\n"
    )

    # Add auto-detect lines as comments
    auto_msg = generate_auto_message(repo_path)
    if auto_msg:
        for line in auto_msg.splitlines():
            template += f"# {line}\n"
    else:
        template += "# No changes detected OR unable to detect automatically.\n"

    template += "\n"  # blank line where you can write message

    template_path.write_text(template)
    return template_path


def generate_auto_message(repo_path: Path):

    status = run_git(["status", "--porcelain"], cwd=repo_path)
    changed = status.stdout.splitlines()

    # If nothing changed → None
    if not changed:
        return None

    msg = []
    msg.append("Auto-commit:")
    msg.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    msg.append("")  # blank line
    msg.append("Changed files:")

    modified_files = [c[3:] for c in changed]  # "M X.py" → "X.py"

    for f in modified_files:
        msg.append(f" - {f}")

    msg.append("")
    msg.append("Detected changes:")

    # Pattern-based tagging:
    tags = auto_detect_tags(modified_files)
    for t in tags:
        msg.append(f" - {t}")

    return "\n".join(msg)


# ---------------------------------------------------------
# Option A: Automated commit message
# ---------------------------------------------------------
def commit_auto(repo_path: Path):

    msg = generate_auto_message(repo_path)

    if msg is None:
        print("ℹ️  Nothing to commit.")
        return None

    # msg_file = repo_path / "commit_msg_auto.txt"
    # msg_file.write_text(msg)

    return run_git(["commit", "-m", msg], cwd=repo_path)


# ---------------------------------------------------------
# Option B: Commit message from template
# ---------------------------------------------------------
def commit_with_template(repo_path: Path):

    msg_file = create_template_file(repo_path)

    # open in VSCode (blocks until closed)
    subprocess.run(["code", str(msg_file), "--wait"])

    # commit using file
    result = run_git(["commit", "-F", str(msg_file)], cwd=repo_path)
    return result




