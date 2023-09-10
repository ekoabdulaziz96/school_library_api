from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from school_api.app_libraries import settings as app_settings
from school_api.app_libraries.api.serializers.librarian import (
    ListStudentBorrowSerializer,
    StudentBorrowCreationSerializer,
    StudentBorrowExtendSerializer,
    StudentBorrowreturnSerializer,
)
from school_api.app_libraries.paginations import BorrowPagination
from school_api.users.models import User
from school_api.users.permissions import IsLibrarian, IsSuperadmin


class ListStudentBorrow(generics.ListCreateAPIView):
    permission_classes = [IsSuperadmin | IsLibrarian]
    pagination_class = BorrowPagination
    ordering = ("created_at",)
    search_fields = ["book__title", "book__author", "book__uuid"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentBorrowCreationSerializer
        return ListStudentBorrowSerializer

    def get_queryset(self):
        user_student = User.objects.filter(username=self.kwargs["username"]).first()
        if not user_student:
            raise NotFound(app_settings.MSG_STUDENT_NOT_FOUND)

        return user_student.borrow_histories.filter(is_borrowed=1).select_related("book")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "username": self.kwargs["username"]}
        )
        serializer.is_valid(raise_exception=True)

        result = serializer.save(**kwargs)
        message = app_settings.MSG_BORROW_SUCCESS.format(result["count_borrow"], result["student_name"])
        return Response(data=message, status=status.HTTP_201_CREATED)


class ListStudentBorrowHistory(generics.ListCreateAPIView):
    permission_classes = [IsSuperadmin | IsLibrarian]
    pagination_class = BorrowPagination
    serializer_class = ListStudentBorrowSerializer
    ordering = ("created_at",)
    search_fields = ["book__title", "book__author", "book__uuid"]

    def get_queryset(self):
        user_student = User.objects.filter(username=self.kwargs["username"]).first()
        if not user_student:
            raise NotFound(app_settings.MSG_STUDENT_NOT_FOUND)

        return user_student.borrow_histories.select_related("book")


class StudentBorrowReturn(generics.UpdateAPIView):
    permission_classes = [IsSuperadmin | IsLibrarian]
    pagination_class = BorrowPagination
    serializer_class = StudentBorrowreturnSerializer
    ordering = ("created_at",)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user_student = User.objects.filter(username=self.kwargs["username"]).first()
        if not user_student:
            raise NotFound(app_settings.MSG_STUDENT_NOT_FOUND)

        serializer = self.get_serializer(user_student, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        result = serializer.save(**kwargs)
        message = app_settings.MSG_BORROW_RETURN_SUCCESS.format(result["count_borrow"], result["student_name"])
        return Response(data=message, status=status.HTTP_200_OK)


class StudentBorrowExtend(generics.UpdateAPIView):
    permission_classes = [IsSuperadmin | IsLibrarian]
    pagination_class = BorrowPagination
    serializer_class = StudentBorrowExtendSerializer
    ordering = ("created_at",)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user_student = User.objects.filter(username=self.kwargs["username"]).first()
        if not user_student:
            raise NotFound(app_settings.MSG_STUDENT_NOT_FOUND)

        serializer = self.get_serializer(user_student, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        result = serializer.save(**kwargs)
        message = app_settings.MSG_BORROW_EXTEND_SUCCESS.format(result["count_borrow"], result["student_name"])
        return Response(data=message, status=status.HTTP_200_OK)
