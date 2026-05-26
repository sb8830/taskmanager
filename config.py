import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import streamlit as st
except Exception:
    st = None

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def get_setting(key: str, default=None):
    """Read config from Streamlit Cloud secrets first, then environment, then default."""
    if st is not None:
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
    return os.getenv(key, default)

DATABASE_URL = get_setting("DATABASE_URL", "sqlite:///taskflow.db")
SECRET_KEY = get_setting("SECRET_KEY", "taskflow-secret-change-me")
APP_ENV = get_setting("APP_ENV", "production")

UPLOAD_FOLDER = BASE_DIR / "uploads"
REPORT_FOLDER = BASE_DIR / "reports"
LOG_FOLDER = BASE_DIR / "logs"

SESSION_TIMEOUT_MINUTES = int(get_setting("SESSION_TIMEOUT_MINUTES", 30))
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "xlsx", "csv", "docx", "txt"}
MAX_UPLOAD_MB = int(get_setting("MAX_UPLOAD_MB", 20))

SMTP_HOST = get_setting("SMTP_HOST", "")
SMTP_PORT = int(get_setting("SMTP_PORT", 587))
SMTP_USER = get_setting("SMTP_USER", "")
SMTP_PASSWORD = get_setting("SMTP_PASSWORD", "")
SMTP_FROM = get_setting("SMTP_FROM", SMTP_USER)

ADMIN_EMAIL = get_setting("ADMIN_EMAIL", "admin@taskflow.com")
ADMIN_PASSWORD = get_setting("ADMIN_PASSWORD", "Admin@123")
AGENT_EMAIL = get_setting("AGENT_EMAIL", "agent@taskflow.com")
AGENT_PASSWORD = get_setting("AGENT_PASSWORD", "Agent@123")

for folder in [UPLOAD_FOLDER, REPORT_FOLDER, LOG_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)
