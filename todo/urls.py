from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path("task/add/", TaskCreateView.as_view(), name="task-add"),
    path("task/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]
