import requests
import pytest
from config.get_token import get_token
from config.ghifile import save_results, add_test_result

BASE_URL = "http://127.0.0.1:8000"
HEADERS_VALID = {"Authorization": get_token()}  
HEADERS_INVALID = {"Authorization": "Bearer invalid_token"}
HEADERS_NONE = {}  
RESULT_FILE_PATH = r"D:/năm 3/kì 2/Kĩ thuật lập trình/bt nhóm/test_api/results/result_put.json"

@pytest.mark.order(1)
def test_put_update_user_success():
    """Put1: Cap nhat thong tin User hop le"""
    updated_user = {"Ten": "Van", "DiaChi": "Da Nang", "Email": "van111@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/8", json=updated_user, headers=HEADERS_VALID)
    add_test_result("Put1", response, 200)
    assert response.status_code == 200

@pytest.mark.order(2)
def test_put_update_user_no_auth():
    """Put2: Cap nhat User khi khong co Authorization."""
    updated_user = {"Ten": "Linh", "DiaChi": "Da Nang", "Email": "linh123@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/1", json=updated_user, headers=HEADERS_NONE)
    add_test_result("Put2", response, 401, "Not authenticated")
    assert response.status_code == 401

@pytest.mark.order(3)
def test_put_update_user_invalid_token():
    """Put3: Cap nhat User voi Token sai hoac het han"""
    updated_user = {"Ten": "Linh", "DiaChi": "Da Nang", "Email": "linh123@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/1", json=updated_user, headers=HEADERS_INVALID)
    add_test_result("Put3", response, 401, "Token không hợp lệ hoặc đã hết hạn")
    assert response.status_code == 401

@pytest.mark.order(4)
def test_put_update_nonexistent_user():
    """Put4: Cap nhat thong tin User khong ton tai"""
    updated_user = {"Ten": "Linh", "DiaChi": "Da Nang", "Email": "linh123@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/9999", json=updated_user, headers=HEADERS_VALID)
    add_test_result("Put4", response, 404, "Khong tim thay User!!!")
    assert response.status_code == 404

@pytest.mark.order(5)
def test_put_update_user_without_id():
    """Put5: Cap nhat User nhung khong chi dinh Id"""
    updated_user = {"Ten": "Linh", "DiaChi": "Da Nang", "Email": "linh123@gmail.com"}
    response = requests.put(f"{BASE_URL}/users", json=updated_user, headers=HEADERS_VALID)
    add_test_result("Put5", response, 405)
    assert response.status_code == 405

@pytest.mark.order(6)
def test_put_update_user_empty_data():
    """Put6: Cap nhat User nhung bo trong du lieu"""
    response = requests.put(f"{BASE_URL}/users/1", json={}, headers=HEADERS_VALID)
    add_test_result("Put6", response, 400, "Khong co du lieu de cap nhat")
    assert response.status_code == 400

@pytest.mark.order(7)
def test_put_update_user_duplicate_email():
    """Put7: Cap nhat email nhung trung voi email trong DB"""
    updated_user = {"Email": "lyn@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/5", json=updated_user, headers=HEADERS_VALID)
    add_test_result("Put7", response, 400)
    assert response.status_code == 400

@pytest.mark.order(8)
def test_put_update_user_invalid_format():
    """Put8: Cap nhat User nhung du lieu nhap khong dung dinh dang"""
    updated_user = {"Ten": 12345, "DiaChi": "Da Nang", "Email": "test@gmail.com"}
    response = requests.put(f"{BASE_URL}/users/5", json=updated_user, headers=HEADERS_VALID)
    add_test_result("Put8", response, 422)
    assert response.status_code == 422

@pytest.fixture(scope="session", autouse=True)
def finalize():
    """Luu ket qua vao file """
    yield
    save_results(RESULT_FILE_PATH)

if __name__ == "__main__":
    pytest.main()
