from dataclasses import dataclass

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


@dataclass
class ReceptionTicketData:
    owner_name: str
    phone: str
    address: str
    license_plate: str
    brand_name: str
    vehicle_condition: str
    service_notes: str


class ReceptionWizardPage(BasePage):
    """Four-step reception wizard at /reception/create/."""

    PATH = "/reception/create/"

    def open(self) -> "ReceptionWizardPage":
        self.goto(self.PATH)
        self.wizard.wait_for(state="visible")
        return self

    @property
    def wizard(self) -> Locator:
        return self.page.locator("#reception-wizard")

    def next_step(self) -> None:
        self.page.get_by_role("button", name="Tiếp theo").click()

    def submit(self) -> None:
        self.page.get_by_role("button", name="Tạo phiếu tiếp nhận").click()

    def _fill(self, field_name: str, value: str) -> None:
        self.wizard.locator(f"[name='{field_name}']").fill(value)

    def complete_wizard(self, data: ReceptionTicketData) -> None:
        self._fill("owner_name", data.owner_name)
        self._fill("phone", data.phone)
        self._fill("address", data.address)
        self.next_step()

        self._fill("license_plate", data.license_plate)
        self.wizard.locator("select[name='brand']").select_option(label=data.brand_name)
        self._fill("vehicle_condition", data.vehicle_condition)
        self.next_step()

        self._fill("service_notes", data.service_notes)
        self.next_step()

        self.submit()
