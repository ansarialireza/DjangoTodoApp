import pytest
from django.urls import reverse
from todo.models import Task
from accounts.models import User, Profile
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestTaskViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={
                "first_name": "Test",
                "last_name": "User",
                "description": "A test user",
            },
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_tasks(self):
        Task.objects.create(title="Task 1", is_completed=False, user=self.user)  # Use self.user
        Task.objects.create(title="Task 2", is_completed=True, user=self.user)    # Use self.user

        url = reverse("api:v1:task-list")
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == "Task 1"
        assert response.data[1]["title"] == "Task 2"

    def test_create_task(self):
        url = reverse("api:v1:task-list")
        data = {"title": "New Task", "is_completed": False, "user": self.user.id}  # Use self.user.id
        response = self.client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data["title"] == "New Task"
        assert response.data["is_completed"] is False
        assert response.data["user"] == self.user.id

    def test_update_task(self):
        task = Task.objects.create(
            title="Task 1", is_completed=False, user=self.user  # Use self.user
        )
        url = reverse("api:v1:task-detail", args=[task.id])
        data = {"title": "Updated Task", "is_completed": True, "user": self.user.id}  # Use self.user.id
        response = self.client.put(url, data, format="json")

        assert response.status_code == 200
        assert response.data["title"] == "Updated Task"
        assert response.data["is_completed"] is True

    def test_delete_task(self):
        task = Task.objects.create(
            title="Task 1", is_completed=False, user=self.user  # Use self.user
        )
        url = reverse("api:v1:task-detail", args=[task.id])
        response = self.client.delete(url)

        assert response.status_code == 204
        assert Task.objects.count() == 0