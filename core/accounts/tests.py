import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email="test@example.com", password="Testpassword1")
    assert user.email == "test@example.com"
    assert user.check_password("Testpassword1")


@pytest.mark.django_db
def test_superuser_creation():
    superuser = User.objects.create_superuser(
        email="admin@example.com", password="adminpassword"
    )
    assert superuser.is_superuser
    assert superuser.is_staff


@pytest.mark.django_db
def test_login_success(client):
    login_url = reverse("accounts:login")
    response = client.post(
        login_url, {"username": "test@example.com", "password": "Testpassword1"}
    )
    assert response.status_code == 302  # Redirect on successful login
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "شما با موفقیت وارد سایت  شدید."


@pytest.mark.django_db
def test_login_failure(client):
    User.objects.create_user(email="test@example.com", password="Testpassword1")
    login_url = reverse("accounts:login")
    response = client.post(
        login_url, {"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 200  # Should render the login page again
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0  # No success message should be present


@pytest.mark.django_db
def test_logout(client):
    client.login(email="test@example.com", password="Testpassword1")
    logout_url = reverse("accounts:logout")
    response = client.post(logout_url)  # Change to POST request
    assert response.status_code == 302  # Redirect after logout
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "شما با موفقیت از سایت خارج شدید."


@pytest.mark.django_db
def test_register_success(client):
    register_url = reverse("accounts:register")
    response = client.post(
        register_url,
        {
            "email": "test@example.com",
            "password1": "Strongpassword123",
            "password2": "Strongpassword123",
        },
    )
    assert response.status_code == 302  # Redirect after successful registration


@pytest.mark.django_db
def test_register_failure(client):
    register_url = reverse("accounts:register")
    response = client.post(
        register_url,
        {
            "username": "newuser@example.com",
            "password1": "newpassword",
            "password2": "differentpassword",
        },
    )
    assert response.status_code == 200  # Should render the registration page again
    assert not User.objects.filter(email="newuser@example.com").exists()


# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.contrib.messages import get_messages

# User = get_user_model()

# class UserModelTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')

#     def test_user_creation(self):
#         self.assertEqual(self.user.email, 'test@example.com')
#         self.assertTrue(self.user.check_password('Testpassword1'))

#     def test_superuser_creation(self):
#         superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
#         self.assertTrue(superuser.is_superuser)
#         self.assertTrue(superuser.is_staff)

# class LoginViewTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')
#         self.login_url = reverse('accounts:login')

#     def test_login_success(self):
#         response = self.client.post(self.login_url, {
#             'username': 'test@example.com',
#             'password': 'Testpassword1'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect on successful login
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "شما با موفقیت وارد سایت  شدید.")

#     def test_login_failure(self):
#         response = self.client.post(self.login_url, {
#             'username': 'test@example.com',
#             'password': 'wrongpassword'
#         })
#         self.assertEqual(response.status_code, 200)  # Should render the login page again
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(len(messages), 0)  # No success message should be present

# class LogoutViewTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')
#         self.client.login(email='test@example.com', password='Testpassword1')
#         self.logout_url = reverse('accounts:logout')

#     def test_logout(self):
#         response = self.client.post(self.logout_url)  # Change to POST request
#         self.assertEqual(response.status_code, 302)  # Redirect after logout
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "شما با موفقیت از سایت خارج شدید.")

# class RegisterViewTests(TestCase):
#     def setUp(self):
#         self.register_url = reverse('accounts:register')

#     def test_register_success(self):
#         response = self.client.post(self.register_url, {
#             'email': 'test@example.com',
#             'password1': 'Strongpassword123',
#             'password2': 'Strongpassword123'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after successful registration


#     def test_register_failure(self):
#         response = self.client.post(self.register_url, {
#             'username': 'newuser@example.com',
#             'password1': 'newpassword',
#             'password2': 'differentpassword'
#         })
#         self.assertEqual(response.status_code, 200)  # Should render the registration page again
#         self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
