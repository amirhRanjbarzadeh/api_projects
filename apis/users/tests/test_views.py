from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class JWTTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        login_url = reverse('users:token_obtain_pair')
        response = self.client.post(login_url, {'username': 'testuser', 'password': 'testpassword123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data['access']

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class CreateUserViewTest(APITestCase):
    def test_create_user_valid(self):
        url = reverse('users:signup')
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")

    def test_create_user_invalid(self):
        url = reverse('users:signup')
        data = {
            "username": "",
            "password": "short"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class DeactivateUserViewTest(JWTTestCase):
    def test_deactivate_user(self):
        self.authenticate()

        url = reverse('users:deactivate')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.data["detail"], "Account Deactivated")

    def test_unauthenticated_user_deactivate(self):
        url = reverse('users:deactivate')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordViewTest(JWTTestCase):
    def test_change_password_valid(self):
        self.authenticate()
        url = reverse('users:change_password')
        response = self.client.post(url, {'old_password': "testpassword123",
                                          "new_password": "testpasswordchanged123",
                                          "new_password_again": "testpasswordchanged123"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password changed successfully")

    def test_change_password_dont_match(self):
        self.authenticate()
        url = reverse('users:change_password')
        response = self.client.post(url, {'old_password': "testpassword123",
                                          "new_password": "testchanged1",
                                          "new_password_again": "anothertestchaned1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The new passwords do not match.", response.data["non_field_errors"])

    def test_change_password_invalid(self):
        self.authenticate()
        url = reverse('users:change_password')
        response = self.client.post(url, {'old_password': "incorrectpass",
                                          "new_password": "testchanged1",
                                          "new_password_again": "testchanged1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Old password is incorrect", response.data["old_password"])

    def test_change_password_unauthenticated(self):
        url = reverse('users:change_password')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserUpdateViewTest(JWTTestCase):
    def test_user_update(self):
        self.authenticate()
        url = reverse('users:user_update')
        data = {
            "username": "updateduser",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(response.data["detail"], "User updated successfully")

    def test_user_update_unauthenticated(self):
        url = reverse('users:user_update')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


