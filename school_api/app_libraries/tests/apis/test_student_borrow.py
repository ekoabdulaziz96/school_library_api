from django.shortcuts import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from school_api.app_libraries.tests.factories import BookFactory, StudentBorrowFactory
from school_api.users.tests.factories import UserFactory


class ListStudentBorrowTest(APITestCase):
    def setUp(self):
        self.user_student = UserFactory(role="student")

        self.book_1 = BookFactory(title="programming")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_1)
        self.book_2 = BookFactory(title="language")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_2, is_borrowed=False)

        StudentBorrowFactory.create_batch(5, user_student=self.user_student)
        StudentBorrowFactory.create_batch(3, user_student=self.user_student, is_borrowed=False)

        self.user_librarian = UserFactory(role="librarian")

        self.complete_url = reverse("api_library:list-student-borrow", args=[self.user_student.username])

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_fail_because_username_not_found(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(reverse("api_library:list-student-borrow", args=["random"]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), "Student not found.")

    def test_success_with_filter_title(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + self.book_1.title)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_1.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid_for_returned_book(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_2.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_success(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)
        self.assertEqual(len(response.data["results"][0]), 5)
        self.assertEqual(len(response.data["results"][0]["book"]), 5)


class ListStudentBorrowHistoryTest(APITestCase):
    def setUp(self):
        self.user_student = UserFactory(role="student")

        self.book_1 = BookFactory(title="programming")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_1)
        self.book_2 = BookFactory(title="language")
        StudentBorrowFactory(user_student=self.user_student, book=self.book_2, is_borrowed=False)

        StudentBorrowFactory.create_batch(5, user_student=self.user_student)
        StudentBorrowFactory.create_batch(3, user_student=self.user_student, is_borrowed=False)

        self.user_librarian = UserFactory(role="librarian")

        self.complete_url = reverse("api_library:list-student-borrow-history", args=[self.user_student.username])

    def test_fail_because_not_logged_user(self):
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user_student)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_fail_because_username_not_found(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(reverse("api_library:list-student-borrow", args=["random"]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), "Student not found.")

    def test_success_with_filter_title(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + self.book_1.title)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_1.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success_with_filter_uuid_for_returned_book(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url + "?q=" + str(self.book_2.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_success(self):
        self.client.force_login(self.user_librarian)
        response = self.client.get(self.complete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        self.assertEqual(len(response.data["results"][0]), 5)
        self.assertEqual(len(response.data["results"][0]["book"]), 5)


class StudentBorrowCreateTest(APITestCase):
    def setUp(self):
        self.today = timezone.localtime().date()

        self.user_student = UserFactory(role="student", first_name="eko", last_name="aziz")
        self.user_librarian = UserFactory(role="librarian")

        self.book_1 = BookFactory(quantity=2)
        self.book_2 = BookFactory(quantity=1)
        self.payload = {"book_uuids": [self.book_1.uuid, self.book_2.uuid]}
        self.complete_url = reverse("api_library:list-student-borrow", args=[self.user_student.username])

    def test_fail_because_not_logged_user(self):
        response = self.client.post(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user_student)
        response = self.client.post(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_fail_because_username_not_found(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(reverse("api_library:list-student-borrow", args=["random"]), data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), "Student not found.")

    def test_fail_because_empty_payload(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "This field is required.")

    def test_fail_because_empty_book_uuids(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data={"book_uuids": []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_exceeds_quota_selected_book(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(
            self.complete_url, data={"book_uuids": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Exceed the quota, maximum 10 books.")

    def test_fail_because_invalid_book_uuids_format(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data={"book_uuids": ["1"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid UUID.", str(response.data["book_uuids"][0]))

    def test_fail_because_invalid_book_uuids_value(self):
        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data={"book_uuids": ["f3252e4f-c7dd-4a41-b755-4adcb1efd50f"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_exceeds_quota_selected_and_current_book(self):
        StudentBorrowFactory.create_batch(9, user_student=self.user_student)

        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Exceed the quota, maximum 10 books.")

    def test_fail_because_book_out_of_stock(self):
        self.book_1.quantity = 0
        self.book_1.save()

        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Choosen book out of stok. book title:", str(response.data["book_uuids"][0]))

    def test_fail_because_book_have_been_borrowed(self):
        StudentBorrowFactory(user_student=self.user_student, book=self.book_2)

        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Choosen book have been borrowed. book title:", str(response.data["book_uuids"][0]))

    def test_success(self):
        StudentBorrowFactory(user_student=UserFactory(role="student"), book=self.book_2)
        StudentBorrowFactory(user_student=UserFactory(role="student"), book=self.book_2, deadline_date=self.today)

        self.client.force_login(self.user_librarian)
        response = self.client.post(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "Success add 2 borrowed book to eko aziz.")

        self.book_1.refresh_from_db()
        self.book_2.refresh_from_db()
        self.assertEqual(self.book_1.quantity, 1)
        self.assertEqual(self.book_1.nearest_return_date, None)
        self.assertEqual(self.book_2.quantity, 0)
        self.assertEqual(self.book_2.nearest_return_date, self.today)

        with self.subTest("check list student borrow"):
            response = self.client.get(reverse("api_library:list-student-borrow", args=[self.user_student.username]))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 2)

        with self.subTest("check list book for book_2"):
            response = self.client.get(reverse("api_library:list-book") + "?q=" + str(self.book_2.uuid))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertIsNotNone(response.data["results"][0]["nearest_return_date"])


class StudentBorrowReturnTest(APITestCase):
    def setUp(self):
        self.today = timezone.localtime().date()

        self.user_student = UserFactory(role="student", first_name="eko", last_name="aziz")
        self.user_librarian = UserFactory(role="librarian")

        self.book_1 = BookFactory(quantity=1)
        self.book_2 = BookFactory(quantity=0, nearest_return_date=self.today)

        self.borrow_1 = StudentBorrowFactory(user_student=self.user_student, book=self.book_1)
        self.borrow_2 = StudentBorrowFactory(user_student=self.user_student, book=self.book_2)
        StudentBorrowFactory(user_student=self.user_student)

        self.payload = {"book_uuids": [self.book_1.uuid, self.book_2.uuid]}
        self.complete_url = reverse("api_library:student-borrow-return", args=[self.user_student.username])

    def test_fail_because_not_logged_user(self):
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user_student)
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_fail_because_username_not_found(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(reverse("api_library:student-borrow-return", args=["random"]), data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), "Student not found.")

    def test_fail_because_empty_payload(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "This field is required.")

    def test_fail_because_empty_book_uuids(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_exceeds_quota_selected_book(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(
            self.complete_url, data={"book_uuids": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Exceed the quota, maximum 10 books.")

    def test_fail_because_invalid_book_uuids_format(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": ["1"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid UUID.", str(response.data["book_uuids"][0]))

    def test_fail_because_invalid_book_uuids_value(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": ["f3252e4f-c7dd-4a41-b755-4adcb1efd50f"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_book_have_been_returned(self):
        self.borrow_2.is_borrowed = False
        self.borrow_2.save()

        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Choosen book have been returned. book title:", str(response.data["book_uuids"][0]))

    def test_success(self):
        StudentBorrowFactory(user_student=UserFactory(role="student"), book=self.book_2, deadline_date=self.today)

        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success return 2 borrowed book from eko aziz.")

        self.book_1.refresh_from_db()
        self.book_2.refresh_from_db()
        self.assertEqual(self.book_1.quantity, 2)
        self.assertEqual(self.book_1.nearest_return_date, None)
        self.assertEqual(self.book_2.quantity, 1)
        self.assertEqual(self.book_2.nearest_return_date, None)

        with self.subTest("check list student borrow"):
            response = self.client.get(reverse("api_library:list-student-borrow", args=[self.user_student.username]))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

        with self.subTest("check list book for book_2"):
            response = self.client.get(reverse("api_library:list-book") + "?q=" + str(self.book_2.uuid))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertIsNone(response.data["results"][0]["nearest_return_date"])


class StudentBorrowExtendTest(APITestCase):
    def setUp(self):
        self.today = timezone.localtime().date()
        self.deadline_date = self.today + timezone.timedelta(days=30)

        self.user_student = UserFactory(role="student", first_name="eko", last_name="aziz")
        self.user_librarian = UserFactory(role="librarian")

        self.book_1 = BookFactory(quantity=1)
        self.book_2 = BookFactory(quantity=0, nearest_return_date=self.today)

        self.borrow_1 = StudentBorrowFactory(
            user_student=self.user_student, book=self.book_1, deadline_date=self.today
        )
        self.borrow_2 = StudentBorrowFactory(
            user_student=self.user_student, book=self.book_2, deadline_date=self.today
        )
        StudentBorrowFactory(user_student=self.user_student)

        self.payload = {"book_uuids": [self.book_1.uuid, self.book_2.uuid]}
        self.complete_url = reverse("api_library:student-borrow-extend", args=[self.user_student.username])

    def test_fail_because_not_logged_user(self):
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "Authentication credentials were not provided.")

    def test_fail_because_logged_as_student(self):
        self.client.force_login(self.user_student)
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(str(response.data["detail"]), "You do not have permission to perform this action.")

    def test_fail_because_username_not_found(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(reverse("api_library:student-borrow-extend", args=["random"]), data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), "Student not found.")

    def test_fail_because_empty_payload(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "This field is required.")

    def test_fail_because_empty_book_uuids(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_exceeds_quota_selected_book(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(
            self.complete_url, data={"book_uuids": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Exceed the quota, maximum 10 books.")

    def test_fail_because_invalid_book_uuids_format(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": ["1"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid UUID.", str(response.data["book_uuids"][0]))

    def test_fail_because_invalid_book_uuids_value(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data={"book_uuids": ["f3252e4f-c7dd-4a41-b755-4adcb1efd50f"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["book_uuids"][0]), "Choose at least 1 book.")

    def test_fail_because_book_have_been_extended(self):
        self.borrow_2.count_extend = 1
        self.borrow_2.save()

        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Choosen book can't be extended. book title:", str(response.data["book_uuids"][0]))

    def test_success(self):
        self.client.force_login(self.user_librarian)
        response = self.client.patch(self.complete_url, data=self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success extend 2 borrowed book from eko aziz.")

        self.borrow_1.refresh_from_db()
        self.borrow_2.refresh_from_db()
        self.assertEqual(self.borrow_1.count_extend, 1)
        self.assertEqual(self.borrow_1.deadline_date, self.deadline_date)
        self.assertEqual(self.borrow_2.count_extend, 1)
        self.assertEqual(self.borrow_2.deadline_date, self.deadline_date)

        with self.subTest("check list student borrow"):
            response = self.client.get(reverse("api_library:list-student-borrow", args=[self.user_student.username]))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 3)

        with self.subTest("check list book for book_2"):
            response = self.client.get(reverse("api_library:list-book") + "?q=" + str(self.book_2.uuid))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertIsNotNone(response.data["results"][0]["nearest_return_date"])
