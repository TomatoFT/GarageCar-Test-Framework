"""Reusable UI flows for tests (Arrange helpers)."""

from playwright.sync_api import Page

from config import settings
from pages.payment_page import PaymentCollectPage
from pages.reception_wizard_page import ReceptionTicketData, ReceptionWizardPage
from pages.repair_page import RepairDetailPage, RepairStartPage
from utils.data_loader import load_json
from utils.helpers import unique_license_plate, unique_phone


def create_vehicle_via_reception(page: Page, plate: str | None = None) -> str:
    """Run the reception wizard; return the license plate used."""
    flow = load_json("core_flow.json")
    plate = plate or unique_license_plate()

    ReceptionWizardPage(page, settings.BASE_URL).open().complete_wizard(
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
    return plate


def create_vehicle_with_debt(page: Page) -> tuple[str, int]:
    """Reception + repair with labor → returns (plate, debt amount)."""
    flow = load_json("core_flow.json")
    plate = create_vehicle_via_reception(page)

    RepairStartPage(page, settings.BASE_URL).open().start_repair(plate)
    detail = RepairDetailPage(page, settings.BASE_URL)
    detail.wait_for_order_id_from_url()
    detail.add_labor_line(quantity=1, description=flow["labor_rate"]["description"])

    return plate, flow["labor_rate"]["amount"]


def open_payment_confirm_for_plate(page: Page, plate: str) -> int:
    return PaymentCollectPage(page, settings.BASE_URL).open().select_vehicle_by_plate(plate)
