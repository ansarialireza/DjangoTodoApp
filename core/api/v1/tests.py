from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todo.models import Task
from accounts.models import User, Profile
from rest_framework.authtoken.models import Token

class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_task(self):
        url = reverse('api:v1:task-list')
        data = {'title': 'New Task', 'user': self.profile.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_list_tasks(self):
        Task.objects.create(title='Task 1', user=self.profile)
        Task.objects.create(title='Task 2', user=self.profile)
        
        url = reverse('api:v1:task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task(self):
        task = Task.objects.create(title='Task to Retrieve', user=self.profile)
        url = reverse('api:v1:task-detail', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task(self):
        task = Task.objects.create(title='Old Task', user=self.profile)
        url = reverse('api:v1:task-detail', args=[task.id])
        data = {'title': 'Updated Task', 'user': self.profile.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(title='Task to Delete', user=self.profile)
        url = reverse('api:v1:task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())