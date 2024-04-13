import json
from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student
from task_management.models import Task


class DeleteStudentTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')

    def test_should_delete_task_associated_to_a_student(self):
        task = self.given_a_valid_task()
        self.given_the_student_is_logged_in()

        response = self.when_the_user_requests_to_delete_a_valid_task(task)

        self.then_the_task_is_deleted(response)
        self.and_we_get_a_success_message(response)

    def test_should_not_delete_task_given_missing_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_requests_to_delete_an_invalid_task()

        self.then_the_task_is_not_deleted_and_we_get_a_response_of(response, 400)
        self.and_an_error_message_of(response, {'error': 'Task ID is required'})

    def test_should_not_delete_task_given_invalid_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_with_an_invalid_task_id()

        self.then_the_task_is_not_deleted_and_we_get_a_response_of(response, 404)

        self.and_an_error_message_of(response, {'error': 'Task not found'})

    def test_should_not_delete_task_given_invalid_method(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_with_an_invalid_http_method()

        self.then_the_task_is_not_deleted_and_we_get_a_response_of(response, 405)
        self.and_an_error_message_of(response, {'error': 'Method not allowed'})

    def test_should_not_delete_task_given_unauthenticated_user(self):
        task = self.given_a_valid_task()

        response = self.when_the_user_requests_to_delete_a_valid_task(task)

        self.then_the_task_is_not_deleted_and_the_user_is_redirected(response)

    def given_the_student_is_logged_in(self):
        self.client.force_login(self.student)

    def given_a_valid_task(self):
        return Task.objects.create(name='Test Task', description='Test Description', student=self.student,
                                   due_date='2024-05-15')

    def when_the_user_requests_to_delete_a_valid_task(self, task):
        return self.client.delete(reverse('complete-task'), data=json.dumps({'id': task.id}),
                                  content_type='application/json')

    def when_the_user_makes_a_request_with_an_invalid_http_method(self):
        response = self.client.post(reverse('complete-task'))
        return response

    def when_the_user_requests_to_delete_an_invalid_task(self):
        response = self.client.delete(reverse('complete-task'), data=json.dumps({}),
                                      content_type='application/json')
        return response

    def when_the_user_makes_a_request_with_an_invalid_task_id(self):
        response = self.client.delete(reverse('complete-task'), data=json.dumps({'id': 999}),
                                      content_type='application/json')
        return response

    def then_the_task_is_deleted(self, response):
        self.assertEqual(response.status_code, 200)

    def then_the_task_is_not_deleted_and_we_get_a_response_of(self, response, response_code):
        self.assertEqual(response.status_code, response_code)

    def then_the_task_is_not_deleted_and_the_user_is_redirected(self, response):
        self.assertEqual(response.status_code, 302)

    def and_we_get_a_success_message(self, response):
        self.assertTrue(json.loads(response.content)['success'])

    def and_an_error_message_of(self, response, error):
        self.assertEqual(response.json(), error)
