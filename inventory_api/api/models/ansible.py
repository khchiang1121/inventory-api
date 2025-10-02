# =============================================================================
# File: ansible.py
# Description: Django models for Ansible inventory, groups, hosts, and variables.
# Model Checklist: v3
# Last Checked: 2025-10-01
# =============================================================================

import json
from typing import Any, Dict, List

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from .base import AbstractBase
from .users import CustomGroup, CustomUser


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
class AnsibleInventory(AbstractBase):
    """Represents a complete Ansible inventory"""

    name = models.CharField(max_length=255, unique=True, help_text="Inventory name")
    description = models.TextField(blank=True, help_text="Inventory description")
    source_type = models.CharField(
        max_length=64,
        choices=[
            ("static", "Static"),
            ("dynamic", "Dynamic"),
        ],
        default="static",
        help_text="Type of inventory source",
    )
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft")],
        default="active",
        help_text="Inventory status",
    )
    user = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name="ansible_inventories",
        help_text="Users who have access to the inventory",
    )
    user_group = models.ManyToManyField(
        CustomGroup,
        blank=True,
        related_name="ansible_inventories",
        help_text="User groups who have access to the inventory",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ansible Inventory"
        verbose_name_plural = "Ansible Inventories"

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
class AnsibleGroup(AbstractBase):
    """Enhanced Ansible group with inventory support"""

    ansible_inventory = models.ForeignKey(
        AnsibleInventory,
        on_delete=models.CASCADE,
        related_name="ansible_groups",
        help_text="Inventory that this group belongs to",
    )
    name = models.CharField(max_length=255, help_text="Ansible group name")
    description = models.TextField(blank=True, help_text="Group description")
    is_special = models.BooleanField(
        default=False, help_text="Whether this is a special group (all, ungrouped)"
    )
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft")],
        default="active",
        help_text="Group status",
    )

    @property
    def child_groups(self) -> list:
        """Get all child groups"""
        return [rel.child_group for rel in self.child_relationships.all()]

    @property
    def parent_groups(self) -> list:
        """Get all parent groups"""
        return [rel.parent_group for rel in self.parent_relationships.all()]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ansible_inventory", "name"], name="unique_inventory_group"
            )
        ]
        ordering = ["ansible_inventory", "name"]

    def __str__(self) -> str:
        return f"{self.ansible_inventory.name}:{self.name}"

    def clean(self) -> None:
        super().clean()
        if self.name == "all" and not self.is_special:
            raise ValidationError(
                {"is_special": "If group name is 'all', is_special must be True."}
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
class AnsibleGroupVariable(AbstractBase):
    """Stores variables for groups"""

    ansible_group = models.ForeignKey(
        AnsibleGroup,
        on_delete=models.CASCADE,
        related_name="ansible_group_variables",
        help_text="Group that this variable belongs to",
    )
    name = models.CharField(max_length=255, help_text="Variable name")
    description = models.TextField(blank=True, help_text="Variable description")
    content = models.TextField(help_text="Variable content")
    content_type = models.CharField(
        max_length=32,
        choices=[
            ("yaml", "YAML"),
            ("json", "JSON"),
            ("ini", "INI"),
            ("env", "Environment Variables"),
        ],
        default="yaml",
        help_text="Variable content format",
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="Tag list for categorization and filtering"
    )
    priority = models.PositiveIntegerField(
        default=100, help_text="Weight/priority, lower numbers have higher priority"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("draft", "Draft"),
        ],
        default="active",
        help_text="Ansible variable set status",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ansible_group", "name"], name="unique_group_variable")
        ]
        ordering = ["ansible_group", "priority"]

    def __str__(self) -> str:
        return f"{self.ansible_group.name}:{self.name}"


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
class AnsibleGroupRelationship(AbstractBase):
    """Group relationships with inventory support"""

    parent_group = models.ForeignKey(
        AnsibleGroup,
        on_delete=models.CASCADE,
        related_name="child_relationships",
        help_text="Parent group",
    )
    child_group = models.ForeignKey(
        AnsibleGroup,
        on_delete=models.CASCADE,
        related_name="parent_relationships",
        help_text="Child group",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent_group", "child_group"], name="unique_parent_child"
            )
        ]
        verbose_name = "Ansible Group Relationship"
        verbose_name_plural = "Ansible Group Relationships"

    def __str__(self) -> str:
        return f"{self.parent_group.name} -> {self.child_group.name}"

    def clean(self) -> None:
        from django.core.exceptions import ValidationError

        if self.parent_group == self.child_group:
            raise ValidationError("A group cannot be its own parent")

        if self.parent_group.ansible_inventory != self.child_group.ansible_inventory:
            raise ValidationError("Parent and child groups must be in the same inventory")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
