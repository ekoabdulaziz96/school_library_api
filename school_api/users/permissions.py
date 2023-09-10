from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class IsStudent(IsAuthenticated):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        return is_authenticated and request.user and request.user.role == "student"


class IsLibrarian(IsAuthenticated):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        return is_authenticated and request.user and request.user.role == "librarian"


class IsSuperadmin(IsAuthenticated):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        return is_authenticated and request.user and request.user.role == "superadmin"
