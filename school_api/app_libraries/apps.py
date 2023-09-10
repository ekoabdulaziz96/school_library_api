from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppLibrariesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "school_api.app_libraries"
    verbose_name = _("Libraries")

    # def ready(self):
    #     try:
    #         import school_api.app_libraries.signals  # noqa: F401
    #         import school_api.app_libraries.tasks  # noqa: F401
    #     except ImportError:
    #         pass