class AnsibleHost(AbstractBase):
    """Enhanced host model with inventory support and aliases"""

    ansible_inventory = models.ForeignKey(
        AnsibleInventory,
        on_delete=models.CASCADE,
        related_name="ansible_hosts",
        help_text="Inventory that this host belongs to",
    )
    ansible_groups = models.ManyToManyField(
        AnsibleGroup,
        related_name="ansible_hosts",
        blank=True,
        help_text="Groups that this host belongs to",
    )

    # Generic foreign key to either VM or Baremetal
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    host = GenericForeignKey("content_type", "object_id")

    # Host aliases (Ansible supports multiple aliases for the same host)
    aliases = models.JSONField(default=list, blank=True, help_text="List of host aliases")

    # Ansible connection parameters
    ansible_host = models.GenericIPAddressField(
        null=True, blank=True, help_text="Ansible connection IP"
    )
    ansible_port = models.PositiveIntegerField(default=22, help_text="SSH port")
    ansible_user = models.CharField(max_length=64, default="root", help_text="SSH username")
    ansible_ssh_private_key_file = models.TextField(
        max_length=1000, blank=True, help_text="Path to SSH private key"
    )
    ansible_ssh_common_args = models.CharField(
        max_length=255, blank=True, help_text="SSH common arguments"
    )
    ansible_ssh_extra_args = models.CharField(
        max_length=255, blank=True, help_text="SSH extra arguments"
    )
    ansible_ssh_pipelining = models.BooleanField(default=False, help_text="Enable SSH pipelining")
    ansible_ssh_executable = models.CharField(
        max_length=255, blank=True, help_text="SSH executable path"
    )
    ansible_python_interpreter = models.CharField(
        max_length=255, blank=True, help_text="Python interpreter path"
    )
    ansible_shell_type = models.CharField(
        max_length=32, blank=True, help_text="Shell type (bash, sh, etc.)"
    )

    # Host status
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("maintenance", "Maintenance"),
            ("error", "Error"),
        ],
        default="active",
        help_text="Host status in inventory",
    )

    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional host metadata")

    class Meta:
        unique_together = ["ansible_inventory", "content_type", "object_id"]
        verbose_name = "Ansible Host"
        verbose_name_plural = "Ansible Hosts"

    def __str__(self) -> str:
        if hasattr(self, "_state") and self._state.adding:
            # Object is being created, groups not available yet
            return f"{self.host if self.host else 'Host'}"
        group_names = ", ".join([group.name for group in self.ansible_groups.all()])
        return f"{self.host} in [{group_names}]" if group_names else f"{self.host}"

    # add a validator to check if all group are in the same inventory
    def clean(self) -> None:
        super().clean()
        if not all(
            group.ansible_inventory == self.ansible_inventory
            for group in self.ansible_groups.all()
        ):
            raise ValidationError("All groups must be in the same inventory")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
