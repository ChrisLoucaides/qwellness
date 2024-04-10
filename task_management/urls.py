from django.urls import path
from task_management.views import create_task, get_student_tasks, update_task

urlpatterns = [
    path('new-task/', create_task, name='new-task'),
    path('student-tasks/', get_student_tasks, name='student-tasks'),
    path('edit-task/', update_task, name='edit-task')
]
