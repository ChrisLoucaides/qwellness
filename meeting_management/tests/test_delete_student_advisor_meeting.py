import json
from django.test import TestCase, Client
from django.urls import reverse
from user_management.models import Student, Advisor
from meeting_management.models import Meeting


class DeleteStudentMeetingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(username='test_student')
        self.advisor = Advisor.objects.create(username='test_advisor')

    def test_should_delete_meeting_associated_to_a_student(self):
        meeting = self.given_a_valid_meeting()
        self.given_the_user_is_logged_in()

        response = self.when_the_user_requests_to_delete_a_valid_meeting(meeting)

        self.then_the_meeting_is_deleted(response)
        self.and_we_get_a_success_message(response)

    def test_should_not_delete_meeting_given_missing_id(self):
        self.given_the_user_is_logged_in()

        response = self.when_the_user_requests_to_delete_an_invalid_meeting()

        self.then_the_meeting_is_not_deleted_and_we_get_a_response_of(response, 400)
        self.and_an_error_message_of(response, {'error': 'Meeting ID is required'})

    def test_should_not_delete_meeting_given_invalid_id(self):
        self.given_the_user_is_logged_in()

        response = self.when_the_user_makes_a_request_with_an_invalid_meeting_id()

        self.then_the_meeting_is_not_deleted_and_we_get_a_response_of(response, 404)
        self.and_an_error_message_of(response, {'error': 'Meeting not found'})

    def test_should_not_delete_meeting_given_invalid_method(self):
        self.given_the_user_is_logged_in()

        response = self.when_the_user_makes_a_request_with_an_invalid_http_method()

        self.then_the_meeting_is_not_deleted_and_we_get_a_response_of(response, 405)
        self.and_an_error_message_of(response, {'error': 'Method not allowed'})

    def test_should_not_delete_meeting_given_unauthenticated_user(self):
        meeting = self.given_a_valid_meeting()

        response = self.when_the_user_requests_to_delete_a_valid_meeting(meeting)

        self.then_the_meeting_is_not_deleted_and_the_user_is_redirected(response)

    def given_the_user_is_logged_in(self):
        self.client.force_login(self.student)

    def given_a_valid_meeting(self):
        return Meeting.objects.create(student=self.student, advisor=self.advisor, date='2024-05-15', time='08:00:00')

    def when_the_user_requests_to_delete_a_valid_meeting(self, meeting):
        return self.client.delete(reverse('remove-meeting'), data=json.dumps({'id': meeting.id}),
                                  content_type='application/json')

    def when_the_user_makes_a_request_with_an_invalid_http_method(self):
        response = self.client.post(reverse('remove-meeting'))
        return response

    def when_the_user_requests_to_delete_an_invalid_meeting(self):
        response = self.client.delete(reverse('remove-meeting'), data=json.dumps({}),
                                      content_type='application/json')
        return response

    def when_the_user_makes_a_request_with_an_invalid_meeting_id(self):
        response = self.client.delete(reverse('remove-meeting'), data=json.dumps({'id': 999}),
                                      content_type='application/json')
        return response

    def then_the_meeting_is_deleted(self, response):
        self.assertEqual(response.status_code, 200)

    def then_the_meeting_is_not_deleted_and_we_get_a_response_of(self, response, response_code):
        self.assertEqual(response.status_code, response_code)

    def then_the_meeting_is_not_deleted_and_the_user_is_redirected(self, response):
        self.assertEqual(response.status_code, 302)

    def and_we_get_a_success_message(self, response):
        self.assertTrue(json.loads(response.content)['success'])

    def and_an_error_message_of(self, response, error):
        self.assertEqual(response.json(), error)
