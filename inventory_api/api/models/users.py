from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.mixins import GuardianUserMixin


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
