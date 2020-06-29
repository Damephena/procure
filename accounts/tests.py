# from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
class UserAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.client.post('/api/v1/rest-auth/registration/', data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'test@example.com',
        })

        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ self.token)
    
    def test_user_profile_retrieval(self):
        data = {
            'email':'test@example.com'
        }
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
