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

    def test_filter_advisors_students_returns_students(self):
        # Given advisor and student
        advisor = Advisor.objects.create(username='test_advisor')
        student = Student.objects.create(username='test_student', advisor=advisor)

        # When we make a request
        request = self.factory.get('/filter-advisors-students/')
        request.user = Mock(is_authenticated=True)

        # with an advisor username
        request.GET = request.GET.copy()
        request.GET['username'] = 'test_advisor'

        # and we filter the students
        response = filter_advisors_students(request)

        # Check if response is successful
        self.assertEqual(response.status_code, 200)

        # Deserialize response content
        response_data = json.loads(response.content.decode('utf-8'))

        # Check if students are returned
        self.assertIn('students', response_data)
        self.assertEqual(len(response_data['students']), 1)

        # Check student details
        returned_student = response_data['students'][0]
        self.assertEqual(returned_student['username'], 'test_student')
        # Add more assertions for other student details if needed

    def test_filter_advisors_students_no_authentication(self):
        # Create a mock request without authentication
        request = self.factory.get('/filter-advisors-students/')
        request.user = Mock(is_authenticated=False)

        # Call the view function
        response = filter_advisors_students(request)

        # Check if response redirects to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertIn('/accounts/login/', response.headers['Location'])
