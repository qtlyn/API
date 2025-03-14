import requests
import pytest
from config.get_token import get_token
from config.ghifile import save_results, add_test_result

BASE_URL = "http://127.0.0.1:8000"
HEADERS_VALID = {"Authorization": get_token()}  
HEADERS_INVALID = {"Authorization": "Bearer invalid_token"}
HEADERS_NONE = {}  
RESULT_FILE_PATH = r"D:/năm 3/kì 2/Kĩ thuật lập trình/bt nhóm/test_api/results/result_get.json"

@pytest.mark.order(1)
def test_get_users_success():
    """G1: Kiem tra API co tra ve dung thong tin khong"""
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS_VALID)
    add_test_result("G1", response, 200)
    assert response.status_code == 200

@pytest.mark.order(2)
def test_get_user_by_id_success():
    """G2: Lay thong tin User theo Id co ton tai"""
    response = requests.get(f"{BASE_URL}/users/1", headers=HEADERS_VALID)
    add_test_result("G2", response, 200)
    assert response.status_code == 200

@pytest.mark.order(3)
def test_get_user_by_invalid_id():
    """G3: Lay thong tin User theo Id khong ton tai"""
    response = requests.get(f"{BASE_URL}/users/9999", headers=HEADERS_VALID)
    add_test_result("G3", response, 404)
    assert response.status_code == 404

@pytest.mark.order(4)
def test_get_users_unauthorized():
    """G4: Kiem tra API co tra ve du lieu khi khong co Authorization."""
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS_NONE)
    add_test_result("G4", response, 401)
    assert response.status_code == 401

@pytest.mark.order(5)
def test_get_users_invalid_token():
    """G5: Kiem tra API co tra ve du lieu khi Authorization sai hoac het han"""
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS_INVALID)
    add_test_result("G5", response, 401)
    assert response.status_code == 401

@pytest.fixture(scope="session", autouse=True)
def finalize():
    """Luu ket qua vao file"""
    yield
    save_results(RESULT_FILE_PATH)

if __name__ == "__main__":
    pytest.main()
