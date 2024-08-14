from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', ServicesListView.as_view(), name='index'),
]
