import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class RepairStartPage(BasePage):
    PATH = "/repairs/start/"

    def open(self) -> "RepairStartPage":
        self.goto(self.PATH)
        return self

    def start_repair(self, license_plate: str) -> None:
        self.page.locator("input[name='license_plate']").fill(license_plate)
        self.page.get_by_role("button", name="Tạo phiếu sửa").click()


class RepairDetailPage(BasePage):
    def __init__(self, page: Page, base_url: str, order_id: int | None = None) -> None:
        super().__init__(page, base_url)
        self.order_id = order_id

    def open(self, order_id: int) -> "RepairDetailPage":
        self.order_id = order_id
        self.goto(f"/repairs/{order_id}/")
        return self

    @property
    def title(self) -> Locator:
        return self.page.locator(".page-header__title")

    @property
    def line_items_table(self) -> Locator:
        return self.page.locator("table.data-table")

    def add_labor_line(self, *, quantity: int, description: str) -> None:
        self.page.locator("input[name='quantity']").fill(str(quantity))
        self.page.locator("select[name='labor_rate']").select_option(index=1)
        self.page.locator("input[name='description']").fill(description)
        self.page.get_by_role("button", name="Thêm").click()

    def wait_for_order_id_from_url(self) -> int:
        self.page.wait_for_url(re.compile(r"/repairs/\d+/"))
        match = re.search(r"/repairs/(\d+)/", self.page.url)
        assert match, f"Could not parse repair order id from {self.page.url}"
        return int(match.group(1))


class WorkshopPage(BasePage):
    PATH = "/repairs/workshop/"

    def open(self) -> "WorkshopPage":
        self.goto(self.PATH)
        return self

    @property
    def kanban(self) -> Locator:
        return self.page.locator("#workshop-kanban")

    def column(self, status: str) -> Locator:
        return self.kanban.locator(f".kanban__column[data-status='{status}']")
