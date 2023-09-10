from rest_framework import generics

from school_api.app_libraries.api.serializers import BookSerializer
from school_api.app_libraries.models import Book
from school_api.app_libraries.paginations import BookPagination


class ListBook(generics.ListAPIView):
    permission_classes = []
    pagination_class = BookPagination
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    ordering = ("title",)
    search_fields = ["title", "author", "uuid"]
    ordering_fields = ["title", "author"]
