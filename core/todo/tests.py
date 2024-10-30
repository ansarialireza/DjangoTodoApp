from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task
from accounts.models import Profile

User = get_user_model()

class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(email='testuser@example.com', password='password')

    def test_task_list_view(self):
        Task.objects.create(title='Test Task 1', user=self.profile)
        Task.objects.create(title='Test Task 2', user=self.profile)

        response = self.client.get(reverse('todo:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')

    def test_task_create_view(self):
        response = self.client.post(reverse('todo:task-create'), {
            'title': 'New Task',
            'description': 'Task description',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        task = Task.objects.create(title='Old Task', user=self.profile)
        response = self.client.post(reverse('todo:task-update', kwargs={'pk': task.pk}), {
            'title': 'Updated Task',
            'description': 'Updated description',
        })
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_task_delete_view(self):
        task = Task.objects.create(title='Task to Delete', user=self.profile)
        response = self.client.post(reverse('todo:task-delete', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_done_view(self):
        task = Task.objects.create(title='Task to Mark as Done', user=self.profile)
        response = self.client.post(reverse('todo:task-done', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)