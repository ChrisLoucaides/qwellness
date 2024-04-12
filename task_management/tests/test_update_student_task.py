import json
from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student
from task_management.models import Task


class UpdateTaskViewTest(TestCase):  # TODO FYP-24: Refactor me
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')

    def test_update_task_valid_data(self):
        task = Task.objects.create(name='Test Task', due_date='2024-04-30', description='Test Description',
                                   student=self.student)

        self.client.force_login(self.student)

        updated_data = {
            'id': task.id,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('edit-task'), data=json.dumps(updated_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        updated_task = Task.objects.get(id=task.id)
        self.assertEqual(updated_task.name, 'Updated Task')
        self.assertEqual(str(updated_task.due_date), '2024-05-15')
        self.assertEqual(updated_task.description, 'Updated Description')

    def test_update_task_missing_id(self):
        self.client.force_login(self.student)

        data = {
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('edit-task'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Task ID is required'})

    def test_update_task_invalid_id(self):
        self.client.force_login(self.student)

        data = {
            'id': 999,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('edit-task'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Task not found'})

    def test_update_task_invalid_method(self):
        self.client.force_login(self.student)

        response = self.client.post(reverse('edit-task'))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Method not allowed'})

    def test_update_task_unauthenticated(self):
        data = {
            'id': 1,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('edit-task'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 302)
