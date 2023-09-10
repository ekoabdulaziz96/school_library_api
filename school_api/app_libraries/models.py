from uuid import uuid4

from django.db import models

from school_api.bases.models import BaseModel, SafeDeleteModel
from school_api.users.models import User


class Book(SafeDeleteModel):
    uuid = models.UUIDField(default=uuid4, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    nearest_return_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "library_books"

    def __str__(self):
        return self.title


class BorrowHistory(BaseModel):
    uuid = models.UUIDField(default=uuid4, unique=True)
    user_student = models.ForeignKey(User, on_delete=models.PROTECT, related_name="borrow_histories")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrow_histories")
    count_extend = models.PositiveIntegerField(default=0)
    is_borrowed = models.BooleanField(default=True, db_index=True)
    deadline_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "library_borrow_histories"

    def __str__(self):
        return f"{self.user_student.name} - {self.book.title}"

    @property
    def borrowed_at(self):
        return self.created_at.date()
