from django.db import models
from user_management.models import Student


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    description = models.TextField()
    completed = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name
