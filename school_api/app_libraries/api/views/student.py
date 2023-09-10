from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from school_api.app_libraries import settings as app_settings
from school_api.app_libraries.api.serializers.librarian import ListStudentBorrowSerializer
from school_api.app_libraries.paginations import BorrowPagination
from school_api.users.permissions import IsStudent


class ListBorrowMe(generics.ListCreateAPIView):
    permission_classes = [IsStudent]
    pagination_class = BorrowPagination
    serializer_class = ListStudentBorrowSerializer
    ordering = ("created_at",)
    search_fields = ["book__title", "book__author", "book__uuid"]

    def get_queryset(self):
        return self.request.user.borrow_histories.filter(is_borrowed=1).select_related("book")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "username": self.kwargs["username"]}
        )
        serializer.is_valid(raise_exception=True)

        result = serializer.save(**kwargs)
        message = app_settings.MSG_BORROW_SUCCESS.format(result["count_borrow"], result["student_name"])
        return Response(data=message, status=status.HTTP_201_CREATED)


class ListBorrowMeHistory(generics.ListCreateAPIView):
    permission_classes = [IsStudent]
    pagination_class = BorrowPagination
    serializer_class = ListStudentBorrowSerializer
    ordering = ("created_at",)
    search_fields = ["book__title", "book__author", "book__uuid"]

    def get_queryset(self):
        return self.request.user.borrow_histories.select_related("book")
