## 0_setup_venv.py
# imports 
from pathlib import Path
import sys

import click

import src.utils.setup_helper as sh 
from src.utils.settings import session


def main(env=None):
    env = session.env
    print("Running with env:", env)

    # load env variables from .env and .env.session
    sh.load_env_vars()

    # load paths from .env and save to .env.session
    sh.get_paths()
    
    ROOT = Path(__file__).resolve().parents[2]
    session.root = ROOT

    LOGS = Path(ROOT) / "logs"
    LOGS.mkdir(parents=True, exist_ok=True)

    LOGFILE = LOGS / "0_setup_env_python.log"

    session.save_session()

    # Show which Python interpreter is being used
    short = sh.shorten_path(sys.executable, n=3)
    print(f"ℹ️ Using Python interpreter: ../{short}")

    # install necessary packages
    sh.install_packages(env, ROOT, LOGFILE)
    
    print("\nVirtual environment setup complete.")


@click.command()
@click.option("--env", 
              type=click.Choice(["base", "+mlops", "+dev", "all"]), 
              required=False, 
              show_choices=True
              )
@sh.cli_or_api
def main_entry_check(env):
    main(env)

if __name__ == "__main__":
    main_entry_check()
