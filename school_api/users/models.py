from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """
    Default custom user model for school_api.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    ROLE_CHOICES = (
        ("superadmin", "Superadmin"),
        ("librarian", "Librarian"),
        ("student", "Student"),
    )
    role = models.CharField(choices=ROLE_CHOICES, blank=False, null=False, default="student")

    REQUIRED_FIELDS = []

    @property
    def name(self):
        return self.get_full_name()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})
