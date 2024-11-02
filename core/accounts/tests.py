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
def test_login_failure(client):
    User.objects.create_user(email="test@example.com", password="Testpassword1")
    login_url = reverse("accounts:login")
    response = client.post(
        login_url, {"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0


@pytest.mark.django_db
def test_logout(client):
    client.login(email="test@example.com", password="Testpassword1")
    logout_url = reverse("accounts:logout")
    response = client.post(logout_url)
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "شما با موفقیت از سایت خارج شدید."


# @pytest.mark.django_db
# def test_login_success(client):
#     user = User.objects.create_user(email="trthest@exththample.com", password="Teszdfgtpassword1")
#     user.save()

#     login_url = reverse("accounts:login")
#     response = client.post(
#         login_url, {"username": "trthest@exththample.com", "password": "Teszdfgtpassword1"}
#     )

#     assert response.status_code == 302
#     messages = list(get_messages(response.wsgi_request))
#     assert str(messages[0]) == "شما با موفقیت وارد سایت شدید."



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
    assert response.status_code == 200
    assert not User.objects.filter(email="newuser@example.com").exists()
