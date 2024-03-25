from django.test import TestCase, RequestFactory
from django.urls import reverse
from user_management.models import Advisor
from user_management.views import signup

AN_EXAMPLE_LAST_NAME = 'User'
AN_EXAMPLE_FIRST_NAME = 'Test'
A_VALID_EMAIL_ADDRESS = 'test@example.com'
AN_INVALID_CREDENTIALS_MESSAGE = 'Invalid username or password'
A_VALID_USERNAME = 'testuser'
A_VALID_PASSWORD = 'testpassword'
AN_INVALID_PASSWORD = 'invalid'
A_VALID_ADVISOR_USERNAME = "ValidAdvisor"


class SignUpTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.advisor = Advisor.objects.create(username=A_VALID_ADVISOR_USERNAME)

    def test_should_register_a_new_user_and_redirect_them_to_login_page(self):
        request = self.given_a_sign_up_form_post_request_with(
            A_VALID_USERNAME, A_VALID_PASSWORD, A_VALID_PASSWORD,
            A_VALID_EMAIL_ADDRESS, AN_EXAMPLE_FIRST_NAME,
            AN_EXAMPLE_LAST_NAME, self.advisor.id
        )

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_a_new_user_is_created(response)

    def test_should_not_register_a_new_user_and_should_redisplay_signup_page(self):
        request = self.given_an_invalid_signup_form_post_request()

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_the_user_is_not_created_and_the_signup_page_is_redisplayed(response)

    def test_should_not_register_user_given_wrong_http_method(self):
        request = self.given_a_sign_up_form_get_request()

        response = self.when_we_try_and_register_a_new_user(request)

        self.then_the_user_is_not_created_and_the_signup_page_is_redisplayed(response)

    def given_a_sign_up_form_get_request(self):
        request = self.factory.get(reverse('signup'))
        return request

    def given_a_sign_up_form_post_request_with(self, username, password, password_confirmation, email, first_name,
                                               last_name, advisor):
        request = self.factory.post(reverse('signup'), {
            'username': username,
            'password': password,
            'confirm_password': password_confirmation,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'advisor': advisor
        })
        return request

    def then_a_new_user_is_created(self, response):
        self.assertEqual(response.status_code, 200)

    def then_the_user_is_not_created_and_the_signup_page_is_redisplayed(self, response):
        self.assertEqual(response.status_code, 200)

    def given_an_invalid_signup_form_post_request(self):
        request = self.factory.post(reverse('signup'), {})
        return request

    @staticmethod
    def when_we_try_and_register_a_new_user(request):
        response = signup(request)
        return response
