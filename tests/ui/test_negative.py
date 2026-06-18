"""
QA concept: negative testing — business rules and validation boundaries.

These tests verify the app rejects invalid input, not just happy paths.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.payment_page import PaymentConfirmPage
from pages.reception_wizard_page import ReceptionTicketData, ReceptionWizardPage
from pages.repair_page import RepairStartPage
from tests.helpers.garage_flow import create_vehicle_via_reception, create_vehicle_with_debt, open_payment_confirm_for_plate
from utils.data_loader import load_json
from utils.garage_seed import reset_daily_reception_limit, set_daily_reception_limit
from utils.helpers import unique_license_plate, unique_phone


@pytest.mark.negative
@pytest.mark.regression
def test_repair_start_with_unknown_plate_fails(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    RepairStartPage(authenticated_page, settings.BASE_URL).open().start_repair("ZZ-UNKNOWN-999")

    expect(authenticated_page).to_have_url(re.compile(r"/repairs/start/?$"))
    expect(authenticated_page.locator("body")).to_contain_text("404")


@pytest.mark.negative
@pytest.mark.regression
def test_payment_exceeding_debt_shows_warning(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    plate, debt = create_vehicle_with_debt(authenticated_page)
    vehicle_id = open_payment_confirm_for_plate(authenticated_page, plate)

    PaymentConfirmPage(authenticated_page, settings.BASE_URL).open(vehicle_id).confirm_payment(
        debt + 50_000
    )

    expect(authenticated_page.locator(".alert--warning")).to_contain_text(
        "Số tiền nhập không hợp lệ"
    )


@pytest.mark.negative
@pytest.mark.regression
def test_reception_blocked_when_daily_limit_reached(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    flow = load_json("core_flow.json")
    first_plate = create_vehicle_via_reception(authenticated_page)

    set_daily_reception_limit(1)

    try:
        ReceptionWizardPage(authenticated_page, settings.BASE_URL).open().complete_wizard(
            ReceptionTicketData(
                owner_name=flow["customer"]["owner_name"],
                phone=unique_phone(),
                address=flow["customer"]["address"],
                license_plate=unique_license_plate(),
                brand_name=flow["brand"],
                vehicle_condition=flow["customer"]["vehicle_condition"],
                service_notes=flow["customer"]["service_notes"],
            )
        )

        expect(authenticated_page).to_have_url(re.compile(r"/reception/create/?$"))
        expect(authenticated_page.locator(".alert--warning")).to_contain_text(
            "Đã quá hạn số lượng tiếp nhận"
        )
    finally:
        reset_daily_reception_limit()

    authenticated_page.goto(f"{settings.BASE_URL}/reception/")
    expect(authenticated_page.locator("table.data-table")).to_contain_text(first_plate)
