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

    def save_session(self):
        if self.root is None:
            raise RuntimeError("Session.root must be set before saving session.")
        file_path = Path(self.root) / ".env.session"

        state= {
            "SESSION_ENV": self.env or "",
            "SESSION_BRANCH": self.branch or "",
            "SESSION_ROOT": str(self.root or ""),
            "SESSION_DATA": str(self.data or ""),
            "SESSION_VENV": str(self.venv or ""),
            "SESSION_URL_REPO": self.url_repo or "",
        }

        with open(file_path, "w") as f:
            for key, value in state.items():
                f.write(f"{key}={value}\n")
    

session = Session()