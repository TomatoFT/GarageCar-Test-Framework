from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Garage Pro home dashboard with bento stat cards."""

    PATH = "/dashboard/"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def open(self) -> "DashboardPage":
        self.goto(self.PATH)
        return self

    @property
    def greeting(self) -> Locator:
        return self.page.locator(".page-header__title")

    @property
    def receptions_today_card(self) -> Locator:
        return self.page.locator(".bento-card").filter(has_text="Tiếp nhận hôm nay")

    @property
    def quick_actions(self) -> Locator:
        return self.page.locator(".quick-actions")
