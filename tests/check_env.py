# tests/check_env.py
import os, sys

# logging ergänzen


required = [
    "APP_ENV",
    "SECRET_KEY",
    "API_TOKEN",
]

missing = [k for k in required if k not in os.environ]

if missing:
    print("Missing ENV vars:", missing)
    sys.exit(1)
