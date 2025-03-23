import requests
import pytest
from config.ghifile import save_results, add_test_result

BASE_URL = "http://127.0.0.1:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/token"
RESULT_FILE_PATH = r"D:/năm 3/kì 2/Kĩ thuật lập trình/bt nhóm/test_api/results/result_SQLi.json"

SQLI_PAYLOADS = [
    ("' OR '1'='1' --", "S1"),
    ("' OR '1'='1' /*", "S2"),
    ("1' OR '1'='1' --", "S3"),
    ("1' OR '1'='1' /*", "S4"),
    ("admin' --", "S5"),
    ("' UNION SELECT null, username, password FROM users --", "S6"),
    ("' OR (SELECT COUNT(*) FROM users) > 0 --", "S7"),
]

@pytest.mark.parametrize("payload, code", SQLI_PAYLOADS)
def test_sql_injection_login(payload, code):
    """ Kiểm tra SQL Injection trong quá trình đăng nhập """
    data = {"username": payload, "password":"password"}
    response = requests.post(LOGIN_ENDPOINT, json=data)
    is_vulnerable = response.status_code == 200 and "access_token" in response.text
    add_test_result(code, response, expected_status=401 if not is_vulnerable else 200)
    print(f"\n[{code}] Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"VULNERABLE: {is_vulnerable}\n")
    assert not is_vulnerable, f"API bị SQL Injection với payload: {payload}!"

@pytest.fixture(scope="session", autouse=True)
def finalize():
    """Lưu kết quả vào file"""
    yield
    save_results(RESULT_FILE_PATH)

if __name__ == "__main__":
    pytest.main()
