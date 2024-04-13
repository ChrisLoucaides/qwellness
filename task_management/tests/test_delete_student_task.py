from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student
from task_management.models import Task


class DeleteTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')

    def test_should_delete_existing_task(self):
        task = self.given_a_valid_existing_task()
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_delete_a_task(task.id)

        self.then_the_task_is_deleted(response)
        self.then_attempt_to_get_deleted_task_fails(task.id)

    def test_should_not_delete_task_given_missing_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_delete_a_task(None)

        self.then_we_get_a_response_code(response, 400)
        self.and_an_error_message_of(response, {'error': 'Task ID is required'})

    def test_should_not_delete_task_given_invalid_id(self):
        self.given_the_student_is_logged_in()

        response = self.when_the_user_makes_a_request_to_delete_a_task(999)

        self.then_we_get_a_response_code(response, 404)
        self.and_an_error_message_of(response, {'error': 'Task not found'})

    def test_should_not_delete_task_given_invalid_method(self):
        self.given_the_student_is_logged_in()

        response = self.when_a_user_makes_a_request_with_an_invalid_delete_method()

        self.then_we_get_a_response_code(response, 405)
        self.and_an_error_message_of(response, {'error': 'Method not allowed'})

    def test_should_not_delete_task_given_unauthenticated_user(self):
        response = self.when_the_user_makes_a_request_to_delete_a_task(1)

        self.then_we_get_a_response_code(response, 302)

    def given_the_student_is_logged_in(self):
        self.client.force_login(self.student)

    def given_a_valid_existing_task(self):
        task = Task.objects.create(name='Test Task', due_date='2024-04-30', description='Test Description',
                                   student=self.student)
        return task

    def when_the_user_makes_a_request_to_delete_a_task(self, task_id):
        response = self.client.delete(reverse('complete-task', kwargs={'task_id': task_id}))
        return response

    def when_a_user_makes_a_request_with_an_invalid_delete_method(self):
        response = self.client.post(reverse('complete-task', kwargs={'task_id': 1}))
        return response

    def then_the_task_is_deleted(self, response):
        self.assertEqual(response.status_code, 200)

    def then_attempt_to_get_deleted_task_fails(self, task_id):
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def then_we_get_a_response_code(self, response, response_code):
        self.assertEqual(response.status_code, response_code)

    def and_an_error_message_of(self, response, error):
        self.assertEqual(response.json(), error)
