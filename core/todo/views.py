from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Task
from .forms import TaskCreateForm, TaskUpdateForm
from django.views import View
from django.urls import reverse_lazy
from accounts.models import Profile


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ["created_at"]

    def get_queryset(self):
        user=self.request.user
        return Task.objects.filter(user=user).order_by("created_at")


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task-list")


class TaskDoneView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        task.is_completed = True
        task.save()
        return redirect(reverse_lazy("todo:task-list"))
