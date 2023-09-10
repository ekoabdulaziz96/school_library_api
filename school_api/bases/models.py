from django.db import models
from safedelete import models as safedelete_models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created_at"


class SafeDeleteModel(safedelete_models.SafeDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_by_cascade = None

    class Meta:
        abstract = True
        get_latest_by = "created_at"
