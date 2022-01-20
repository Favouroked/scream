from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


from users.models import User

TEST_EMAIL = 'test@gmail.com'
TEST_PASSWORD = 'testCore`83'


# Create your tests here.
class UsersTests(APITestCase):

    def test_user_registration(self):
        url = reverse('users:register')
        data = {'email': TEST_EMAIL, 'password': TEST_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertIsNotNone(response.data.get('token', None))

    def test_user_registration_fail_with_invalid_email(self):
        url = reverse('users:register')
        data = {'email': 'abc123', 'password': TEST_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        User.objects.create_user(TEST_EMAIL, TEST_PASSWORD)
        url = reverse('users:login')
        data = {'email': TEST_EMAIL, 'password': TEST_PASSWORD}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertIsNotNone(response.data.get('token', None))

    def test_get_user_by_id(self):
        user = User.objects.create_user(TEST_EMAIL, TEST_PASSWORD)
        url = reverse('users:user_details', args=(user.id,))
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id', None), 1)
        self.assertEqual(response.data.get('email', None), TEST_EMAIL)
        self.assertIsNotNone(response.data.get('created_at', None))

