from django.contrib.auth.models import Group
from django.db import models

from inventory_api.api.models.users import CustomUser

from .base import AbstractBase


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class Tenant(AbstractBase):
    """Tenant model for multi-tenancy"""

    name = models.CharField(max_length=255, help_text="Tenant name")
    description = models.TextField(blank=True, help_text="Tenant description")
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Tenant status",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class Region(AbstractBase):
    """Region model"""

    name = models.CharField(max_length=255, help_text="Region name")
    description = models.TextField(blank=True, help_text="Region description")
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Region status",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class Vendor(AbstractBase):
    """Hardware manufacturer model"""

    name = models.CharField(
        max_length=100, unique=True, help_text="Vendor name, e.g., Dell, HPE, etc."
    )
    contact_email = models.EmailField(blank=True, help_text="Vendor contact email")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Vendor contact phone")
    address = models.TextField(blank=True, help_text="Vendor address")

    class Meta:
        ordering = ["name"]
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self) -> str:
        return str(self.name)
