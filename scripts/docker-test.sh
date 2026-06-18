#!/usr/bin/env bash
# Run the full test stack in Docker (GarageCar + Playwright).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export GARAGE_DIR="${GARAGE_DIR:-$(dirname "$ROOT")/GarageCar}"

if [ ! -f "$GARAGE_DIR/manage.py" ]; then
  echo "GarageCar not found at $GARAGE_DIR"
  echo "Clone it: git clone https://github.com/TomatoFT/GarageCar.git \"$GARAGE_DIR\""
  exit 1
fi

mkdir -p reports
docker compose up --build --abort-on-container-exit tests
docker compose down

echo ""
echo "Report: $ROOT/reports/report.html"
