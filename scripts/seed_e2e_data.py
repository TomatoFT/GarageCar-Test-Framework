#!/usr/bin/env python3
"""CLI wrapper — run: python scripts/seed_e2e_data.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.garage_seed import seed_e2e_data

if __name__ == "__main__":
    seed_e2e_data()
    print("E2E seed complete")
