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

# add a model for user group
class UserGroup(Group):
    """User group model"""

    name = models.CharField(max_length=255, help_text="Group name")
    description = models.TextField(blank=True, help_text="Group description")
    status = models.CharField(max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")], help_text="Group status")
    user = models.ManyToManyField("User", related_name="user_groups")
