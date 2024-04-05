import json
from django.test import TestCase, Client
from task_management.models import Task
from user_management.models import Student


class CreateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')
        self.client.force_login(self.student)

    def test_create_task_success(self):
        data = self.given_a_valid_task_payload()

        response = self.when_a_post_request_is_made_to_the_create_task_endpoint(data)

        self.then_a_new_task_is_created(response)

        response_data = json.loads(response.content)
        self.and_we_get_a_success_response(response_data)

        task_id = response_data['task_id']
        self.and_the_task_has_been_added_to_the_database(task_id)

        Task.objects.filter(pk=task_id).delete()  # Clean Up

    def and_the_task_has_been_added_to_the_database(self, task_id):
        self.assertIsNotNone(Task.objects.filter(pk=task_id).first())

    def and_we_get_a_success_response(self, response_data):
        self.assertTrue(response_data['success'])

    def then_a_new_task_is_created(self, response):
        self.assertEqual(response.status_code, 201)

    def when_a_post_request_is_made_to_the_create_task_endpoint(self, data):
        return self.client.post('/create_task/', data=data)

    @staticmethod
    def given_a_valid_task_payload():
        data = {
            'username': 'test_student',
            'name': 'Test Task',
            'due_date': '2024-04-02',
            'description': 'Test Description'
        }
        return data

    def test_create_task_student_not_found(self):
        data = self.given_an_invalid_student_in_the_payload()

        response = self.when_a_post_request_is_made_to_the_create_task_endpoint(data)

        self.then_we_get_a_404(response)

        response_data = json.loads(response.content)
        self.and_the_response_contains_a_student_not_found_error_message(response_data)

    def and_the_response_contains_a_student_not_found_error_message(self, response_data):
        self.assertEqual(response_data['error'], 'Student not found')

    def then_we_get_a_404(self, response):
        self.assertEqual(response.status_code, 404)

    @staticmethod
    def given_an_invalid_student_in_the_payload():
        data = {
            'username': 'non_existing_student',
            'name': 'Test Task',
            'due_date': '2024-04-02',
            'description': 'Test Description'
        }
        return data

    def test_create_task_method_not_allowed(self):
        response = self.when_a_get_request_is_made_to_the_create_task_endpoint()

        self.then_we_get_a_405(response)

        response_data = json.loads(response.content)
        self.and_the_response_contains_a_method_not_allowed_message(response_data)

    def and_the_response_contains_a_method_not_allowed_message(self, response_data):
        self.assertEqual(response_data['error'], 'Method not allowed')

    def then_we_get_a_405(self, response):
        self.assertEqual(response.status_code, 405)

    def when_a_get_request_is_made_to_the_create_task_endpoint(self):
        response = self.client.get('/create_task/')
        return response
