from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


User = get_user_model()

class AuthAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.email = 'user@example.com'
        self.password = 'TestPass123'

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'name': 'febincf',
            'email': self.email,
            'password': self.password,
            'age': 25
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.email)

    def test_token_obtain_success(self):
        User.objects.create_user(email=self.email, password=self.password)

        response = self.client.post(self.token_url, {
            'email': self.email,
            'password': self.password
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_invalid_credentials(self):
        User.objects.create_user(email=self.email, password=self.password)

        response = self.client.post(self.token_url, {
            'email': self.email,
            'password': 'wrongpass'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)