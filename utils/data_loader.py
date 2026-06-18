import json
from pathlib import Path
from typing import Any

from config import settings


def load_json(filename: str) -> dict[str, Any]:
    path = settings.DATA_DIR / filename
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)
