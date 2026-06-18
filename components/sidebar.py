from playwright.sync_api import Locator, Page


class Sidebar:
    """Reusable navigation component from the authenticated app shell."""

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def root(self) -> Locator:
        return self.page.locator("#app-sidebar")

    def link(self, name: str) -> Locator:
        return self.root.get_by_role("link", name=name)

    def go_to_home(self) -> None:
        self.link("Trang chủ").click()

    def go_to_reception(self) -> None:
        self.link("Tiếp nhận xe").click()

    def go_to_workshop(self) -> None:
        self.link("Xưởng sửa chữa").click()
