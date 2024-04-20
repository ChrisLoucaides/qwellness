from django.urls import path

from meeting_management.views import create_meeting_student, get_student_meetings, delete_meeting, \
    create_meeting_advisor

urlpatterns = [
    path('advisor-meeting-for-student/', create_meeting_student, name='advisor-meeting-for-student'),
    path('advisor-meeting-for-advisor/', create_meeting_advisor, name='advisor-meeting-for-advisor'),
    path('student-meetings/', get_student_meetings, name='student-meetings'),
    path('remove-meeting/', delete_meeting, name='remove-meeting'),
]
