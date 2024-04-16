import json
from django.test import TestCase, Client
from user_management.models import Student, Advisor
from meeting_management.models import Meeting


class CreateMeetingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')
        self.advisor = Advisor.objects.create(username='test_advisor')
        self.client.force_login(self.student)

    def test_should_create_a_new_meeting_for_a_student(self):
        data = self.given_a_valid_meeting_payload()

        response = self.when_a_post_request_is_made_to_create_meeting_endpoint(data)

        self.then_a_new_meeting_is_created(response)

        response_data = response.json()
        self.and_we_get_a_success_response(response_data)

        meeting_id = response_data['meeting_id']
        self.and_the_meeting_has_been_added_to_the_database(meeting_id)

        Meeting.objects.filter(pk=meeting_id).delete()  # Clean Up

    def test_should_create_a_new_meeting_for_an_advisor(self):
        data = self.given_a_valid_meeting_payload_for_advisor()

        response = self.when_a_post_request_is_made_to_create_meeting_endpoint(data)

        self.then_a_new_meeting_is_created(response)

        response_data = response.json()
        self.and_we_get_a_success_response(response_data)

        meeting_id = response_data['meeting_id']
        self.and_the_meeting_has_been_added_to_the_database(meeting_id)

        Meeting.objects.filter(pk=meeting_id).delete()  # Clean Up

    def test_should_not_create_meeting_given_invalid_user_id(self):
        data = self.given_an_invalid_user_id_in_payload()

        response = self.when_a_post_request_is_made_to_create_meeting_endpoint(data)

        self.then_we_get_a_404(response)
        response_data = response.json()
        self.and_the_response_contains_an_error_message(response_data)

    def given_a_valid_meeting_payload(self):
        data = {
            'user_id': self.student.id,
            'date_and_time': '2024-04-16T10:00:00'
        }
        return data

    def given_a_valid_meeting_payload_for_advisor(self):
        data = {
            'user_id': self.advisor.id,
            'date_and_time': '2024-04-16T10:00:00',
            'student_username': self.student.username
        }
        return data

    @staticmethod
    def given_an_invalid_user_id_in_payload():
        data = {
            'user_id': 9999,
            'date_and_time': '2024-04-16T10:00:00'
        }
        return data

    def when_a_post_request_is_made_to_create_meeting_endpoint(self, data):
        return self.client.post('/advisor-meeting/', data=json.dumps(data), content_type='application/json')

    def then_a_new_meeting_is_created(self, response):
        self.assertEqual(response.status_code, 201)

    def and_we_get_a_success_response(self, response_data):
        self.assertTrue(response_data['success'])

    def and_the_meeting_has_been_added_to_the_database(self, meeting_id):
        self.assertIsNotNone(Meeting.objects.filter(pk=meeting_id).first())

    def then_we_get_a_404(self, response):
        self.assertEqual(response.status_code, 404)

    def and_the_response_contains_an_error_message(self, response_data):
        self.assertIn('error', response_data)
