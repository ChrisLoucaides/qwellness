from django.urls import path

from meeting_management.views import create_meeting_student

urlpatterns = [
    path('advisor-meeting-for-student/', create_meeting_student, name='advisor-meeting-for-student'),
]
