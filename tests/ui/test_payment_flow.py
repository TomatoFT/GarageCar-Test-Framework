"""
QA concept: business-rule validation — payment amount cannot exceed vehicle debt.
"""

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.payment_page import PaymentConfirmPage
from tests.helpers.garage_flow import create_vehicle_with_debt, open_payment_confirm_for_plate
from utils.data_loader import load_json


@pytest.mark.regression
def test_collect_and_confirm_partial_payment(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    flow = load_json("core_flow.json")
    plate, labor_amount = create_vehicle_with_debt(authenticated_page)
    partial = flow["payment"]["partial_amount"]
    assert partial <= labor_amount

    vehicle_id = open_payment_confirm_for_plate(authenticated_page, plate)
    confirm = PaymentConfirmPage(authenticated_page, settings.BASE_URL).open(vehicle_id)
    expect(confirm.debt_display).to_contain_text(str(labor_amount)[:3])

    confirm.confirm_payment(partial)
    expect(authenticated_page.locator(".alert--success")).to_contain_text("Thanh toán thành công")
