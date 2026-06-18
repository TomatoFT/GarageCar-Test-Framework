"""
QA concept: dependent workflows — repair requires an existing vehicle from reception.
"""

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.repair_page import RepairDetailPage, RepairStartPage, WorkshopPage
from tests.helpers.garage_flow import create_vehicle_via_reception
from utils.data_loader import load_json
from utils.helpers import unique_license_plate


@pytest.mark.regression
def test_start_repair_and_add_labor_line(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    flow = load_json("core_flow.json")
    plate = create_vehicle_via_reception(authenticated_page)

    RepairStartPage(authenticated_page, settings.BASE_URL).open().start_repair(plate)
    detail = RepairDetailPage(authenticated_page, settings.BASE_URL)
    detail.wait_for_order_id_from_url()

    expect(detail.title).to_contain_text("Phiếu sửa")
    detail.add_labor_line(quantity=1, description=flow["labor_rate"]["description"])

    expect(detail.line_items_table).to_contain_text(flow["labor_rate"]["description"])
    expect(authenticated_page.locator(".page-header__desc")).to_contain_text("đ")


@pytest.mark.regression
def test_workshop_kanban_shows_repair_card(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    plate = create_vehicle_via_reception(authenticated_page)
    RepairStartPage(authenticated_page, settings.BASE_URL).open().start_repair(plate)

    workshop = WorkshopPage(authenticated_page, settings.BASE_URL).open()
    expect(workshop.kanban).to_be_visible()
    expect(workshop.column("pending")).to_contain_text(plate)
