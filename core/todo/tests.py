import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task
from accounts.models import Profile

User = get_user_model()


@pytest.mark.django_db  # Add this line
def test_task_list_view(client):
    user = User.objects.create_user(email="testuser@example.com", password="password")
    profile, created = Profile.objects.get_or_create(user=user)
    client.login(email="testuser@example.com", password="password")

    Task.objects.create(title="Test Task 1", user=profile)
    Task.objects.create(title="Test Task 2", user=profile)

    response = client.get(reverse("todo:task-list"))

    assert response.status_code == 200
    assert "todo/task_list.html" in [
        t.name for t in response.templates
    ]


@pytest.mark.django_db
def test_task_create_view(client):
    user = User.objects.create_user(email="testuser@example.com", password="password")
    profile, created = Profile.objects.get_or_create(user=user)
    client.login(email="testuser@example.com", password="password")

    response = client.post(
        reverse("todo:task-create"),
        {
            "title": "New Task",
            "description": "Task description",
        },
    )

    assert response.status_code == 302
    assert Task.objects.filter(title="New Task").exists()


@pytest.mark.django_db
def test_task_update_view(client):
    user = User.objects.create_user(email="testuser@example.com", password="password")
    profile, created = Profile.objects.get_or_create(user=user)
    client.login(email="testuser@example.com", password="password")

    task = Task.objects.create(title="Old Task", user=profile)
    response = client.post(
        reverse("todo:task-update", kwargs={"pk": task.pk}),
        {
            "title": "Updated Task",
            "description": "Updated description",
        },
    )

    assert response.status_code == 302
    task.refresh_from_db()
    assert task.title == "Updated Task"


@pytest.mark.django_db
def test_task_delete_view(client):
    user = User.objects.create_user(email="testuser@example.com", password="password")
    profile, created = Profile.objects.get_or_create(user=user)
    client.login(email="testuser@example.com", password="password")

    task = Task.objects.create(title="Task to Delete", user=profile)
    response = client.post(reverse("todo:task-delete", kwargs={"pk": task.pk}))

    assert response.status_code == 302
    assert not Task.objects.filter(pk=task.pk).exists()


@pytest.mark.django_db
def test_task_done_view(client):
    user = User.objects.create_user(email="testuser@example.com", password="password")
    profile, created = Profile.objects.get_or_create(user=user)
    client.login(email="testuser@example.com", password="password")

    task = Task.objects.create(title="Task to Mark as Done", user=profile)
    response = client.post(reverse("todo:task-done", kwargs={"pk": task.pk}))

    assert response.status_code == 302
    task.refresh_from_db()
    assert task.is_completed
