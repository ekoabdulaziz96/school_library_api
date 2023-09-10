from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_api.app_libraries.tests.factories import BookFactory, StudentBorrowFactory
from school_api.users.tests.factories import UserFactory


class ListBorrowMeTest(APITestCase):
    def setUp(self):
        self.user_student = UserFactory(role="student")
        self.user_librarian = UserFactory(role="librarian")

        self.book_1 = BookFactory(title="programming")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_1)
        self.book_2 = BookFactory(title="language")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_2, is_borrowed=False)

        StudentBorrowFactory.create_batch(5, user_student=self.user_student)
        StudentBorrowFactory.create_batch(3, user_student=self.user_student, is_borrowed=False)

        self.complete_url = reverse("api_library:list-borrow-me")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_librarian(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_success_with_filter_title(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + self.book_1.title)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_1.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid_for_returned_book(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_2.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_success(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)
        self.assertEqual(len(response.data["results"][0]), 5)
        self.assertEqual(len(response.data["results"][0]["book"]), 5)


class ListBorrowMeHistoryTest(APITestCase):
    def setUp(self):
        self.user_student = UserFactory(role="student")

        self.book_1 = BookFactory(title="programming")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_1)
        self.book_2 = BookFactory(title="language")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_2, is_borrowed=False)

        StudentBorrowFactory.create_batch(5, user_student=self.user_student)
        StudentBorrowFactory.create_batch(3, user_student=self.user_student, is_borrowed=False)

        self.user_librarian = UserFactory(role="librarian")

        self.complete_url = reverse("api_library:list-borrow-me-history")

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_librarian(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_success_with_filter_title(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + self.book_1.title)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_1.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid_for_returned_book(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_2.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        self.assertEqual(len(response.data["results"][0]), 5)
        self.assertEqual(len(response.data["results"][0]["book"]), 5)
