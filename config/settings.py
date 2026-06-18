"""Central config for the test framework. Values come from .env or defaults."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/login/")
DEMO_USERNAME = os.getenv("DEMO_USERNAME", "opera")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "1")

DATA_DIR = ROOT_DIR / "data"
BASELINES_DIR = ROOT_DIR / "baselines"
REPORTS_DIR = ROOT_DIR / "reports"
AUTH_DIR = ROOT_DIR / ".auth"
AUTH_STORAGE = AUTH_DIR / "storage.json"

GARAGE_DIR = Path(os.getenv("GARAGE_DIR", Path.home() / "GarageCar"))
