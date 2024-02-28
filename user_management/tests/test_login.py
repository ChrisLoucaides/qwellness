from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from user_management.models import Account
from user_management.views import user_login

AN_INVALID_CREDENTIALS_MESSAGE = 'Invalid username or password'
A_VALID_USERNAME = 'testuser'
A_VALID_PASSWORD = 'testpassword'
AN_INVALID_PASSWORD = 'invalid'


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.username = A_VALID_USERNAME
        self.password = A_VALID_PASSWORD
        self.user = Account.objects.create_user(username=self.username, password=self.password)

    def test_should_login_user_given_valid_credentials(self):
        request = self.given_a_login_post_request_with_credentials(self.username, self.password)

        response = self.when_we_attempt_authentication(request)

        self.then_the_user_is_logged_in_and_redirected(response)

    def test_should_not_login_user_given_invalid_credentials(self):
        request = self.given_a_login_post_request_with_credentials(self.username, AN_INVALID_PASSWORD)

        response = self.when_we_attempt_authentication(request)

        self.then_the_user_is_not_logged_in_and_the_login_page_is_re_displayed(response)
        self.and_the_response_contains(response, AN_INVALID_CREDENTIALS_MESSAGE)

    def test_should_not_login_user_given_wrong_http_method(self):
        request = self.given_a_login_get_request()

        response = self.when_we_attempt_authentication(request)

        self.then_the_user_is_not_logged_in_and_the_login_page_is_re_displayed(response)

    def given_a_login_get_request(self):
        request = self.factory.get(reverse('login'))
        return request

    def given_a_login_post_request_with_credentials(self, username, password):
        request = self.factory.post(reverse('login'), {'username': username, 'password': password})

        def get_response():
            return None

        # noinspection PyTypeChecker
        middleware = SessionMiddleware(get_response)  # Create session as it is needed to create middleware object
        middleware.process_request(request)
        return request

    def then_the_user_is_logged_in_and_redirected(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))  # TODO FYP-10: Change URL to frontend

    @staticmethod
    def when_we_attempt_authentication(request):
        response = user_login(request)
        return response

    def and_the_response_contains(self, response, response_message):
        self.assertContains(response, response_message)

    def then_the_user_is_not_logged_in_and_the_login_page_is_re_displayed(self,
                                                                          response):
        self.assertEqual(response.status_code, 200)
