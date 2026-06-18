from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ReceptionPage(BasePage):
    """Today's vehicle reception ticket list."""

    PATH = "/reception/"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def open(self) -> "ReceptionPage":
        self.goto(self.PATH)
        return self

    @property
    def page_title(self) -> Locator:
        return self.page.locator(".page-header__title")

    @property
    def create_ticket_button(self) -> Locator:
        return self.page.get_by_role("link", name="Tạo phiếu mới")

    @property
    def tickets_table(self) -> Locator:
        return self.page.locator("table.data-table")
