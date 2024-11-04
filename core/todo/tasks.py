from celery import shared_task
from .models import Task

@shared_task
def delete_completed_tasks():
    deleted_count, _ = Task.objects.filter(is_completed=True).delete()
    return f"{deleted_count} completed tasks deleted."

@shared_task
def print_hello():
    print("Hello, this task runs every 10 seconds!")