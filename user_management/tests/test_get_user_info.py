import json
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock
from user_management.views import get_user_info


class TestGetUserInfo(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()

    def test_should_return_authenticated_user_data(self):
        user = self.given_an_authenticated_student_user_with_credentials('test_user', 'test_password', 'Test')
        user.advisor = self.and_an_advisor_with_credentials('test_advisor', 'test_password', 'Advisor')
        self.and_the_user_is_saved(user)

        response = self.when_a_request_is_made(self.to_the_get_user_info_endpoint_with_user(user))

        expected_data = self.then_the_response_comes_back_as_200(response, user)
        self.and_the_content_matches_with_our_expected_data(expected_data, response)

    def and_the_content_matches_with_our_expected_data(self, expected_data, response):
        self.assertEqual(json.loads(response.content), expected_data)

    def then_the_response_comes_back_as_200(self, response, user):
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "role": user.role,
            "advisor": user.advisor.username if user.advisor else None
        }
        return expected_data

    def to_the_get_user_info_endpoint_with_user(self, user):
        request = self.factory.get('/get-user-info/')
        request.user = user
        return request

    def and_an_advisor_with_credentials(self, username, password, first_name):
        return self.User.objects.create_user(username=username, password=password,
                                             first_name=first_name)

    def given_an_authenticated_student_user_with_credentials(self, username, password, first_name):
        return self.User.objects.create_user(username=username, password=password, first_name=first_name,
                                             role='student')

    @staticmethod
    def when_a_request_is_made(request):
        return get_user_info(request)

    @staticmethod
    def and_the_user_is_saved(user):
        user.save()

    def test_get_user_info_unauthenticated(self):
        # Given
        request = self.factory.get('/get-user-info/')
        request.user = Mock(is_authenticated=False)

        # When
        response = get_user_info(request)

        # Then
        self.assertEqual(response.status_code, 302)
        self.assertIn('Location', response.headers)
        self.assertIn('/accounts/login/', response.headers['Location'])
