"""
QA concept: multi-step form (wizard) — navigate panels, validate, submit.

Requires garage_prerequisites (Toyota brand in DB).
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages.reception_page import ReceptionPage
from pages.reception_wizard_page import ReceptionTicketData, ReceptionWizardPage
from utils.data_loader import load_json
from utils.helpers import unique_license_plate, unique_phone


@pytest.mark.regression
def test_reception_wizard_creates_ticket(
    garage_prerequisites: None,
    authenticated_page: Page,
) -> None:
    flow = load_json("core_flow.json")
    plate = unique_license_plate()

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
