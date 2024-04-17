from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Advisor, Student
import json

SEVENTEENTH_OF_APRIL_2024 = '2024-04-17'
TEN_AM = '10:00'

VALID_STUDENT_PASSWORD = 'password'
VALID_STUDENT_EMAIL = 'student@example.com'
VALID_STUDENT_USERNAME = 'student'

VALID_ADVISOR_EMAIL = 'advisor@example.com'
VALID_ADVISOR_PASSWORD = 'password'
VALID_ADVISOR_USERNAME = 'advisor'


class MeetingManagementTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.advisor = Advisor.objects.create_user(username=VALID_ADVISOR_USERNAME, email=VALID_ADVISOR_EMAIL,
                                                   password=VALID_ADVISOR_PASSWORD)
        self.student = Student.objects.create_user(username=VALID_STUDENT_USERNAME, email=VALID_STUDENT_EMAIL,
                                                   password=VALID_STUDENT_PASSWORD)

        self.student.advisor = self.advisor
        self.student.save()

    def test_student_should_be_able_to_schedule_advisor_meeting(self):
        self.given_a_logged_in_student()
        meeting_data = self.and_a_filled_in_meeting_form_for(SEVENTEENTH_OF_APRIL_2024, TEN_AM)

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_the_meeting_is_scheduled(response)
        self.and_the_meeting_id_field_is_in_the_response(response)
        self.and_the_meeting_id_is_added_to_the_students_list_of__meeting_ids()
        self.and_the_value_of_the_new_meeting_id_is_in_the_response(response)

    def test_should_not_schedule_advisor_meeting_given_missing_fields(self):
        self.given_a_logged_in_student()
        meeting_data = self.and_a_filled_in_meeting_form_with_no_date()

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 400)
        self.and_there_is_an_error_in_the_response(response)

    def test_should_not_schedule_advisor_meeting_if_student_does_not_exist(self):
        self.given_a_logged_in_student()

        meeting_data = self.and_a_filled_in_meeting_form_with_invalid_id()

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 404)
        self.and_there_is_an_error_in_the_response(response)

    def test_should_not_schedule_meeting_if_no_advisor_assigned_to_student(self):
        self.given_a_logged_in_student()
        self.and_that_student_does_not_have_an_advisor_assigned()
        meeting_data = self.and_a_filled_in_meeting_form_for(SEVENTEENTH_OF_APRIL_2024, TEN_AM)

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_we_get_a_response_code_of(response, 400)
        self.and_there_is_an_error_in_the_response(response)

    def given_a_logged_in_student(self):
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

    def and_a_filled_in_meeting_form_for(self, date, time):
        meeting_data = {
            'id': self.student.id,
            'date': date,
            'time': time
        }
        return meeting_data

    def and_that_student_does_not_have_an_advisor_assigned(self):
        self.student.advisor = None
        self.student.save()

    def when_the_user_requests_to_schedule_a_new_meeting(self, meeting_data):
        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
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

    def and_the_meeting_id_is_added_to_the_students_list_of__meeting_ids(self):
        self.assertTrue(Student.objects.get(id=self.student.id).advisor_meeting_ids)

    def and_the_value_of_the_new_meeting_id_is_in_the_response(self, response):
        self.assertIn(response.json()['meeting_id'], Student.objects.get(id=self.student.id).advisor_meeting_ids)

    def and_a_filled_in_meeting_form_with_no_date(self):
        meeting_data = {
            'id': self.student.id,
            'time': TEN_AM
        }
        return meeting_data

    @staticmethod
    def and_a_filled_in_meeting_form_with_invalid_id():
        meeting_data = {
            'id': 9999,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }
        return meeting_data
