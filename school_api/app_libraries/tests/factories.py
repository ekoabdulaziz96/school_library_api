from django.utils import timezone
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from school_api.app_libraries.models import Book, BorrowHistory
from school_api.users.tests.factories import UserFactory


class BookFactory(DjangoModelFactory):
    title = Faker("sentence")
    author = Faker("name")
    quantity = 15

    class Meta:
        model = Book
        django_get_or_create = ["title"]


class StudentBorrowFactory(DjangoModelFactory):
    book = SubFactory(BookFactory)
    user_student = SubFactory(UserFactory)
    deadline_date = timezone.localtime().date() + timezone.timedelta(days=30)

    class Meta:
        model = BorrowHistory
        django_get_or_create = ["book", "user_student"]
