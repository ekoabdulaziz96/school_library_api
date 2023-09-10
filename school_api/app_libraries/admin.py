from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import decorators

from school_api.app_libraries.models import Book

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "quantity"]


class BookAdmin(admin.ModelAdmin):
    form = BookForm
    list_display = ["title", "author", "quantity", "nearest_return_date"]
    search_fields = ["title", "author"]


admin.site.register(Book, BookAdmin)
