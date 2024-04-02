from django.test import TestCase, Client
from task_management.models import Task, Student
from task_management.views import create_task
import json


class CreateTaskViewTestCase(TestCase):
    def setUp(self):
        # Create test accounts (students) for authentication
        self.student = Student.objects.create_user(username='test_user', password='test_password')

        # Create a test client
        self.client = Client()

    def test_should_create_a_task_for_a_student_account(self):
        # Given: Valid task data
        payload = {
            "username": "test_user",
            "name": "Complete Assignment",
            "due_date": "2024-04-10",
            "description": "Finish writing the essay for English class"
        }
        # When: Calling the create_task method
        response = create_task(self.get_request(payload))

        # Then: Ensure that the task is created successfully
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(Task.objects.filter(name="Complete Assignment").exists())

        # Get the student object
        student = Student.objects.get(username='test_user')

        # Check if the created task ID is added to the student's task_ids JSONField
        task_id = Task.objects.get(name="Complete Assignment").id
        self.assertIn(task_id, student.task_ids)

    def get_request(self, payload):
        request = self.client.post('/create-task/', json.dumps(payload), content_type='application/json')
        request.user = self.student
        return request
