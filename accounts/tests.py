from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UserTestCase(APITestCase):
    '''
    Test cases for regular `user` usertype.
    '''
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

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_user_profile_retrieval(self):
        data = {
            'email':'test@example.com'
        }
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])

    def test_regular_user_cannot_retrieve_all_users_profiles(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_retrieve_all_admins_profile(self):
        response = self.client.get(reverse('admin-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTestCase(APITestCase):
    '''
    Test cases for `admin` usertype.
    '''
    def setUp(self):
        self.client = APIClient()
        self.admin = self.client.post('/api/v1/accounts/admin/register/', data={
            'first_name': 'test',
            'last_name': 'admin',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'admin@example.com',
        })
        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'admin@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_admin_profile_retrieval(self):
        data = {
            'email':'admin@example.com'
        }
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])

    def test_admin_can_retrieve_all_users_profiles(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_retrieve_all_admins_profile(self):
        response = self.client.get(reverse('admin-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
