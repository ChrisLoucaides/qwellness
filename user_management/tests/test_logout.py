from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from user_management.views import user_logout


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_logout_when_user_is_logged_in(self):
        # Given
        user = get_user_model().objects.create_user(username='test_user', password='password')
        request = self.factory.get(reverse('user_logout'))
        request.user = user

        # Create a session (Given)
        middleware = SessionMiddleware(lambda request: None)  # TODO FYP-12: Refactor me
        middleware.process_request(request)

        # When
        response = user_logout(request)

        # Then
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    def test_user_logout_when_user_is_not_logged_in(self):
        # Given
        request = self.factory.get(reverse('user_logout'))
        request.user = AnonymousUser()

        # When
        response = user_logout(request)

        # Then
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
