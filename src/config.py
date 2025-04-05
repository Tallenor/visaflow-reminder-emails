import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

ENV_VARS = {
    "PROD": None,
    "XATA_BRANCH": None,
    "XATA_API_KEY": None,
    "XATA_DATABASE_URL": None,
    "BREVO_EMAIL_API_KEY": None
}

def validate_env_vars():
    """
    Validate that all required environment variables are set.
    """
    missing_keys = [key for key in ENV_VARS.keys() if os.getenv(key) is None]
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")


def get_env_vars():
    """
    Get all environment variables.
    """
    for key in ENV_VARS.keys():
        ENV_VARS[key] = os.getenv(key)
    return ENV_VARS


# Validate environment variables on import
validate_env_vars()

# Get environment variables
ENV_CONFIG = get_env_vars()

BASE_DIR = Path(__file__).parent.parent


# Set PROD environment variable
PROD = True if ENV_CONFIG["PROD"] == "True"  else False
