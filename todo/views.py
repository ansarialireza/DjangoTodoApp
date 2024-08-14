from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    ordering = ['created_at']