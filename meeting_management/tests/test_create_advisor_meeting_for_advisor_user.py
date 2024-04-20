from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Advisor, Student
import json

SEVENTEENTH_OF_APRIL_2024 = '2024-04-17'
TEN_AM = '10:00'

VALID_ADVISOR_PASSWORD = 'password'
VALID_ADVISOR_EMAIL = 'advisor@example.com'
VALID_ADVISOR_USERNAME = 'advisor'

VALID_STUDENT_PASSWORD = 'password'
VALID_STUDENT_EMAIL = 'student@example.com'
VALID_STUDENT_USERNAME = 'student'


class MeetingManagementTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.advisor = Advisor.objects.create_user(username=VALID_ADVISOR_USERNAME, email=VALID_ADVISOR_EMAIL,
                                                   password=VALID_ADVISOR_PASSWORD)
        self.student = Student.objects.create_user(username=VALID_STUDENT_USERNAME, email=VALID_STUDENT_EMAIL,
                                                   password=VALID_STUDENT_PASSWORD)

        self.nonexistent_student_username = 'nonexistent_student'
        self.nonexistent_student = Student.objects.create_user(username=self.nonexistent_student_username,
                                                               email='nonexistent@student.com',
                                                               password='nonexistent_password')

        self.student.advisor = self.advisor
        self.student.save()

    def test_advisor_should_be_able_to_schedule_student_meeting(self):
        self.given_a_logged_in_advisor()
        meeting_data = self.and_a_filled_in_meeting_form_for_student(SEVENTEENTH_OF_APRIL_2024, TEN_AM)

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_the_meeting_is_scheduled(response)
        self.and_the_meeting_id_field_is_in_the_response(response)

    def test_should_not_schedule_student_meeting_given_missing_fields(self):
        self.given_a_logged_in_advisor()
        meeting_data = self.and_a_filled_in_meeting_form_with_missing_fields()

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 400)
        self.and_there_is_an_error_in_the_response(response)

    def test_should_not_schedule_meeting_if_advisor_does_not_exist(self):
        self.given_a_logged_in_advisor()

        meeting_data = self.and_a_filled_in_meeting_form_with_invalid_advisor_id()

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 404)
        self.and_there_is_an_error_in_the_response(response)

    def test_should_not_schedule_meeting_if_student_does_not_exist(self):
        self.given_a_logged_in_advisor()
        meeting_data = self.and_a_filled_in_meeting_form_with_invalid_student_username()

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 400)
        self.and_there_is_an_error_in_the_response(response)

    def given_a_logged_in_advisor(self):
        self.client.login(username=VALID_ADVISOR_USERNAME, password=VALID_ADVISOR_PASSWORD)

    def and_a_filled_in_meeting_form_for_student(self, date, time):
        meeting_data = {
            'id': self.advisor.id,
            'student': VALID_STUDENT_USERNAME,
            'date': date,
            'time': time
        }
        return meeting_data

    def and_a_filled_in_meeting_form_with_missing_fields(self):
        meeting_data = {
            'id': self.advisor.id,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }
        return meeting_data

    @staticmethod
    def and_a_filled_in_meeting_form_with_invalid_advisor_id():
        meeting_data = {
            'id': 9999,
            'student': VALID_STUDENT_USERNAME,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }
        return meeting_data

    def and_a_filled_in_meeting_form_with_invalid_student_username(self):
        meeting_data = {
            'id': self.advisor.id,
            'student': 'nonexistent_student',
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }
        return meeting_data

    def when_the_user_requests_to_schedule_a_new_meeting(self, meeting_data):
        response = self.client.post(reverse('advisor-meeting-for-advisor'), data=json.dumps(meeting_data),
                                    content_type='application/json')
        return response

    def then_the_meeting_is_scheduled(self, response):
        self.assertEqual(response.status_code, 201)

    def then_we_get_a_response_code_of(self, response, response_code):
        self.assertEqual(response.status_code, response_code)

    def and_there_is_an_error_in_the_response(self, response):
        self.assertTrue('error' in response.json())

    def and_the_meeting_id_field_is_in_the_response(self, response):
        self.assertTrue('meeting_id' in response.json())
