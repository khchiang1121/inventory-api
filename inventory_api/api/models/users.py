from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from guardian.mixins import GuardianUserMixin

from inventory_api.api.models.base import AbstractBase


class CustomUser(GuardianUserMixin, AbstractUser):
    """Custom user model with additional fields"""

    account = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        help_text="Unique account identifier",
    )
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Account status",
    )


# Use Django's built-in Group model
# from django.contrib.auth.models import Group
