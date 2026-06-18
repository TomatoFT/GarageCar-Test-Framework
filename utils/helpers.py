import re
import time
from typing import Any

from faker import Faker

fake = Faker("vi_VN")


def unique_license_plate() -> str:
    """Generate a plausible Vietnamese license plate for test data exercises."""
    return f"{fake.random_int(10, 99)}{fake.random_uppercase_letter()}-{fake.random_int(10000, 99999)}"


def unique_phone() -> str:
    return fake.numerify("09########")


def extract_csrf_token(html: str) -> str:
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    if not match:
        raise ValueError("CSRF token not found in response HTML")
    return match.group(1)


def wait_for_server(url: str, timeout_seconds: int = 30) -> None:
    import urllib.error
    import urllib.request

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    raise TimeoutError(f"Server did not respond at {url} within {timeout_seconds}s")
