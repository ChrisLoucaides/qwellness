from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from user_management.models import Account
from user_management.views import user_login, signup

AN_EXAMPLE_LAST_NAME = 'User'

AN_EXAMPLE_FIRST_NAME = 'Test'

A_VALID_EMAIL_ADDRESS = 'test@example.com'

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

        self.the_user_is_not_logged_in_and_the_login_page_is_re_displayed(response)
        self.and_the_response_contains(response, AN_INVALID_CREDENTIALS_MESSAGE)

    def test_should_not_login_user_given_wrong_http_method(self):
        request = self.given_a_login_get_request()

        response = self.when_we_attempt_authentication(request)

        self.the_user_is_not_logged_in_and_the_login_page_is_re_displayed(response)

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
        self.assertEqual(response.url, reverse('dashboard'))

    @staticmethod
    def when_we_attempt_authentication(request):
        response = user_login(request)
        return response

    def and_the_response_contains(self, response, response_message):
        self.assertContains(response, response_message)

    def the_user_is_not_logged_in_and_the_login_page_is_re_displayed(self,
                                                                     response):  # TODO: Revisit this, add assertion to check for login page?
        self.assertEqual(response.status_code, 200)


class SignUpTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_success(self):
        request = self.given_a_sign_up_form_post_request_with(A_VALID_USERNAME, A_VALID_PASSWORD, A_VALID_PASSWORD,
                                                              A_VALID_EMAIL_ADDRESS, AN_EXAMPLE_FIRST_NAME,
                                                              AN_EXAMPLE_LAST_NAME)

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_a_new_user_is_created_and_we_redirect_them(response)

    def test_signup_invalid_form(self):
        request = self.given_an_invalid_signup_form_post_request()

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_the_user_is_not_created_and_the_signup_page_is_redisplayed(response)

    def test_signup_get_request(self):
        request = self.given_a_sign_up_form_get_request()

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_the_user_is_not_created_and_the_signup_page_is_redisplayed(response)

    def given_a_sign_up_form_get_request(self):
        request = self.factory.get(reverse('signup'))
        return request

    def given_a_sign_up_form_post_request_with(self, username, password, password_confirmation, email, first_name,
                                               last_name):
        request = self.factory.post(reverse('signup'), {
            'username': username,
            'password': password,
            'confirm_password': password_confirmation,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        return request

    def then_a_new_user_is_created_and_we_redirect_them(self, response):
        self.assertEqual(response.status_code, 302)

    def then_the_user_is_not_created_and_the_signup_page_is_redisplayed(self, response):
        self.assertEqual(response.status_code, 200)

    def given_an_invalid_signup_form_post_request(self):
        request = self.factory.post(reverse('signup'), {})
        return request

    @staticmethod
    def when_we_try_and_register_a_new_user(request):
        response = signup(request)
        return response
