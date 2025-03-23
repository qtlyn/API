import requests
import pytest
from concurrent.futures import ThreadPoolExecutor
import time
from config.get_token import get_token

BASE_URL = "http://127.0.0.1:8000"
HEADERS_VALID = {"Authorization": get_token()}

def send_request(i):
    time.sleep(0.05)  
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS_VALID)
    return response.status_code

def test_rate_limiting():
    request_count = 500  
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(send_request, range(request_count)))  
    blocked_count = results.count(429)
    assert blocked_count > 0, f"Rate Limiting KHÔNG hoạt động! gửi{request_count} request nhưng không bị chặn."

if __name__ == "__main__":
    pytest.main()