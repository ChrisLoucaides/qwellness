from django.db import models
from user_management.models import Account


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='student_meetings')
    advisor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='advisor_meetings')
    date_and_time = models.DateTimeField()

    def __str__(self):
        return f"Meeting between {self.student.username} and {self.advisor.username} at {self.date_and_time}"
