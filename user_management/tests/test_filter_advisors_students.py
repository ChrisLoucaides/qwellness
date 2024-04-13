import json
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from user_management.views import filter_advisors_students
from user_management.models import Student, Advisor
from unittest.mock import Mock


class TestFilterAdvisorsStudents(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()

    def test_should_filter_all_students_based_on_advisor(self):
        advisor = self.given_an_advisor_with_username('test_advisor')
        # noinspection PyUnusedLocal
        student = self.and_a_student_with_username_and_advisor('test_student', advisor)  # it is used, just not directly
        request = self.and_an_authenticated_advisor_makes_a_request_to_get_a_list_of_their_students()

        response = self.when_we_filter_the_advisors_students(request)

        self.then_we_receive_a_200_response_code(response)

        response_data = self.and_deserialize_the_response_content(response)

        self.and_all_students_are_in_the_response(response_data)
        self.and_the_student_details_are_correct(response_data)

    def and_the_student_details_are_correct(self, response_data):
        returned_student = response_data['students'][0]
        self.assertEqual(returned_student['username'], 'test_student')

    def and_all_students_are_in_the_response(self, response_data):
        self.assertIn('students', response_data)
        self.assertEqual(len(response_data['students']), 1)

    def then_we_receive_a_200_response_code(self, response):
        self.assertEqual(response.status_code, 200)

    def and_an_authenticated_advisor_makes_a_request_to_get_a_list_of_their_students(self):
        request = self.factory.get('/filter-advisors-students/')
        request.user = Mock(is_authenticated=True)
        request.GET = request.GET.copy()
        request.GET['username'] = 'test_advisor'
        return request

    @staticmethod
    def and_deserialize_the_response_content(response):
        return json.loads(response.content.decode('utf-8'))

    @staticmethod
    def and_a_student_with_username_and_advisor(username, advisor):
        return Student.objects.create(username=username, advisor=advisor)

    @staticmethod
    def given_an_advisor_with_username(username):
        advisor = Advisor.objects.create(username=username)
        return advisor

    def test_should_not_returned_filtered_students_given_no_authentication(self):

        request = self.when_a_non_authenticated_user_makes_a_request_to_get_a_list_of_their_students()

        response = self.when_we_filter_the_advisors_students(request)

        self.then_we_redirect_the_user_to_the_login_page(response)

    def then_we_redirect_the_user_to_the_login_page(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertIn('/accounts/login/', response.headers['Location'])

    def when_a_non_authenticated_user_makes_a_request_to_get_a_list_of_their_students(self):
        request = self.factory.get('/filter-advisors-students/')
        request.user = Mock(is_authenticated=False)
        return request

    @staticmethod
    def when_we_filter_the_advisors_students(request):
        return filter_advisors_students(request)
