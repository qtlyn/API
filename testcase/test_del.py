import requests
import pytest
from config.get_token import get_token
from config.ghifile import save_results, add_test_result

BASE_URL = "http://127.0.0.1:8000"
HEADERS_VALID = {"Authorization": get_token()}  
HEADERS_INVALID = {"Authorization": "Bearer invalid_token"}
HEADERS_NONE = {}  
RESULT_FILE_PATH = r"D:/năm 3/kì 2/Kĩ thuật lập trình/bt nhóm/test_api/results/result_del.json"

@pytest.mark.order(1)
def test_delete_user_success():
    """Del1: Xoa user thanh cong"""
    response = requests.delete(f"{BASE_URL}/users/7", headers=HEADERS_VALID)
    add_test_result("Del1", response, 200, "xoa User thanh cong")
    assert response.status_code == 200

@pytest.mark.order(2)
def test_delete_user_without_authorization():
    """Del2: xoa User khi khong co Authorization"""
    response = requests.delete(f"{BASE_URL}/users/8", headers=HEADERS_NONE)
    add_test_result("Del2", response, 401, "Not authenticated")
    assert response.status_code == 401

@pytest.mark.order(3)
def test_delete_user_invalid_token():
    """Del3: Xoa User khi token sai hoac het han"""
    response = requests.delete(f"{BASE_URL}/users/9", headers=HEADERS_INVALID)
    add_test_result("Del3", response, 401, "Token không hợp lệ hoặc đã hết hạn")
    assert response.status_code == 401

@pytest.mark.order(4)
def test_delete_nonexistent_user():
    """Del4: Xoa thong tin User khong ton tai"""
    response = requests.delete(f"{BASE_URL}/users/999", headers=HEADERS_VALID)
    add_test_result("Del4", response, 404, "Khong tim thay user")
    assert response.status_code == 404

@pytest.fixture(scope="session", autouse=True)
def finalize():
    """Luu ket qua vao file"""
    yield
    save_results(RESULT_FILE_PATH) 

if __name__ == "__main__":
    pytest.main()
