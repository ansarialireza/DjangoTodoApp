from django.core.management.base import BaseCommand
from faker import Faker
from todo.models import Task
from accounts.models import User
import random

class Command(BaseCommand):

    help = "Create five random tasks"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fake = Faker()
    
    def handle(self, *args, **options):
        user_email = self.fake.email()
        # user_password = self.fake.password()
        user_password = "Ansari@ansari1"
        user = User.objects.create_user(email = user_email,password = user_password)

        user.profile.first_name = self.fake.first_name()
        user.profile.last_name = self.fake.last_name()
        user.profile.description = self.fake.text()
        user.profile.save()

        for _ in range(5):
            task = Task(
                title = self.fake.sentence(),
                is_completed=random.choice([True,False]),
                user = user
            )
            task.save()
            self.stdout.write(self.style.SUCCESS(f'Task "task.title" created successfully for user "user.email"'))
