"""Shared pytest fixtures for Playwright page objects and API helpers."""

import re

import pytest
from playwright.sync_api import APIRequestContext, Browser, Page, Playwright

from components.sidebar import Sidebar
from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.reception_page import ReceptionPage
from utils.api_client import ApiClient
from utils.garage_seed import seed_e2e_data


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-baselines",
        action="store_true",
        default=False,
        help="Refresh committed visual baseline PNG files",
    )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": settings.BASE_URL,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def auth_storage(browser: Browser) -> str:
    """
    Log in once per session and persist cookies to disk.

    Tests using `authenticated_page` reuse this state instead of
    walking through the login form every time.
    """
    settings.AUTH_DIR.mkdir(parents=True, exist_ok=True)
    path = str(settings.AUTH_STORAGE)

    context = browser.new_context(
        base_url=settings.BASE_URL,
        viewport={"width": 1280, "height": 720},
    )
    page = context.new_page()
    LoginPage(page).open().login(settings.DEMO_USERNAME, settings.DEMO_PASSWORD)
    page.wait_for_url(re.compile(r".*/dashboard/?$"))
    context.storage_state(path=path)
    context.close()
    return path


@pytest.fixture
def authenticated_page(browser: Browser, auth_storage: str) -> Page:
    """Browser page with a restored Django session (fast path)."""
    context = browser.new_context(
        base_url=settings.BASE_URL,
        storage_state=auth_storage,
        viewport={"width": 1280, "height": 720},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def api_request_context(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=settings.BASE_URL)
    yield context
    context.dispose()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    return DashboardPage(page, settings.BASE_URL)


@pytest.fixture
def reception_page(page: Page) -> ReceptionPage:
    return ReceptionPage(page, settings.BASE_URL)


@pytest.fixture
def sidebar(page: Page) -> Sidebar:
    return Sidebar(page)


@pytest.fixture(scope="session")
def garage_prerequisites() -> None:
    """Ensure brand + labor rate exist before core flow tests."""
    seed_e2e_data()


@pytest.fixture
def api_client(api_request_context: APIRequestContext) -> ApiClient:
    client = ApiClient(api_request_context)
    client.login(settings.DEMO_USERNAME, settings.DEMO_PASSWORD)
    return client
