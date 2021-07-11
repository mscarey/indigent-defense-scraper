import pytest

from scrapers.hays import search_calendar


@pytest.mark.vcr
def test_search_calendar():
    response = search_calendar()
    assert response.status_code == 200
