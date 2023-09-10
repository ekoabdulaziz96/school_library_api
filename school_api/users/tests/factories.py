from collections.abc import Sequence
from typing import Any

from factory import Faker, fuzzy, post_generation
from factory.django import DjangoModelFactory

from school_api.users.models import User


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    role = fuzzy.FuzzyChoice(choices=[t[0] for t in User.ROLE_CHOICES])

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = User
        django_get_or_create = ["username"]
