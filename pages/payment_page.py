import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class PaymentCollectPage(BasePage):
    PATH = "/payments/collect/"

    def open(self) -> "PaymentCollectPage":
        self.goto(self.PATH)
        return self

    def select_vehicle_by_plate(self, license_plate: str) -> int:
        self.page.locator("select[name='vehicle']").select_option(label=license_plate)
        self.page.get_by_role("button", name="Tiếp tục").click()
        self.page.wait_for_url(re.compile(r"/payments/confirm/\d+/"))
        match = re.search(r"/payments/confirm/(\d+)/", self.page.url)
        assert match, f"Could not parse vehicle id from {self.page.url}"
        return int(match.group(1))


class PaymentConfirmPage(BasePage):
    def open(self, vehicle_id: int) -> "PaymentConfirmPage":
        self.goto(f"/payments/confirm/{vehicle_id}/")
        return self

    @property
    def debt_display(self) -> Locator:
        return self.page.locator(".stat-card__value")

    def confirm_payment(self, amount: int) -> None:
        self.page.locator("input[name='amount']").fill(str(amount))
        self.page.get_by_role("button", name="Xác nhận thu tiền").click()
