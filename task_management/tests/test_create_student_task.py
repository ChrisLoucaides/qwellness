import json
from django.test import TestCase, Client
from task_management.models import Task
from user_management.models import Student


class CreateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test student and log in
        self.student = Student.objects.create(username='test_student')
        self.client.force_login(self.student)

    def test_create_task_success(self):
        # Given
        data = {
            'username': 'test_student',
            'name': 'Test Task',
            'due_date': '2024-04-02',
            'description': 'Test Description'
        }
        # When
        response = self.client.post('/create_task/', data=data)
        # Then
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        task_id = response_data['task_id']
        self.assertIsNotNone(Task.objects.filter(pk=task_id).first())
        # Clean up
        Task.objects.filter(pk=task_id).delete()

    def test_create_task_student_not_found(self):
        # Given
        data = {
            'username': 'non_existing_student',
            'name': 'Test Task',
            'due_date': '2024-04-02',
            'description': 'Test Description'
        }
        # When
        response = self.client.post('/create_task/', data=data)
        # Then
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Student not found')

    def test_create_task_method_not_allowed(self):
        # When
        response = self.client.get('/create_task/')
        # Then
        self.assertEqual(response.status_code, 405)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Method not allowed')
