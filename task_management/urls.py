from django.urls import path
from task_management.views import create_task, get_student_tasks

urlpatterns = [
    path('create_task/', create_task, name='create_task'),
    path('get_student_tasks/', get_student_tasks, name='get_student_tasks'),
]
