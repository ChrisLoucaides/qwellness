from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Account(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        ADVISOR = 'ADVISOR', 'Advisor',
        MENTAL_HEALTH_FIRST_AIDER = 'MENTAL_HEALTH_FIRST_AIDER', 'Mental Health First Aider'
        ADMIN = 'ADMIN', 'Admin'

    base_role = Role.ADMIN

    role = models.CharField(max_length=100, choices=Role.choices)

    # Fields specific to Student
    advisor = models.ForeignKey('user_management.Advisor', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='student_advisor')
    last_login_time = models.DateTimeField(null=True, blank=True)
    advisor_meeting_ids = models.JSONField(null=True, blank=True)
    task_ids = models.JSONField(null=True, blank=True)

    # Fields specific to Advisor
    advisee_meeting_ids = models.JSONField(null=True, blank=True)
    advisee_students = models.ManyToManyField('user_management.Student', related_name='advisees', blank=True)

    # Fields specific to Mental Health First Aider
    student_ids = models.JSONField(null=True, blank=True)


class Student(Account):
    base_role = Account.Role.STUDENT

    class Meta:
        proxy = True


class Advisor(Account):
    base_role = Account.Role.ADVISOR

    class Meta:
        proxy = True


class MentalHealthFirstAider(Account):
    class Meta:
        proxy = True
