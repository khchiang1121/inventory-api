import uuid
from typing import Any, Dict, List

from django.db import models


class AbstractBase(models.Model):
    """Base model with common fields for all models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
