# settings.py
# imports 
import os
from pathlib import Path

class Session:
    def __init__(self):
        self.env = None
        self.branch = None
        self.root = None
        self.data = None
        self.venv = None
        self.url_repo = None

        self.env_loaded = False

    def save_session(self):
        if self.root is None:
            raise RuntimeError("Session.root must be set before saving session.")
        file_path = Path(self.root) / ".env.session"

        state= {
            "SESSION_ENV": self.env if self.env is not None else None,
            "SESSION_BRANCH": self.branch if self.branch is not None else None,
            "SESSION_ROOT": str(self.root) if self.root is not None else None,
            "SESSION_DATA": str(self.data) if self.data is not None else None,
            "SESSION_VENV": str(self.venv) if self.venv is not None else None,
            "SESSION_URL_REPO": self.url_repo if self.url_repo is not None else None,
        }

        with open(file_path, "w") as f:
            for key, value in state.items():
                f.write(f"{key}={value}\n")
    

session = Session()