import requests

def get_token():
    try:
        response = requests.post("http://127.0.0.1:8000/token",json={"username": "admin", "password": "password"})
        response.raise_for_status()
        data = response.json()
        access_token = data.get("access_token", "")
        token_type = data.get("token_type", "bearer")
        return f"{token_type} {access_token}"
    except requests.exceptions.RequestException as e:
        print(f"Loi lay token: {e}")
        return None

if __name__ == "__main__":
    token = get_token()
    print("Token:", token)