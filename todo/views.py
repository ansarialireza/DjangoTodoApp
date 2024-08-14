from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    ordering = ['created_at']
    
    # def get_queryset(self):
    #     return Task.objects.filter(user = self.request.user).order_by('created_at')
    
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    fields = ["name"]
    
    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.post = self.object
    #     comment.save()
    #     messages.success(self.request, 'ثبت با موفقیت انجام شد')
    #     return redirect(self.request.path_info)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    fields = ["name"]


class TaskDeleteView(DeleteView):
    model = Task