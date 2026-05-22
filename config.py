import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
UPLOAD_DIR = BASE_DIR / "uploads"
USERS_FILE = BASE_DIR / "users.txt"
TEMPLATES_DIR = BASE_DIR / "templates"

SECRET_KEY = os.getenv("SECRET_KEY", "lab6-dev-secret-change-in-production")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "lab6_auth")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
