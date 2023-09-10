from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_api.users.tests.factories import UserFactory


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.payload = {
            "name": "Test Eko Aziz",
            "username": "test_eko_aziz",
            "role": "student",
            "password": "r-a_n-d_o-m--->123",
        }
        self.complete_url = reverse("user-list")

    def test_fail_because_invalid_role(self):
        self.payload["role"] = "random"
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["role"][0]), "Invalid Role input value. only available 'librarian' & 'student'."
        )

    def test_success_register_for_student(self):
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["name"], "Test Eko Aziz")
        self.assertEqual(response.data["role"], "student")

    def test_success_register_for_librarian(self):
        self.payload["role"] = "librarian"

        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["name"], "Test Eko Aziz")
        self.assertEqual(response.data["role"], "librarian")


class UserMeTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

        self.complete_url = reverse("user-me")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class UserMeUpdateTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.payload = {
            "name": "Test Eko Aziz",
        }
        self.complete_url = reverse("user-me")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.patch(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class ListStudentTest(APITestCase):
    def setUp(self):
        self.user_librarian = UserFactory(role="librarian")

        self.user = UserFactory(first_name="eko", last_name="aziz", username="eko_aziz", role="student")

        self.complete_url = reverse("api_user:list-student")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_success(self):
        UserFactory.create_batch(3, role="student")

        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_success_with_filter(self):
        UserFactory.create_batch(3, role="student")

        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=eko_aziz")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class ListLibrarianTest(APITestCase):
    def setUp(self):
        self.user_superadmin = UserFactory(role="superadmin")

        self.user = UserFactory(first_name="eko", last_name="aziz", username="eko_aziz", role="librarian")

        self.complete_url = reverse("api_user:list-librarian")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_librarian(self):
        self.client.force_login(self.user)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_success(self):
        UserFactory.create_batch(3, role="librarian")

        self.client.force_login(self.user_superadmin)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_success_with_filter(self):
        UserFactory.create_batch(3, role="librarian")

        self.client.force_login(self.user_superadmin)
        response = self.client.get(self.complete_url + "?q=eko_aziz")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
