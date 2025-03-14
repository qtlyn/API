import requests
import pytest
from config.get_token import get_token
from config.ghifile import save_results, add_test_result

BASE_URL = "http://127.0.0.1:8000"
HEADERS_VALID = {"Authorization": get_token()}  
HEADERS_INVALID = {"Authorization": "Bearer invalid_token"}
HEADERS_NONE = {}  
RESULT_FILE_PATH = r"D:/năm 3/kì 2/Kĩ thuật lập trình/bt nhóm/test_api/results/result_post.json"

@pytest.mark.order(1)
def test_post_create_user_success():
    """Post1: Them User moi thanh cong khi có Authorization."""
    new_user = {
        "Id": 7,
        "Ten": "Anh",
        "DiaChi": "Ninh Binh",
        "Email": "a123@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_VALID)
    add_test_result("Post1", response, 200)
    assert response.status_code == 200

@pytest.mark.order(2)
def test_post_create_user_without_authorization():
    """Post2: Them User moi khi khong co Authorization."""
    new_user = {
        "Id": 9,
        "Ten": "An",
        "DiaChi": "Hai Duong",
        "Email": "a123@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_NONE)
    add_test_result("Post2", response, 401, "Not authenticated")
    assert response.status_code == 401

@pytest.mark.order(3)
def test_post_create_user_invalid_token():
    """Post3: Them user moi khi token sai hoac het han"""
    new_user = {
        "Id": 10,
        "Ten": "An",
        "DiaChi": "Ha Noi",
        "Email": "a123@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_INVALID)
    add_test_result("Post3", response, 401, "Token không hợp lệ hoặc đã hết hạn")
    assert response.status_code == 401

@pytest.mark.order(4)
def test_post_create_user_duplicate_id():
    """Post4: Them User moi bi trung Id."""
    new_user = {
        "Id": 1,  
        "Ten": "An",
        "DiaChi": "Ha Noi",
        "Email": "a123@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_VALID)
    add_test_result("Post4", response, 400)
    assert response.status_code == 400

@pytest.mark.order(5)
def test_post_create_user_duplicate_email():
    """Post5: Them User moi bi trung email (vi phạm UNIQUE constraint)."""
    new_user = {
        "Id": 11,
        "Ten": "Yen",
        "DiaChi": "HCM",
        "Email": "lyn@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_VALID)
    add_test_result("Post5", response, 400)
    assert response.status_code == 400

@pytest.mark.order(6)
def test_post_create_user_missing_field():
    """Post6: Them User thieu mot cot(vi du cot email)."""
    new_user = {
        "Id": 12,
        "Ten": "Yen",
        "DiaChi": "HCM",
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_VALID)
    add_test_result("Post6", response, 422)
    assert response.status_code == 422

@pytest.mark.order(7)
def test_post_create_user_invalid_data_format():
    """Post7: Them User moi sai dinh dang du lieu(vi du sai dinh dang DiaChi)"""
    new_user = {
        "Id": 13,
        "Ten": "Yen",
        "DiaChi": 11111,
        "Email": "yenyen@gmail.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=HEADERS_VALID)
    add_test_result("Post7", response, 422)
    assert response.status_code == 422

@pytest.fixture(scope="session", autouse=True)
def finalize():
    """Luu ket qua vao file."""
    yield
    save_results(RESULT_FILE_PATH) 

if __name__ == "__main__":
    pytest.main()
