from playwright.sync_api import APIRequestContext

from config import settings
from utils.helpers import extract_csrf_token


class ApiClient:
    """Thin wrapper around Playwright's APIRequestContext for Django session auth."""

    def __init__(self, request: APIRequestContext) -> None:
        self.request = request
        self.base_url = settings.BASE_URL

    def login(self, username: str, password: str) -> APIRequestContext:
        login_page = self.request.get(f"{self.base_url}{settings.LOGIN_PATH}")
        csrf = extract_csrf_token(login_page.text())
        response = self.request.post(
            f"{self.base_url}{settings.LOGIN_PATH}",
            form={
                "csrfmiddlewaretoken": csrf,
                "username": username,
                "password": password,
            },
            headers={"Referer": f"{self.base_url}{settings.LOGIN_PATH}"},
        )
        if response.status not in (200, 302):
            raise RuntimeError(f"Login failed with status {response.status}")
        return self.request

    def search(self, query: str) -> dict:
        response = self.request.get(
            f"{self.base_url}/reception/api/search/",
            params={"q": query},
        )
        if response.status != 200:
            raise RuntimeError(f"Search failed with status {response.status}")
        return response.json()
