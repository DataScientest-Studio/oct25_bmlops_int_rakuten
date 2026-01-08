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

# sh = importlib.reload(sh)

def main(env=None):
    env = session.env
    print("Running with env:", env)
    # load env variables from .env and .env.session
    sh.load_env_vars()

    # get input from prompt
    # session.env = env

    # load paths from .env
    sh.get_paths()
    # print("[DEBUG] ROOT loaded =", session.root)
    ROOT = Path(__file__).resolve().parents[2]
    session.root = ROOT

    LOGS = Path(ROOT) / "logs"
    LOGS.mkdir(parents=True, exist_ok=True)

    LOGFILE = LOGS / "0_setup_env_python.log"

    session.save_session()
    
    short = sh.shorten_path(sys.executable, n=3)
    print(f"ℹ️ Using Python interpreter: ../{short}")

    install_packages(env, ROOT, LOGFILE)
    
    print("\nVirtual environment setup complete.")


def install_packages(env, root, logfile):
    # Installing packages
    print("\nInstalling required packages...")

    cmd = ["uv", "sync"]
    # if env == "base":
    #     cmd += ["--group", "base"]
    if env == "+mlops":
        cmd += ["--group", "mlops"]
    elif env == "+dev":
        cmd += ["--group", "dev"]
    elif env == "all":
        cmd += ["--group", "mlops", "--group", "heavy", "--group", "dev"]    
    

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

    print(f"✅ Packages from {env} dependency group installed.")

@click.command()
@click.option("--env", 
              type=click.Choice(["base", "+mlops", "+dev", "all"]), 
              # prompt="Select dependency group",
              required=False, 
              # default=None, 
              show_choices=True
              )
@sh.cli_or_api
def main_entry_check(env):
    main(env)

if __name__ == "__main__":
    main_entry_check()
