from rest_framework import viewsets
from todo.models import Task
from .serializers import TaskSerializer

from rest_framework import generics
from accounts.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
