from locust import HttpUser, task, between
from config.get_token import get_token

class APITestUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.token = get_token()
        self.headers = {"Authorization": self.token} if self.token else {}

    @task(2)
    def get_users(self):
        self.client.get("/users", headers=self.headers)

    @task(1)
    def get_user_by_id(self):
        self.client.get("/users/1", headers=self.headers)

    @task(1)
    def create_user(self):
        new_user = {
            "Id": 100,
            "Ten": "Test",
            "DiaChi": "Ha Noi",
            "Email": "test_locust@gmail.com"
        }
        self.client.post("/users", json=new_user, headers=self.headers)

    @task(1)
    def update_user(self):
        updated_data = {"Ten": "Updated Locust"}
        self.client.put("/users/100", json=updated_data, headers=self.headers)

    @task(1)
    def delete_user(self):
        self.client.delete("/users/100", headers=self.headers)

if __name__ == "__main__":
    import os
    os.system("locust -f test_load.py")
