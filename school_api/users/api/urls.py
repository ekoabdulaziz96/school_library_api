from django.urls import path

from school_api.users.api import views

app_name = "app_libraries"

urlpatterns = [
    path("students/", views.ListStudent.as_view(), name="list-student"),
    path("librarians/", views.ListLibrarian.as_view(), name="list-librarian"),
]
