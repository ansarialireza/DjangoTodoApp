import os

from django.conf import settings

from celery import Celery

import redis

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object(f'django.conf:{settings.__name__}', namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')