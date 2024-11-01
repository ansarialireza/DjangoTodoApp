from locust import HttpUser, task, between
import random

class LoginUser(HttpUser):
    wait_time = between(1, 3)

    # لیست نمونه از نام کاربری و گذرواژه
    users = [
        {"username": "admin@admin.com", "password": "admin"},
        # {"username": "testuser2@example.com", "password": "password2"},
        # می‌توانید کاربران بیشتری اضافه کنید
    ]

    @task
    def login(self):
        # دریافت توکن CSRF
        response = self.client.get("accounts/login/")
        csrf_token = self.extract_csrf_token(response.text)

        if csrf_token:
            # انتخاب یک کاربر به صورت تصادفی
            user = random.choice(self.users)
            login_data = {
                "username": user["username"],
                "password": user["password"],
                "csrfmiddlewaretoken": csrf_token,
            }

            # ارسال درخواست POST برای ورود
            response = self.client.post("/accounts/login/", data=login_data)

            if response.status_code == 200:
                print(f"Login successful for {user['username']}")
            else:
                print(f"Login failed for {user['username']}: {response.status_code}")

    def extract_csrf_token(self, html):
        # استخراج توکن CSRF از HTML
        import re
        match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
        return match.group(1) if match else None