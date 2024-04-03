import json
from django.test import TestCase, Client
from task_management.models import Task
from user_management.models import Student


class GetStudentTasksTest(TestCase):  # TODO FYP-23: Refactor me
    def setUp(self):
        self.client = Client()
        # Create a test student and log in
        self.student = Student.objects.create(username='test_student')
        self.client.force_login(self.student)

    def test_get_student_tasks_success(self):
        # Given
        Task.objects.create(
            name='Test Task 1',
            due_date='2024-04-02',
            description='Test Description 1',
            student=self.student
        )
        Task.objects.create(
            name='Test Task 2',
            due_date='2024-04-03',
            description='Test Description 2',
            student=self.student
        )
        # When
        response = self.client.get('/get_student_tasks/?username=test_student')
        # Then
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue('tasks' in response_data)
        tasks = response_data['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['name'], 'Test Task 1')
        self.assertEqual(tasks[1]['name'], 'Test Task 2')

    def test_get_student_tasks_student_not_found(self):
        # Given
        # Non-existing student
        # When
        response = self.client.get('/get_student_tasks/?username=non_existing_student')
        # Then
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Student not found')

    def test_get_student_tasks_method_not_allowed(self):
        # When
        response = self.client.post('/get_student_tasks/')
        # Then
        self.assertEqual(response.status_code, 405)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Method not allowed')
