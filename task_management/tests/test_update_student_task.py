import json
from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student
from task_management.models import Task


class UpdateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')

    def test_should_update_existing_task(self):
        task = self.given_a_valid_existing_task()
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_update_a_task(self.with_valid_updated_data(task))

        self.then_the_task_is_updated(response)
        self.and_the_updated_task_has_name(self.the_updated_task(task), 'Updated Task')
        self.and_the_updated_task_has_date(self.the_updated_task(task), '2024-05-15')
        self.and_the_updated_task_has_description(self.the_updated_task(task), 'Updated Description')

    def test_should_not_update_task_given_missing_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_update_a_task(self.updated_task_data_with_no_id())

        self.then_we_get_back_a_400(response)
        self.and_an_error_message_of(response, {'error': 'Task ID is required'})

    def test_should_not_update_task_given_invalid_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_update_a_task(self.updated_task_data_with_invalid_id())

        self.then_we_get_back_a_404(response)
        self.and_an_error_message_of(response, {'error': 'Task not found'})

    def test_update_task_invalid_method(self):
        self.given_the_student_is_logged_in()

        response = self.when_a_user_makes_a_request_with_an_invalid_post_method()

        self.then_we_get_back_a_405(response)
        self.and_an_error_message_of(response, {'error': 'Method not allowed'})

    def test_update_task_unauthenticated(self):
        data = {
            'id': 1,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        response = self.when_the_user_makes_a_request_to_update_a_task(data)

        self.assertEqual(response.status_code, 302)

    def given_the_student_is_logged_in(self):
        self.client.force_login(self.student)

    def given_a_valid_existing_task(self):
        task = Task.objects.create(name='Test Task', due_date='2024-04-30', description='Test Description',
                                   student=self.student)
        return task

    def when_the_user_makes_a_request_to_update_a_task(self, updated_data):
        response = self.client.put(reverse('edit-task'), data=json.dumps(updated_data),
                                   content_type='application/json')
        return response

    def then_the_task_is_updated(self, response):
        self.assertEqual(response.status_code, 200)

    def and_the_updated_task_has_description(self, updated_task, updated_task_description):
        self.assertEqual(updated_task.description, updated_task_description)

    def and_the_updated_task_has_date(self, updated_task, updated_task_date):
        self.assertEqual(str(updated_task.due_date), updated_task_date)

    def and_the_updated_task_has_name(self, updated_task, updated_task_name):
        self.assertEqual(updated_task.name, updated_task_name)

    def and_an_error_message_of(self, response, error):
        self.assertEqual(response.json(), error)

    def then_we_get_back_a_400(self, response):  # TODO FYP-24: Refactor into common method
        self.assertEqual(response.status_code, 400)

    def then_we_get_back_a_404(self, response):  # TODO FYP-24: Refactor into common method
        self.assertEqual(response.status_code, 404)

    def then_we_get_back_a_405(self, response):
        self.assertEqual(response.status_code, 405)

    def when_a_user_makes_a_request_with_an_invalid_post_method(self):
        response = self.client.post(reverse('edit-task'))
        return response

    @staticmethod
    def updated_task_data_with_no_id():
        data = {
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        return data

    @staticmethod
    def the_updated_task(task):
        updated_task = Task.objects.get(id=task.id)
        return updated_task

    @staticmethod
    def with_valid_updated_data(task):
        updated_data = {
            'id': task.id,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        return updated_data

    @staticmethod
    def updated_task_data_with_invalid_id():
        data = {
            'id': 999,
            'name': 'Updated Task',
            'due_date': '2024-05-15',
            'description': 'Updated Description'
        }
        return data
