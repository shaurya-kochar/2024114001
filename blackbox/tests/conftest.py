import pytest
import requests
import os

BASE_URL = "http://localhost:8080/api/v1"
ROLL_NUMBER = "2024101104"
USER_ID = os.getenv("QUICKCART_USER_ID", "1")

@pytest.fixture
def api_client():
    class APIClient:
        def request(self, method, endpoint, headers=None, **kwargs):
            if headers is None:
                headers = {}
            if "X-Roll-Number" not in headers:
                headers["X-Roll-Number"] = ROLL_NUMBER
            if "X-User-ID" not in headers:
                headers["X-User-ID"] = USER_ID
            url = f"{BASE_URL}{endpoint}"
            return requests.request(method, url, headers=headers, **kwargs)
        
        def get(self, endpoint, **kwargs): return self.request("GET", endpoint, **kwargs)
        def post(self, endpoint, **kwargs): return self.request("POST", endpoint, **kwargs)
        def put(self, endpoint, **kwargs): return self.request("PUT", endpoint, **kwargs)
        def delete(self, endpoint, **kwargs): return self.request("DELETE", endpoint, **kwargs)

    return APIClient()

@pytest.fixture
def roll_number():
    return ROLL_NUMBER

@pytest.fixture
def user_id():
    return USER_ID

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def reset_cart(api_client):
    api_client.delete("/cart/clear")
    yield
    api_client.delete("/cart/clear")
