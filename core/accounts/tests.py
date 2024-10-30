from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('Testpassword1'))

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')
        self.login_url = reverse('accounts:login')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'Testpassword1'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on successful login
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "شما با موفقیت وارد سایت  شدید.")

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should render the login page again
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)  # No success message should be present

class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='Testpassword1')
        self.client.login(email='test@example.com', password='Testpassword1')
        self.logout_url = reverse('accounts:logout')

    def test_logout(self):
        response = self.client.post(self.logout_url)  # Change to POST request
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "شما با موفقیت از سایت خارج شدید.")

class RegisterViewTests(TestCase):
    def setUp(self):
        self.register_url = reverse('accounts:register')

    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'email': 'test@example.com',
            'password1': 'Strongpassword123',
            'password2': 'Strongpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration


    def test_register_failure(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should render the registration page again
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())


