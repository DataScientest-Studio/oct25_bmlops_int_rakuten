## fastapi/utils.py
# imports
from dotenv import load_dotenv, find_dotenv


## Function to load environment variables from a .env file
def load_env_vars(f_name=".env"):
    """
    Load environment variables from an .env file if available.
    """

    env_path = find_dotenv(filename=f_name)
    if env_path:
        load_dotenv(env_path)
        print(f"Variables from {f_name} loaded")
    
    else:
        print(f"No file '{f_name}' was found")
