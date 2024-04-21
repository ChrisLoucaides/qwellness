from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student, Advisor
from meeting_management.models import Meeting


class TestGetStudentMeetingsView(TestCase):
    def setUp(self):
        self.client = Client()

        self.student = Student.objects.create(username='test_student', email='student@example.com')

        self.advisor = Advisor.objects.create(username='test_advisor', email='advisor@example.com')

        self.meeting1 = Meeting.objects.create(student=self.student, advisor=self.advisor, date='2024-04-18',
                                               time='10:00:00')
        self.meeting2 = Meeting.objects.create(student=self.student, advisor=self.advisor, date='2024-04-19',
                                               time='11:00:00')

    def test_should_retrieve_student_meetings(self):
        self.given_a_logged_in_student()

        response = self.when_the_user_requests_to_view_their_tasks()

        self.then_we_get_back_a_response_code(response, 200)
        self.and_the_correct_number_of_meetings_are_returned(response)

    def test_should_not_retrieve_student_meetings_given_invalid_method(self):
        self.given_a_logged_in_student()

        response = self.when_a_user_requests_to_view_their_tasks_with_an_incorrect_http_post_method()

        self.then_we_get_back_a_response_code(response, 405)

    def test_should_not_retrieve_student_meetings_given_invalid_student_id(self):
        self.given_a_logged_in_student()

        response = self.when_the_user_with_an_invalid_id_requests_to_view_their_tasks()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def given_a_logged_in_student(self):
        self.client.force_login(self.student)

    def when_the_user_requests_to_view_their_tasks(self):
        response = self.client.get(reverse('student-meetings'), {'id': self.student.id})
        return response

    def when_a_user_requests_to_view_their_tasks_with_an_incorrect_http_post_method(self):
        response = self.client.post(reverse('student-meetings'))
        return response

    def when_the_user_with_an_invalid_id_requests_to_view_their_tasks(self):
        response = self.client.get(reverse('student-meetings'), {'id': 999})
        return response

    def then_we_get_back_a_response_code(self, response, response_code):
        self.assertEqual(response.status_code, response_code)

    def and_the_correct_number_of_meetings_are_returned(self, response):
        self.assertEqual(len(response.json()['meetings']), 2)