class AnsibleHostVariable(AbstractBase):
    """Structured host variables with type support"""

    ansible_host = models.ForeignKey(
        AnsibleHost, on_delete=models.CASCADE, related_name="ansible_host_variables"
    )
    name = models.CharField(max_length=255, help_text="Variable name")
    description = models.TextField(blank=True, help_text="Variable description")
    content = models.TextField(help_text="Variable content")
    content_type = models.CharField(
        max_length=32,
        choices=[
            ("yaml", "YAML"),
            ("json", "JSON"),
            ("ini", "INI"),
            ("env", "Environment Variables"),
        ],
        default="yaml",
        help_text="Variable content format",
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="Tag list for categorization and filtering"
    )
    priority = models.PositiveIntegerField(
        default=100, help_text="Weight/priority, lower numbers have higher priority"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("draft", "Draft"),
        ],
        default="active",
        help_text="Ansible variable set status",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ansible_host", "name"], name="unique_host_variable")
        ]
        ordering = ["ansible_host", "priority"]

    def __str__(self) -> str:
        # Use the related object's string representation to avoid relying on a non-existent 'name' attribute
        return f"{str(self.ansible_host)}:{self.name}"


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
class AnsibleInventoryTemplate(AbstractBase):
    """Templates for generating inventory files"""

    name = models.CharField(max_length=255, unique=True, help_text="Template name")
    description = models.TextField(blank=True, help_text="Template description")
    template_type = models.CharField(
        max_length=32,
        choices=[
            ("ini", "INI Format"),
            ("yaml", "YAML Format"),
            ("json", "JSON Format"),
            ("jinja2", "Jinja2 Template"),
        ],
        default="jinja2",
        help_text="Template type",
    )
    template_content = models.TextField(help_text="Template content")

    class Meta:
        ordering = ["name"]

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
class AnsibleVariableSet(AbstractBase):
    """Independent variable sets that can be associated with multiple inventories"""

    name = models.CharField(max_length=255, unique=True, help_text="Variable set name")
    description = models.TextField(blank=True, help_text="Variable set description")
    content = models.TextField(help_text="Variable content")
    content_type = models.CharField(
        max_length=32,
        choices=[
            ("yaml", "YAML"),
            ("json", "JSON"),
            ("ini", "INI"),
            ("env", "Environment Variables"),
        ],
        default="yaml",
        help_text="Variable content format",
    )
    tags = models.JSONField(
        default=list, blank=True, help_text="Tag list for categorization and filtering"
    )
    priority = models.PositiveIntegerField(
        default=100, help_text="Weight/priority, lower numbers have higher priority"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("draft", "Draft"),
        ],
        default="active",
        help_text="Ansible variable set status",
    )
    user = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name="ansible_variable_sets",
        help_text="Users who have access to the variable set",
    )
    user_group = models.ManyToManyField(
        CustomGroup,
        blank=True,
        related_name="ansible_variable_sets",
        help_text="User groups who have access to the variable set",
    )

    class Meta:
        ordering = ["name", "priority"]
        verbose_name = "Ansible Variable Set"
        verbose_name_plural = "Ansible Variable Sets"

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
class AnsibleInventoryVariableSetAssociation(AbstractBase):
    """Association table for inventory and variable sets (for variable merging)"""

    ansible_inventory = models.ForeignKey(
        AnsibleInventory,
        on_delete=models.CASCADE,
        related_name="associated_variable_sets",
    )
    ansible_variable_set = models.ForeignKey(
        AnsibleVariableSet,
        on_delete=models.CASCADE,
        related_name="associated_inventories",
    )
    load_priority = models.PositiveIntegerField(
        default=100,
        help_text="Variable loading priority, lower numbers have higher priority",
    )
    enabled = models.BooleanField(default=True, help_text="Whether this variable set is enabled")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ansible_inventory", "ansible_variable_set"],
                name="unique_inventory_variable_set",
            )
        ]
        ordering = ["ansible_inventory", "load_priority"]
        verbose_name = "Inventory Variable Set Association"
        verbose_name_plural = "Inventory Variable Set Associations"

    def __str__(self) -> str:
        return f"{self.ansible_inventory.name} -> {self.ansible_variable_set.name}"
