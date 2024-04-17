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

    def test_create_meeting_success(self):
        self.given_a_logged_in_student()
        meeting_data = self.and_a_filled_in_meeting_form_for(SEVENTEENTH_OF_APRIL_2024, TEN_AM)

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.then_the_meeting_is_scheduled(response)
        self.and_the_meeting_id_field_is_in_the_response(response)
        self.and_the_meeting_id_is_added_to_the_students_list_of__meeting_ids()
        self.and_the_value_of_the_new_meeting_id_is_in_the_response(response)

    def test_create_meeting_missing_fields(self):
        self.given_a_logged_in_student()

        meeting_data = {
            'id': self.student.id,
            'time': TEN_AM
        }

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_meeting_student_not_found(self):
        self.given_a_logged_in_student()

        meeting_data = {
            'id': 9999,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())

    def test_create_meeting_no_advisor_assigned(self):
        self.given_a_logged_in_student()

        self.student.advisor = None
        self.student.save()

        meeting_data = self.and_a_filled_in_meeting_form_for(SEVENTEENTH_OF_APRIL_2024, TEN_AM)

        response = self.when_the_user_requests_to_schedule_a_new_meeting(meeting_data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def given_a_logged_in_student(self):
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

    def and_a_filled_in_meeting_form_for(self, date, time):
        meeting_data = {
            'id': self.student.id,
            'date': date,
            'time': time
        }
        return meeting_data

    def when_the_user_requests_to_schedule_a_new_meeting(self, meeting_data):
        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')
        return response

    def then_the_meeting_is_scheduled(self, response):
        self.assertEqual(response.status_code, 201)

    def and_the_meeting_id_field_is_in_the_response(self, response):
        self.assertTrue('meeting_id' in response.json())

    def and_the_meeting_id_is_added_to_the_students_list_of__meeting_ids(self):
        self.assertTrue(Student.objects.get(id=self.student.id).advisor_meeting_ids)

    def and_the_value_of_the_new_meeting_id_is_in_the_response(self, response):
        self.assertIn(response.json()['meeting_id'], Student.objects.get(id=self.student.id).advisor_meeting_ids)
