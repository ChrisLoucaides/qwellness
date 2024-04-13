import json
from django.test import TestCase, Client
from task_management.models import Task
from user_management.models import Student


class GetStudentTasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')
        self.client.force_login(self.student)

    def test_should_retrieve_tasks_associated_to_a_student(self):
        self.given_two_existing_tasks_are_in_the_database()

        response = self.when_we_make_a_request_to_the_student_tasks_endpoint()

        self.then_we_get_back_a_200(response)  # TODO FYP-23: refactor me

        response_data = json.loads(response.content)
        self.and_the_list_of_tasks_is_in_the_response_data(response_data)

        tasks = response_data['tasks']
        self.and_there_are_exactly_two_tasks_in_the_response(tasks)
        self.and_both_tasks_match_those_in_the_database(tasks)

    def and_both_tasks_match_those_in_the_database(self, tasks):
        self.assertEqual(tasks[0]['name'], 'Test Task 1')
        self.assertEqual(tasks[1]['name'], 'Test Task 2')

    def and_there_are_exactly_two_tasks_in_the_response(self, tasks):
        self.assertEqual(len(tasks), 2)

    def and_the_list_of_tasks_is_in_the_response_data(self, response_data):
        self.assertTrue('tasks' in response_data)

    def then_we_get_back_a_200(self, response):
        self.assertEqual(response.status_code, 200)

    def when_we_make_a_request_to_the_student_tasks_endpoint(self):
        response = self.client.get('/student-tasks/?username=test_student')
        return response

    def given_two_existing_tasks_are_in_the_database(self):
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

    def test_should_not_retrieve_tasks_given_invalid_student(self):
        response = self.when_a_request_to_the_student_tasks_endpoint_containing_an_invalid_student()

        self.then_we_get_a_404(response)
        response_data = json.loads(response.content)
        self.and_the_response_message_contains_a_student_not_found_error(response_data)

    def and_the_response_message_contains_a_student_not_found_error(self, response_data):
        self.assertEqual(response_data['error'], 'Student not found')

    def then_we_get_a_404(self, response):
        self.assertEqual(response.status_code, 404)

    def when_a_request_to_the_student_tasks_endpoint_containing_an_invalid_student(self):
        response = self.client.get('/student-tasks/?username=non_existing_student')
        return response

    def test_should_not_retrieve_student_tasks_given_wrong_http_method(self):
        response = self.when_a_post_request_is_made_to_the_student_tasks_endpoint()

        self.then_we_get_a_405(response)
        response_data = json.loads(response.content)
        self.and_the_response_message_contains_a_method_not_allowed_error(response_data)

    def and_the_response_message_contains_a_method_not_allowed_error(self, response_data):
        self.assertEqual(response_data['error'], 'Method not allowed')

    def then_we_get_a_405(self, response):
        self.assertEqual(response.status_code, 405)

    def when_a_post_request_is_made_to_the_student_tasks_endpoint(self):
        response = self.client.post('/student-tasks/')
        return response
