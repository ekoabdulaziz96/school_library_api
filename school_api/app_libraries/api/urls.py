from django.urls import path

from school_api.app_libraries.api import views
from school_api.app_libraries.api.views import librarian, student

app_name = "app_libraries"

# general / anonymous / non-user
urlpatterns = [
    path("books/", views.ListBook.as_view(), name="list-book"),
]

# librarian
urlpatterns += [
    path("student-borrow/<str:username>/", librarian.ListStudentBorrow.as_view(), name="list-student-borrow"),
    path(
        "student-borrow/<str:username>/return", librarian.StudentBorrowReturn.as_view(), name="student-borrow-return"
    ),
    path(
        "student-borrow/<str:username>/extend", librarian.StudentBorrowExtend.as_view(), name="student-borrow-extend"
    ),
    path(
        "student-borrow/<str:username>/history/",
        librarian.ListStudentBorrowHistory.as_view(),
        name="list-student-borrow-history",
    ),
]

# student
urlpatterns += [
    path("borrow/me/", student.ListBorrowMe.as_view(), name="list-borrow-me"),
    path(
        "borrow/me/history/",
        student.ListBorrowMeHistory.as_view(),
        name="list-borrow-me-history",
    ),
]
