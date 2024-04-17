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
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

        meeting_data = {
            'id': self.student.id,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue('meeting_id' in response.json())

        student = Student.objects.get(id=self.student.id)
        self.assertTrue(student.advisor_meeting_ids)
        self.assertIn(response.json()['meeting_id'], student.advisor_meeting_ids)

    def test_create_meeting_missing_fields(self):
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

        meeting_data = {
            'id': self.student.id,
            'time': TEN_AM
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_meeting_student_not_found(self):
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

        meeting_data = {
            'id': 9999,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())

    def test_create_meeting_no_advisor_assigned(self):
        self.client.login(username=VALID_STUDENT_USERNAME, password=VALID_STUDENT_PASSWORD)

        self.student.advisor = None
        self.student.save()

        meeting_data = {
            'id': self.student.id,
            'date': SEVENTEENTH_OF_APRIL_2024,
            'time': TEN_AM
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())
