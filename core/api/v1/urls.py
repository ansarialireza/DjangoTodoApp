from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

app_name = 'v1'


urlpatterns = [
    path('', include(router.urls)),
]