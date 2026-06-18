"""
QA concept: API layer of the test pyramid — verify session auth without a browser.

Playwright's request context handles cookies automatically after form login.
"""

import pytest

from config import settings
from utils.api_client import ApiClient
from utils.helpers import extract_csrf_token


@pytest.mark.api
def test_login_sets_session_cookie(api_request_context) -> None:
    login_page = api_request_context.get(f"{settings.BASE_URL}{settings.LOGIN_PATH}")
    csrf = extract_csrf_token(login_page.text())

    response = api_request_context.post(
        f"{settings.BASE_URL}{settings.LOGIN_PATH}",
        form={
            "csrfmiddlewaretoken": csrf,
            "username": settings.DEMO_USERNAME,
            "password": settings.DEMO_PASSWORD,
        },
        headers={"Referer": f"{settings.BASE_URL}{settings.LOGIN_PATH}"},
        max_redirects=0,
    )

    assert response.status == 302
    assert "sessionid" in response.headers.get("set-cookie", "")


@pytest.mark.api
def test_protected_dashboard_requires_auth(api_request_context) -> None:
    response = api_request_context.get(f"{settings.BASE_URL}/dashboard/", max_redirects=0)
    assert response.status == 302
