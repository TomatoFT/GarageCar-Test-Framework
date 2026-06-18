"""
QA concept: end-to-end critical path — reception → repair → payment.

This is the garage's core business loop in one test.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.payment_page import PaymentCollectPage, PaymentConfirmPage
from pages.reception_page import ReceptionPage
from pages.reception_wizard_page import ReceptionTicketData, ReceptionWizardPage
from pages.repair_page import RepairDetailPage, RepairStartPage, WorkshopPage
from utils.data_loader import load_json
from utils.helpers import unique_license_plate, unique_phone


@pytest.mark.regression
def test_core_garage_flow_reception_to_payment(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    flow = load_json("core_flow.json")
    plate = unique_license_plate()
    labor_amount = flow["labor_rate"]["amount"]
    partial = flow["payment"]["partial_amount"]

    # 1. Reception — intake vehicle
    ReceptionWizardPage(authenticated_page, settings.BASE_URL).open().complete_wizard(
        ReceptionTicketData(
            owner_name=flow["customer"]["owner_name"],
            phone=unique_phone(),
            address=flow["customer"]["address"],
            license_plate=plate,
            brand_name=flow["brand"],
            vehicle_condition=flow["customer"]["vehicle_condition"],
            service_notes=flow["customer"]["service_notes"],
        )
    )
    expect(authenticated_page).to_have_url(re.compile(r"/reception/?$"))
    expect(ReceptionPage(authenticated_page, settings.BASE_URL).tickets_table).to_contain_text(plate)

    # 2. Repair — create order and add labor (creates debt)
    RepairStartPage(authenticated_page, settings.BASE_URL).open().start_repair(plate)
    detail = RepairDetailPage(authenticated_page, settings.BASE_URL)
    order_id = detail.wait_for_order_id_from_url()
    detail.add_labor_line(
        quantity=1,
        description=flow["labor_rate"]["description"],
    )
    expect(detail.line_items_table).to_contain_text(flow["labor_rate"]["description"])

    # 3. Workshop — after labor is added, job moves to "in_progress"
    workshop = WorkshopPage(authenticated_page, settings.BASE_URL).open()
    expect(workshop.column("in_progress")).to_contain_text(plate)

    # 4. Payment — collect partial payment against debt
    vehicle_id = PaymentCollectPage(authenticated_page, settings.BASE_URL).open().select_vehicle_by_plate(
        plate
    )
    PaymentConfirmPage(authenticated_page, settings.BASE_URL).open(vehicle_id).confirm_payment(partial)
    expect(authenticated_page.locator(".alert--success")).to_contain_text("Thanh toán thành công")

    # 5. Verify remaining debt on confirm page reload
    PaymentConfirmPage(authenticated_page, settings.BASE_URL).open(vehicle_id)
    remaining = labor_amount - partial
    expect(authenticated_page.locator(".stat-card__value")).to_contain_text(str(remaining)[:3])
