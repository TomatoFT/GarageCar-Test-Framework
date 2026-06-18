"""
QA concept: fixtures for authenticated state, component reuse, navigation.

Uses authenticated_page fixture so tests focus on post-login behavior.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from components.sidebar import Sidebar


@pytest.mark.smoke
def test_dashboard_shows_workshop_stats(authenticated_page: Page) -> None:
    authenticated_page.goto("/dashboard/")

    expect(authenticated_page.locator(".page-header__title")).to_contain_text("Xin chào")
    expect(authenticated_page.locator(".stat-card__label", has_text="Tiếp nhận hôm nay")).to_be_visible()
    expect(authenticated_page.locator(".stat-card__label", has_text="Chờ xử lý")).to_be_visible()
    expect(authenticated_page.get_by_role("link", name="Tiếp nhận xe mới")).to_be_visible()


@pytest.mark.regression
def test_sidebar_navigates_to_reception(authenticated_page: Page) -> None:
    authenticated_page.goto("/dashboard/")
    Sidebar(authenticated_page).go_to_reception()

    expect(authenticated_page).to_have_url(re.compile(r"/reception/?$"))
    expect(authenticated_page.locator(".page-header__title")).to_have_text("Danh sách tiếp nhận")

@pytest.mark.regression
def test_sidebar_navigates_to_workshop(authenticated_page: Page) -> None:
    authenticated_page.goto("/dashboard/")
    Sidebar(authenticated_page).go_to_workshop()

    expect(authenticated_page).to_have_url(re.compile(r"/repairs/workshop/?$"))
    expect(authenticated_page.locator(".page-header__title")).to_have_text("Xưởng sửa chữa")