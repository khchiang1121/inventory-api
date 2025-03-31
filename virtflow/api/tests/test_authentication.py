from django.urls import reverse
from rest_framework import status
from .base import APITestSetup

class AuthenticationTests(APITestSetup):
    """Test authentication endpoints"""
    
    def test_user_login(self):
        """Test user login endpoint"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data) 