from django.core.exceptions import ValidationError as CoreValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from school_api.app_libraries import settings as app_settings
from school_api.app_libraries.api.serializers import BookSerializer
from school_api.app_libraries.bussiness_logics.books import BookBL
from school_api.app_libraries.models import Book, BorrowHistory
from school_api.bases.serializers import BaseModelSerializer, BaseSerializer
from school_api.users.models import User


class ListStudentBorrowSerializer(BaseModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BorrowHistory
        fields = ["book", "is_borrowed", "count_extend", "borrowed_at", "deadline_date"]


class StudentBorrowCreationSerializer(BaseSerializer):
    book_uuids = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        self.user_student = User.objects.filter(username=self.context["username"]).first()
        if not self.user_student:
            raise NotFound(app_settings.MSG_STUDENT_NOT_FOUND)

        current_borrow_count = self.user_student.borrow_histories.filter(is_borrowed=1).count()

        attrs = super().validate(attrs)

        attrs["borrow_objects"] = self.get_validated_books(attrs.get("book_uuids"), current_borrow_count)

        return attrs

    def get_validated_books(self, book_uuids, current_borrow_count):
        if book_uuids is None:
            raise ValidationError({"book_uuids": serializers.Field.default_error_messages["required"]})

        if len(book_uuids) < app_settings.BORROW_MIN_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        elif len(book_uuids) > app_settings.BORROW_MAX_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MAX_COUNT})

        try:
            book_objects = Book.objects.filter(uuid__in=book_uuids)
        except CoreValidationError as e:
            raise ValidationError({"book_uuids": str(e)})

        try:
            borrow_objects = self.user_student.borrow_histories.filter(
                book__uuid__in=book_uuids, is_borrowed=True
            ).first()
            if borrow_objects:
                raise ValidationError(
                    {"book_uuids": app_settings.MSG_BORROW_BORROWED_YET.format(borrow_objects.book.title)}
                )
        except CoreValidationError as e:
            raise ValidationError({"book_uuids": str(e)})

        if len(book_objects) == 0:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        elif len(book_uuids) + current_borrow_count > app_settings.BORROW_MAX_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MAX_COUNT})

        borrow_objects = []
        for book in book_objects:
            if book.quantity < 1:
                raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_BOOK_QTY.format(book.title)})

            deadline_date = timezone.localtime().date() + timezone.timedelta(days=app_settings.BORROW_DEADLINE_DAYS)
            borrow_objects.append(
                BorrowHistory(user_student=self.user_student, book=book, deadline_date=deadline_date)
            )

        return borrow_objects

    def save(self, **kwargs):
        borrow_history_objects = BorrowHistory.objects.bulk_create(self.validated_data["borrow_objects"])
        result_data = {"count_borrow": len(borrow_history_objects), "student_name": self.user_student.name}

        BookBL().sync_qty_for_borrowed_book(borrow_history_objects)
        return result_data


class StudentBorrowreturnSerializer(BaseSerializer):
    book_uuids = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        attrs = super().validate(attrs)

        attrs["borrow_histories"], attrs["borrow_history_objects"] = self.get_validated_borrow_history(
            attrs.get("book_uuids")
        )

        return attrs

    def get_validated_borrow_history(self, book_uuids):
        if book_uuids is None:
            raise ValidationError({"book_uuids": serializers.Field.default_error_messages["required"]})

        if len(book_uuids) < app_settings.BORROW_MIN_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        elif len(book_uuids) > app_settings.BORROW_MAX_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MAX_COUNT})

        try:
            borrow_history_objects = self.instance.borrow_histories.filter(book__uuid__in=book_uuids).select_related(
                "book"
            )
        except CoreValidationError as e:
            raise ValidationError({"book_uuids": str(e)})

        if len(borrow_history_objects) == 0:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        bulk_update_borrow = []
        for borrow_history in borrow_history_objects:
            if borrow_history.is_borrowed is False:
                raise ValidationError(
                    {"book_uuids": app_settings.MSG_BORROW_RETURNED_YET.format(borrow_history.book.title)}
                )

            borrow_history.is_borrowed = False
            borrow_history.deadline_date = None
            bulk_update_borrow.append(borrow_history)

        return bulk_update_borrow, borrow_history_objects

    def save(self, **kwargs):
        bulk_update_borrow = self.validated_data["borrow_histories"]

        count_return = BorrowHistory.objects.bulk_update(bulk_update_borrow, ["is_borrowed", "deadline_date"])
        result_data = {"count_borrow": count_return, "student_name": self.instance.name}

        BookBL().sync_qty_for_returned_book(self.validated_data["borrow_history_objects"])
        return result_data


class StudentBorrowExtendSerializer(BaseSerializer):
    book_uuids = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        attrs = super().validate(attrs)

        attrs["borrow_histories"] = self.get_validated_borrow_history(attrs.get("book_uuids"))

        return attrs

    def get_validated_borrow_history(self, book_uuids):
        if book_uuids is None:
            raise ValidationError({"book_uuids": serializers.Field.default_error_messages["required"]})

        if len(book_uuids) < app_settings.BORROW_MIN_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        elif len(book_uuids) > app_settings.BORROW_MAX_BOOK:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MAX_COUNT})

        try:
            borrow_history_objects = self.instance.borrow_histories.filter(
                is_borrowed=1, book__uuid__in=book_uuids
            ).select_related("book")
        except CoreValidationError as e:
            raise ValidationError({"book_uuids": str(e)})

        if len(borrow_history_objects) == 0:
            raise ValidationError({"book_uuids": app_settings.MSG_BORROW_INVALID_MIN_COUNT})

        deadline_date = timezone.localtime().date() + timezone.timedelta(days=app_settings.BORROW_DEADLINE_DAYS)
        bulk_update_borrow = []
        for borrow_history in borrow_history_objects:
            if borrow_history.count_extend >= app_settings.BORROW_EXTEND_MAX_COUNT:
                raise ValidationError(
                    {"book_uuids": app_settings.MSG_BORROW_INVALID_EXTEND.format(borrow_history.book.title)}
                )

            borrow_history.count_extend += 1
            borrow_history.deadline_date = deadline_date
            bulk_update_borrow.append(borrow_history)

        return bulk_update_borrow

    def save(self, **kwargs):
        bulk_update_borrow = self.validated_data["borrow_histories"]

        count_return = BorrowHistory.objects.bulk_update(bulk_update_borrow, ["count_extend", "deadline_date"])
        result_data = {"count_borrow": count_return, "student_name": self.instance.name}

        return result_data
