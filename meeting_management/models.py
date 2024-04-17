from django.db import models
from user_management.models import Student, Advisor


class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_meetings')
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='advisor_meetings')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Meeting between {self.student.username} and {self.advisor.username} on {self.date}"
