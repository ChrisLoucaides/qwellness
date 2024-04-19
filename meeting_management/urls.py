from django.urls import path

from meeting_management.views import create_meeting_student, get_student_meetings, delete_meeting

urlpatterns = [
    path('advisor-meeting-for-student/', create_meeting_student, name='advisor-meeting-for-student'),
    path('student-meetings/', get_student_meetings, name='student-meetings'),
    path('remove-meeting/', delete_meeting, name='remove-meeting'),
]
