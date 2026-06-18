"""
QA concept: positive vs negative testing, web-first assertions.

- Positive: valid credentials reach the dashboard.
- Negative: invalid credentials stay on login and show a warning.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.login_page import LoginPage
from utils.data_loader import load_json


@pytest.mark.smoke
def test_login_with_valid_credentials(login_page: LoginPage, page: Page) -> None:
    users = load_json("users.json")
    login_page.open().login(users["valid_admin"]["username"], users["valid_admin"]["password"])

    expect(page).to_have_url(f"{settings.BASE_URL}/dashboard/")
    expect(page.locator(".page-header__title")).to_contain_text("Xin chào")


@pytest.mark.smoke
def test_login_with_invalid_password_stays_on_login_page(login_page: LoginPage, page: Page) -> None:
    users = load_json("users.json")
    login_page.open().login(users["invalid"]["username"], users["invalid"]["password"])

    expect(page).to_have_url(re.compile(rf"{re.escape(settings.LOGIN_PATH)}$"))
    expect(page.get_by_role("button", name="Đăng nhập")).to_be_visible()
    expect(page).not_to_have_url(re.compile(r"/dashboard/?$"))
