from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import *
from django.urls import reverse_lazy


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    ordering = ['created_at']
    
    # def get_queryset(self):
    #     return Task.objects.filter(user = self.request.user).order_by('created_at')
    
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('todo:task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy('todo:task-list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('todo:task-list')