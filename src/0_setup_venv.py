## 0_setup_venv.py

# imports 
import os
from pathlib import Path
import subprocess 
import sys
import importlib
import click

import utils.setup_helper as sh 
from utils.settings import session

importlib.reload(sh)

@click.command()
def main():
    # load env variables from .env and .env.session
    sh.load_env_vars()

    # get input from prompt
    ENV = click.prompt("Which packages should be installed?", 
                        type=click.Choice(["core", "+_heavy", "+_dev", "all"]), 
                        default=os.getenv("ENV"),
                        show_choices=True)
    print(f"[INPUT] env = {ENV}")   
    
    
    session.env = ENV

    # load paths from .env
    sh.get_paths()
    # print("[DEBUG] ROOT loaded =", session.root)
    ROOT = session.root

    LOGS = Path(ROOT) / "logs"
    LOGS.mkdir(parents=True, exist_ok=True)

    LOGFILE = LOGS / "0_setup_env_python.log"

    session.save_session()
    
    short = sh.shorten_path(sys.executable, n=3)
    print(f"ℹ️ Using Python interpreter: ../{short}")

    install_packages(ENV, ROOT, LOGFILE)
    
    print("\nVirtual environment setup complete.")


def install_packages(env, root, logfile):
    # Installing packages
    print("\nInstalling required packages...")

    cmd = ["uv", "sync"]
    if env == "+_heavy":
        cmd += ["--group", "heavy"]
    elif env == "+_dev":
        cmd += ["--group", "dev"]
    elif env == "all":
        cmd += ["--group", "heavy", "--group", "dev"]    
    

    # with open(logfile, "a") as log:
    result = subprocess.run(cmd,
                        cwd=str(root), 
                        # stdout=log, #subprocess.DEVNULL,
                        # stderr=log, #subprocess.DEVNULL,
                        check=True
                            )
    if result.returncode != 0:
        print(f"❌ uv sync failed. Check log: {logfile}")
        sys.exit(1)

    print(f"✅ Packages installed ({env}).")



if __name__ == "__main__":
    main()
