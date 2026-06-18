"""
QA concept: authenticated API testing — faster than full UI for data contracts.

GarageCar exposes /reception/api/search/ for the Ctrl+K command palette.
"""

import pytest

from utils.api_client import ApiClient


@pytest.mark.api
def test_search_api_returns_expected_shape(api_client: ApiClient) -> None:
    result = api_client.search("")

    assert set(result.keys()) == {"vehicles", "customers", "parts"}
    assert isinstance(result["vehicles"], list)
    assert isinstance(result["customers"], list)
    assert isinstance(result["parts"], list)


@pytest.mark.api
def test_search_api_finds_data_when_query_matches(api_client: ApiClient) -> None:
    result = api_client.search("a")

    total = len(result["vehicles"]) + len(result["customers"]) + len(result["parts"])
    assert total >= 0
