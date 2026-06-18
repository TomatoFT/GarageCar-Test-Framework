"""Idempotent seed and rule helpers via GarageCar Django shell."""

from __future__ import annotations

import subprocess
import sys

from config import settings


def _run_shell(code: str) -> None:
    garage_dir = settings.GARAGE_DIR
    if not (garage_dir / "manage.py").exists():
        raise FileNotFoundError(f"GarageCar not found at {garage_dir}")

    python = garage_dir / ".venv" / "bin" / "python"
    if not python.exists():
        python = sys.executable

    subprocess.run(
        [str(python), "manage.py", "shell", "-c", code],
        cwd=garage_dir,
        check=True,
        capture_output=True,
        text=True,
    )


def seed_e2e_data() -> None:
    _run_shell(
        """
from apps.customers.models import VehicleBrand
from apps.repairs.models import LaborRate

VehicleBrand.objects.get_or_create(name="Toyota")
LaborRate.objects.get_or_create(name="Thay dau", defaults={"amount": 200000})
"""
    )


def set_daily_reception_limit(limit: int) -> None:
    _run_shell(
        f"""
from apps.core.models import BusinessRule, RuleKey

rule, _ = BusinessRule.objects.get_or_create(
    key=RuleKey.MAX_DAILY_RECEPTIONS,
    defaults={{"name": "So xe sua chua toi da", "value": {limit}}},
)
rule.value = {limit}
rule.save()
"""
    )


def reset_daily_reception_limit() -> None:
    set_daily_reception_limit(0)
