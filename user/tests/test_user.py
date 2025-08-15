from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


REGISTER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token_obtain_pair")
MANAGE_URL = reverse("user:manage_user")
REFRESH_URL = reverse("user:token_refresh")


class AccountsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "email": "testemail@test.com",
            "password": "testpassword",
        }
        self.client.post(REGISTER_URL, self.user_data)

    def test_create_user_without_username(self):
        user_data = {
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "email": "test@test.com",
            "password": "testpassword",
        }

        response = self.client.post(REGISTER_URL, user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertEqual(user_data["email"], response.data["email"])

    def test_create_users_with_duplicate_email(self):
        user_data = {
            "first_name": "testfirst",
            "last_name": "testlast",
            "email": "test_1@test.com",
            "password": "testpassword",
        }
        response1 = self.client.post(REGISTER_URL, user_data)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        user_data_2 = {
            "first_name": "testfirstduplicate",
            "last_name": "testlastduplicate",
            "email": "test_1@test.com",
            "password": "testpassword",
        }
        response2 = self.client.post(REGISTER_URL, user_data_2)

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response2.data["email"][0],
            "user with this email address already exists.",
        )

    def test_user_get_tokens(self):
        token_data = {
            "email": "testemail@test.com",
            "password": "testpassword",
        }
        response = self.client.post(TOKEN_URL, token_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh(self):
        token_data = {
            "email": "testemail@test.com",
            "password": "testpassword",
        }
        response = self.client.post(TOKEN_URL, token_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_refresh = self.client.post(
            REFRESH_URL, {"refresh": response.data["refresh"]}
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_refresh.data)

    def test_get_page_me(self):
        token_data = {
            "email": "testemail@test.com",
            "password": "testpassword",
        }
        response = self.client.post(TOKEN_URL, token_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.get(
            MANAGE_URL, HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
