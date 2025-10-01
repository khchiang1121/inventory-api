import uuid
from typing import Any, Dict, List

from django.db import models

# [MODEL CHECKLIST v3]
# Overall structure
# [] Check all fields in the model are necessary and correct
# [] Include docstring for the model (describe its purpose)
# Fields
# [] Have a "name" field, with max_length=255; if needed, set unique=True
# [] Have a "description" field, and allow blank=True
# [] Every field should include a help_text (except relationship)
# [] Set default value if appropriate
# [] String fields (CharField, TextField) should NOT use null=True
# [] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [] If linking to users, include both "user" and "user_group" fields
# [] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [] ForeignKey that can be optional must use null=True, blank=True
# [] ManyToManyField should always define a related_name
# [] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [] Define __str__() to return a meaningful field (e.g., name)
# [] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [] Define clean and save if needed
class AbstractBase(models.Model):
    """Base model with common fields for all models"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
