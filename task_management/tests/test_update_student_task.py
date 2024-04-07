import json
from datetime import datetime

from django.test import TestCase, Client
from task_management.models import Task
from user_management.models import Student


class UpdateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')
        self.client.force_login(self.student)
        self.task = Task.objects.create(name='Test Task', due_date='2024-04-02', description='Test Description', student=self.student)

    def test_should_update_existing_task(self):
        data = self.given_a_valid_task_payload()

        response = self.when_a_put_request_is_made_to_the_update_task_endpoint(data)

        self.then_task_is_updated(response)

        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.name, data['name'])
        self.assertEqual(updated_task.description, data['description'])
        self.assertEqual(updated_task.due_date, datetime.strptime(data['due_date'], '%Y-%m-%d').date())

    def then_task_is_updated(self, response):
        self.assertEqual(response.status_code, 200)

    def when_a_put_request_is_made_to_the_update_task_endpoint(self, data):
        return self.client.put('/update_task/', data=json.dumps(data), content_type='application/json')

    @staticmethod
    def given_a_valid_task_payload():
        data = {
            'task_id': 1,
            'name': 'Updated Task Name',
            'due_date': '2024-04-05',
            'description': 'Updated Description'
        }
        return data

    def test_should_not_update_task_when_task_id_is_missing(self):
        data = self.given_an_invalid_task_payload()

        response = self.when_a_put_request_is_made_to_the_update_task_endpoint(data)

        self.then_we_get_a_400(response)

        response_data = json.loads(response.content)
        self.and_the_response_contains_a_task_id_required_error_message(response_data)

    def and_the_response_contains_a_task_id_required_error_message(self, response_data):
        self.assertEqual(response_data['error'], 'Task ID is required')

    def then_we_get_a_400(self, response):
        self.assertEqual(response.status_code, 400)

    @staticmethod
    def given_an_invalid_task_payload():
        data = {
            'name': 'Updated Task Name',
            'due_date': '2024-04-05',
            'description': 'Updated Description'
        }
        return data

    def test_should_not_update_task_when_task_does_not_exist(self):
        data = self.given_an_invalid_task_id()

        response = self.when_a_put_request_is_made_to_the_update_task_endpoint(data)

        self.then_we_get_a_404(response)

        response_data = json.loads(response.content)
        self.and_the_response_contains_a_task_not_found_error_message(response_data)

    def and_the_response_contains_a_task_not_found_error_message(self, response_data):
        self.assertEqual(response_data['error'], 'Task not found')

    def then_we_get_a_404(self, response):
        self.assertEqual(response.status_code, 404)

    @staticmethod
    def given_an_invalid_task_id():
        data = {
            'task_id': 9999,
            'name': 'Updated Task Name',
            'due_date': '2024-04-05',
            'description': 'Updated Description'
        }
        return data

    def test_should_not_update_task_when_wrong_http_method_used(self):
        response = self.when_a_get_request_is_made_to_the_update_task_endpoint()

        self.then_we_get_a_405(response)

        response_data = json.loads(response.content)
        self.and_the_response_contains_a_method_not_allowed_message(response_data)

    def and_the_response_contains_a_method_not_allowed_message(self, response_data):
        self.assertEqual(response_data['error'], 'Method not allowed')

    def then_we_get_a_405(self, response):
        self.assertEqual(response.status_code, 405)

    def when_a_get_request_is_made_to_the_update_task_endpoint(self):
        return self.client.get('/update_task/')
