from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_api.app_libraries.tests.factories import BookFactory
from school_api.users.tests.factories import UserFactory


class ListBookTest(APITestCase):
    fixtures = ["school_api/app_libraries/fixtures/dummy-books.json"]

    def setUp(self):
        self.user = UserFactory(role="student")

        self.complete_url = reverse("api_library:list-book")

    def test_success_with_no_login_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"][0]), 5)

    def test_success_with_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"][0]), 5)

    def test_success_with_filter_title(self):
        self.client.force_login(self.user)

        response = self.client.get(self.complete_url + "?q=math")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"][0]), 5)
        self.assertEqual(response.data["results"][0]["title"], "Advance in Mathematics")

    def test_success_with_filter_uuid(self):
        book = BookFactory()

        self.client.force_login(self.user)
        response = self.client.get(self.complete_url + "?q=" + str(book.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"][0]), 5)
