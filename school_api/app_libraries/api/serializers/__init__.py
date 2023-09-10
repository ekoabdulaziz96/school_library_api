from school_api.app_libraries.models import Book
from school_api.bases.serializers import BaseModelSerializer


class BookSerializer(BaseModelSerializer):
    class Meta:
        model = Book
        fields = ["uuid", "title", "author", "quantity", "nearest_return_date"]
