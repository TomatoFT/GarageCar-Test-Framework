from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage


class LoginPage(BasePage):
    """Page object for the standalone login screen."""

    def __init__(self, page: Page, base_url: str | None = None) -> None:
        super().__init__(page, base_url or settings.BASE_URL)

    def open(self) -> "LoginPage":
        self.goto(settings.LOGIN_PATH)
        return self

    def login(self, username: str, password: str) -> DashboardPage:
        self.page.get_by_label("Tài khoản").fill(username)
        self.page.get_by_label("Mật khẩu").fill(password)
        self.page.get_by_role("button", name="Đăng nhập").click()
        return DashboardPage(self.page, self.base_url)
