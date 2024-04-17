from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Advisor, Student
import json


class MeetingManagementTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.advisor = Advisor.objects.create_user(username='advisor', email='advisor@example.com', password='password')
        self.student = Student.objects.create_user(username='student', email='student@example.com', password='password')

        self.student.advisor = self.advisor
        self.student.save()

    def test_create_meeting_success(self):
        self.client.login(username='advisor', password='password')

        meeting_data = {
            'id': self.student.id,
            'date': '2024-04-17',
            'time': '10:00'
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        print(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertTrue('meeting_id' in response.json())

        student = Student.objects.get(id=self.student.id)
        self.assertTrue(student.advisor_meeting_ids)
        self.assertIn(response.json()['meeting_id'], student.advisor_meeting_ids)

    def test_create_meeting_missing_fields(self):
        self.client.login(username='advisor', password='password')

        meeting_data = {
            'id': self.student.id,
            'time': '10:00'
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_create_meeting_student_not_found(self):
        self.client.login(username='advisor', password='password')

        meeting_data = {
            'id': 9999,
            'date': '2024-04-17',
            'time': '10:00'
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())

    def test_create_meeting_no_advisor_assigned(self):
        self.client.login(username='advisor', password='password')

        self.student.advisor = None
        self.student.save()

        meeting_data = {
            'id': self.student.id,
            'date': '2024-04-17',
            'time': '10:00'
        }

        response = self.client.post(reverse('advisor-meeting-for-student'), data=json.dumps(meeting_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())
