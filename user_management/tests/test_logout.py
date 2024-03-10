from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_management.views import user_logout


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_should_logout_when_user_is_logged_in(self):
        request = self.given_a_logout_request_from_a_logged_in_user()

        response = self.when_we_attempt_to_logout(request)

        self.then_the_user_is_logged_out_and_redirected_to_the_login_page(response)

    def then_the_user_is_logged_out_and_redirected_to_the_login_page(self, response):
        self.assertEqual(response.status_code, 302)

    def given_a_logout_request_from_a_logged_in_user(self):
        user = get_user_model().objects.create_user(username='test_user', password='password')
        request = self.factory.get(reverse('user_logout'))
        request.user = user

        def get_response():
            return None

        # noinspection PyTypeChecker
        middleware = SessionMiddleware(get_response)  # Create session as it is needed to create middleware object
        middleware.process_request(request)
        return request

    def test_should_not_logout_when_user_is_not_logged_in(self):
        # Given
        request = self.given_a_logout_request_from_a_non_logged_in_user()

        # When
        response = self.when_we_attempt_to_logout(request)

        # Then
        self.assertEqual(response.status_code, 302)

    def given_a_logout_request_from_a_non_logged_in_user(self):
        request = self.factory.get(reverse('user_logout'))
        request.user = AnonymousUser()
        return request

    @staticmethod
    def when_we_attempt_to_logout(request):
        response = user_logout(request)
        return response
