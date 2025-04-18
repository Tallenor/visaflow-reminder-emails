from src.config import ENV_CONFIG


XATA_API_KEY = ENV_CONFIG["XATA_API_KEY"]
XATA_DATABASE_URL = ENV_CONFIG["XATA_DATABASE_URL"]
XATA_BRANCH = ENV_CONFIG["XATA_BRANCH"]
BREVO_EMAIL_API_KEY = ENV_CONFIG["BREVO_EMAIL_API_KEY"]

DB_URL = f"{XATA_DATABASE_URL}:{XATA_BRANCH}"
