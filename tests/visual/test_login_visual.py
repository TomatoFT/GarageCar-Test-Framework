"""
QA concept: visual regression — catch unintended UI changes.

First run:  pytest tests/visual/ --update-baselines
Later runs:  pytest -m visual
"""

import pytest
from playwright.sync_api import Page

from config import settings
from pages.login_page import LoginPage
from utils.visual import images_within_tolerance


@pytest.mark.visual
def test_login_page_matches_baseline(
    login_page: LoginPage,
    page: Page,
    pytestconfig: pytest.Config,
) -> None:
    login_page.open()
    page.wait_for_load_state("networkidle")

    card = page.locator(".login-card")
    actual = card.screenshot()

    baseline = settings.BASELINES_DIR / "login-card.png"

    if pytestconfig.getoption("--update-baselines"):
        baseline.parent.mkdir(parents=True, exist_ok=True)
        baseline.write_bytes(actual)
        return

    assert baseline.exists(), (
        f"Baseline not found at {baseline}. "
        "Run: pytest tests/visual/ --update-baselines"
    )

    expected = baseline.read_bytes()
    if not images_within_tolerance(actual, expected):
        settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        (settings.REPORTS_DIR / "login-card-actual.png").write_bytes(actual)
        pytest.fail(
            "Login card screenshot differs from baseline. "
            "See reports/login-card-actual.png"
        )
