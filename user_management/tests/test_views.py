from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from user_management.models import Account
from user_management.views import user_login, signup


class UserLoginTestCase(TestCase):  # TODO: refactor me
    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = Account.objects.create_user(username=self.username, password=self.password)

    def test_login_successful(self):
        request = self.factory.post(reverse('login'), {'username': self.username, 'password': self.password})
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()

        response = user_login(request)
        self.assertEqual(response.status_code, 302)

    def test_invalid_credentials(self):
        request = self.factory.post(reverse('login'), {'username': self.username, 'password': 'wrongpassword'})
        response = user_login(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_get_request(self):
        request = self.factory.get(reverse('login'))
        response = user_login(request)
        self.assertEqual(response.status_code, 200)


class SignUpTestCase(TestCase):  # TODO: refactor me
    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_success(self):
        request = self.factory.post(reverse('signup'), {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })
        response = signup(request)
        print(response.content)
        self.assertEqual(response.status_code, 302)

    def test_signup_invalid_form(self):
        request = self.factory.post(reverse('signup'), {})
        response = signup(request)
        self.assertEqual(response.status_code, 200)

    def test_signup_get_request(self):
        request = self.factory.get(reverse('signup'))
        response = signup(request)
        self.assertEqual(response.status_code, 200)
