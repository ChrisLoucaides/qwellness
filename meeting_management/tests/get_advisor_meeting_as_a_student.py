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

    def test_get_student_meetings(self):
        url = reverse('student-meetings')
        self.client.force_login(self.student)

        response = self.client.get(url, {'id': self.student.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['meetings']), 2)

    def test_get_student_meetings_invalid_method(self):
        url = reverse('student-meetings')

        self.client.force_login(self.student)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 405)

    def test_get_student_meetings_invalid_student_id(self):
        url = reverse('student-meetings')

        self.client.force_login(self.student)

        response = self.client.get(url, {'id': 999})

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())
