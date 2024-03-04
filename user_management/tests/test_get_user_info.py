import json
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock
from user_management.views import get_user_info


class TestGetUserInfo(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()

    def test_get_user_info_authenticated(self):
        # Given
        user = self.User.objects.create_user(username='test_user', password='test_password', first_name='Test',
                                             role='admin')
        user.advisor = self.User.objects.create_user(username='test_advisor', password='test_password',
                                                     first_name='Advisor')
        user.save()
        request = self.factory.get('/get-user-info/')
        request.user = user

        # When
        response = get_user_info(request)

        # Then
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "role": user.role,
            "advisor": user.advisor.username if user.advisor else None
        }
        self.assertEqual(json.loads(response.content), expected_data)

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
