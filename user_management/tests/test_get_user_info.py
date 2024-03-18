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
        response_data = json.loads(response.content.decode('utf-8'))
        for key in expected_data:
            self.assertEqual(response_data[key], expected_data[key])

        self.assertTrue('last_login_time' in response_data)

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
    def and_the_user_is_saved(user):
        user.save()

    def test_get_user_info_request_should_redirect_to_login_given_no_authentication(self):
        to_get_info = self.given_a_request_is_made_to_the_get_user_info_endpoint()
        self.and_the_user_is_not_authenticated(to_get_info)

        response = self.when_a_request_is_made(to_get_info)

        self.then_the_user_is_redirected(response)
        self.to_the_login_page(response)

    def then_the_user_is_redirected(self, response):
        self.assertEqual(response.status_code, 302)

    def given_a_request_is_made_to_the_get_user_info_endpoint(self):
        request = self.factory.get('/get-user-info/')
        return request

    def to_the_login_page(self, response):
        self.assertIn('Location', response.headers)
        self.assertIn('/accounts/login/', response.headers['Location'])

    @staticmethod
    def and_the_user_is_not_authenticated(request):
        request.user = Mock(is_authenticated=False)

    @staticmethod
    def when_a_request_is_made(request):
        return get_user_info(request)
