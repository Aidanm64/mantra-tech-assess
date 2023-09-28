import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def pytest_configure():
    pytest.recording_uuid = ''


@pytest.fixture(scope="function")
def wait_for_api():
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=3,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    host = 'localhost'
    port = '8000'
    api_url = "http://%s:%s/" % (host, port)
    headers = {"accept": "*/*", "Content-Type": "application/json"}
    return request_session, api_url, headers