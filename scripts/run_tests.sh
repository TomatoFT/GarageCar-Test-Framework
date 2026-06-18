#!/usr/bin/env bash
# Wait for GarageCar then run pytest with sensible defaults.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

source .venv/bin/activate 2>/dev/null || {
  echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && playwright install"
  exit 1
}

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
LOGIN_PATH="${LOGIN_PATH:-/login/}"

python -c "from utils.helpers import wait_for_server; wait_for_server('${BASE_URL}${LOGIN_PATH}')"

MARKERS="${1:--m smoke}"
shift || true
pytest $MARKERS "$@"
