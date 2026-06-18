"""
QA concept: Page Object Model reuse — same ReceptionPage used across tests.

Assertions live here; locators and navigation live in pages/reception_page.py.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.reception_page import ReceptionPage


@pytest.mark.regression
def test_reception_list_page_loads(authenticated_page: Page) -> None:
    reception = ReceptionPage(authenticated_page, settings.BASE_URL)
    reception.open()

    expect(reception.page_title).to_have_text("Danh sách tiếp nhận")
    expect(reception.create_ticket_button).to_be_visible()
    expect(reception.tickets_table).to_be_visible()


@pytest.mark.regression
def test_reception_create_link_points_to_wizard(authenticated_page: Page) -> None:
    reception = ReceptionPage(authenticated_page, settings.BASE_URL)
    reception.open()
    reception.create_ticket_button.click()

    expect(authenticated_page).to_have_url(re.compile(r"/reception/create/?$"))
