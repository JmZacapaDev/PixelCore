from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')

    def test_user_registration(self):
        """
        Ensure we can register a new user and receive a success response.
        """
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['username'], 'testuser')
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """
        Ensure user registration fails with password mismatch.
        """
        data = {
            'email': 'test2@example.com',
            'username': 'testuser2',
            'password': 'password123',
            'password2': 'password321'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_duplicate_email(self):
        """
        Ensure user registration fails with a duplicate email.
        """
        self.test_user_registration() # Register first user
        data = {
            'email': 'test@example.com', # Duplicate email
            'username': 'anotheruser',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_login(self):
        """
        Ensure an existing user can log in and receive JWT tokens.
        """
        # First, register a user
        self.client.post(self.register_url, {
            'email': 'login@example.com',
            'username': 'loginuser',
            'password': 'password123',
            'password2': 'password123'
        }, format='json')

        # Then, attempt to log in
        login_data = {
            'email': 'login@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Ensure login fails with invalid credentials.
        """
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)