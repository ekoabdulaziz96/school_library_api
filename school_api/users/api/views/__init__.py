from rest_framework import generics

from school_api.users.api.serializers import CustomUserSerializer
from school_api.users.models import User
from school_api.users.paginations import UserPagination
from school_api.users.permissions import IsLibrarian, IsSuperadmin


class ListStudent(generics.ListAPIView):
    permission_classes = [IsSuperadmin | IsLibrarian]
    serializer_class = CustomUserSerializer
    pagination_class = UserPagination
    queryset = User.objects.filter(role="student", is_active=True)
    ordering = ("username",)
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["username", "first_name", "last_name"]


class ListLibrarian(ListStudent):
    permission_classes = [IsSuperadmin]
    queryset = User.objects.filter(role="librarian", is_active=True)
