from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryBrandPage(BasePage):
    PATH = "/inventory/brands/"

    def open(self) -> "InventoryBrandPage":
        self.goto(self.PATH)
        return self

    def add_brand(self, name: str) -> None:
        self.page.get_by_label("Tên hiệu xe").fill(name)
        self.page.get_by_role("button", name="Thêm").click()


class InventoryLaborPage(BasePage):
    PATH = "/inventory/labor-rates/"

    def open(self) -> "InventoryLaborPage":
        self.goto(self.PATH)
        return self

    def add_labor_rate(self, name: str, amount: int) -> None:
        self.page.get_by_label("Loại tiền công").fill(name)
        self.page.get_by_label("Mức tiền").fill(str(amount))
        self.page.get_by_role("button", name="Thêm").click()
