import json
from typing import Any, Dict, List

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .base import AbstractBase
from .users import CustomUser


class AnsibleInventory(AbstractBase):
    """Represents a complete Ansible inventory"""

    name = models.CharField(max_length=255, unique=True, help_text="Inventory name")
    description = models.TextField(blank=True, help_text="Inventory description")
    version = models.CharField(max_length=32, default="1.0", help_text="Inventory version")
    source_type = models.CharField(
        max_length=32,
        choices=[
            ("static", "Static"),
            ("dynamic", "Dynamic"),
            ("hybrid", "Hybrid"),
        ],
        default="static",
        help_text="Type of inventory source",
    )
    source_plugin = models.CharField(
        max_length=64, null=True, help_text="Dynamic inventory plugin name"
    )
    source_config = models.JSONField(
        default=dict, blank=True, help_text="Configuration for dynamic inventory"
    )
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft")],
        default="active",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_inventories",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ansible Inventory"
        verbose_name_plural = "Ansible Inventories"

    def __str__(self) -> str:
        return str(self.name)


class AnsibleInventoryVariable(AbstractBase):
    """Inventory-level variables"""

    inventory = models.ForeignKey(
        AnsibleInventory, on_delete=models.CASCADE, related_name="variables"
    )
    key = models.CharField(max_length=255, help_text="Variable name")
    value = models.TextField(help_text="Variable value (can be JSON)")
    value_type = models.CharField(
        max_length=32,
        choices=[
            ("string", "String"),
            ("integer", "Integer"),
            ("float", "Float"),
            ("boolean", "Boolean"),
            ("json", "JSON"),
            ("list", "List"),
            ("dict", "Dictionary"),
        ],
        default="string",
    )

    class Meta:
        unique_together = ["inventory", "key"]
        ordering = ["key"]

    def __str__(self) -> str:
        return f"{self.inventory.name}:{self.key}"

    def get_typed_value(self) -> Any:
        """Convert the stored string value back to its proper type"""
        import json

        if self.value_type == "string":
            return self.value
        elif self.value_type == "integer":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "boolean":
            return str(self.value).lower() in ("true", "1", "yes", "on")
        elif self.value_type in ("json", "list", "dict"):
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return self.value
        else:
            return self.value


class AnsibleGroup(AbstractBase):
    """Enhanced Ansible group with inventory support"""

    inventory = models.ForeignKey(
        AnsibleInventory, on_delete=models.CASCADE, related_name="groups"
    )
    name = models.CharField(max_length=255, help_text="Ansible group name")
    description = models.TextField(blank=True, help_text="Group description")
    is_special = models.BooleanField(
        default=False, help_text="Whether this is a special group (all, ungrouped)"
    )
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
    )

    class Meta:
        unique_together = ["inventory", "name"]
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.inventory.name}:{self.name}"

    @property
    def all_variables(self) -> dict:
        """Get all variables for this group, including inherited ones"""
        variables = {}

        # Get inventory-level variables first
        for var in self.inventory.variables.all():
            variables[var.key] = var.get_typed_value()

        # Get associated variable sets (ordered by priority)
        associated_sets = self.inventory.associated_variable_sets.filter(
            enabled=True, variable_set__status="active"
        ).order_by("load_priority", "variable_set__priority")

        for association in associated_sets:
            set_vars = association.variable_set.get_parsed_content()
            variables.update(set_vars)

        # Get direct group variables
        for var in self.variables.all():
            variables[var.key] = var.get_typed_value()

        # Get inherited variables from parent groups
        for parent_rel in self.parent_relationships.all():
            parent_vars = parent_rel.parent_group.all_variables
            # Child variables override parent variables
            variables.update(parent_vars)

        return variables

    @property
    def child_groups(self) -> list:
        """Get all child groups"""
        return [rel.child_group for rel in self.child_relationships.all()]

    @property
    def parent_groups(self) -> list:
        """Get all parent groups"""
        return [rel.parent_group for rel in self.parent_relationships.all()]

    @property
    def all_hosts(self) -> list:
        """Get all hosts in this group and child groups"""
        hosts = list(self.hosts.all())

        # Recursively get hosts from child groups
        for child_group in self.child_groups:
            hosts.extend(child_group.all_hosts)

        return hosts

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a specific variable value"""
        try:
            var = self.variables.get(key=key)
            return var.get_typed_value()
        except self.variables.model.DoesNotExist:
            return default

    def set_variable(
        self, key: str, value: Any, value_type: str = "string"
    ) -> "AnsibleGroupVariable":
        """Set a variable for this group"""
        var, created = self.variables.get_or_create(key=key)
        var.value = str(value)
        var.value_type = value_type
        var.save()
        return var


class AnsibleGroupVariable(AbstractBase):
    group = models.ForeignKey(AnsibleGroup, on_delete=models.CASCADE, related_name="variables")
    key = models.CharField(max_length=255, help_text="Variable name")
    value = models.TextField(help_text="Variable value (can be JSON)")
    value_type = models.CharField(
        max_length=32,
        choices=[
            ("string", "String"),
            ("integer", "Integer"),
            ("float", "Float"),
            ("boolean", "Boolean"),
            ("json", "JSON"),
            ("list", "List"),
            ("dict", "Dictionary"),
        ],
        default="string",
    )

    class Meta:
        unique_together = ["group", "key"]
        ordering = ["key"]

    def __str__(self) -> str:
        return f"{self.group.name}:{self.key}"

    def get_typed_value(self) -> Any:
        """Convert the stored string value back to its proper type"""
        import json

        if self.value_type == "string":
            return self.value
        elif self.value_type == "integer":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "boolean":
            return str(self.value).lower() in ("true", "1", "yes", "on")
        elif self.value_type in ("json", "list", "dict"):
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return self.value
        else:
            return self.value


class AnsibleGroupRelationship(AbstractBase):
    """Enhanced group relationships with inventory support"""

    parent_group = models.ForeignKey(
        AnsibleGroup, on_delete=models.CASCADE, related_name="child_relationships"
    )
    child_group = models.ForeignKey(
        AnsibleGroup, on_delete=models.CASCADE, related_name="parent_relationships"
    )

    class Meta:
        unique_together = ["parent_group", "child_group"]
        verbose_name = "Ansible Group Relationship"
        verbose_name_plural = "Ansible Group Relationships"

    def __str__(self) -> str:
        return f"{self.parent_group.name} -> {self.child_group.name}"

    def clean(self) -> None:
        from django.core.exceptions import ValidationError

        if self.parent_group == self.child_group:
            raise ValidationError("A group cannot be its own parent")

        if self.parent_group.inventory != self.child_group.inventory:
            raise ValidationError("Parent and child groups must be in the same inventory")


class AnsibleHost(AbstractBase):
    """Enhanced host model with inventory support and aliases"""

    inventory = models.ForeignKey(AnsibleInventory, on_delete=models.CASCADE, related_name="hosts")
    groups = models.ManyToManyField(AnsibleGroup, related_name="hosts", blank=True)

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
    ansible_ssh_private_key_file = models.CharField(
        max_length=255, blank=True, help_text="Path to SSH private key"
    )
    ansible_ssh_common_args = models.CharField(
        max_length=255, blank=True, help_text="SSH common arguments"
    )
    ansible_ssh_extra_args = models.CharField(
        max_length=255, blank=True, help_text="SSH extra arguments"
    )
    ansible_ssh_pipelining = models.BooleanField(default=True, help_text="Enable SSH pipelining")
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
        unique_together = ["inventory", "content_type", "object_id"]
        verbose_name = "Ansible Host"
        verbose_name_plural = "Ansible Hosts"

    def __str__(self) -> str:
        if hasattr(self, "_state") and self._state.adding:
            # Object is being created, groups not available yet
            return f"{self.host if self.host else 'Host'}"
        group_names = ", ".join([group.name for group in self.groups.all()])
        return f"{self.host} in [{group_names}]" if group_names else f"{self.host}"

    @property
    def host_name(self) -> str:
        """Get the name of the host (VM or Baremetal)"""
        if self.host and hasattr(self.host, "name"):
            return self.host.name
        return str(self.host) if self.host else "Unknown"

    @property
    def host_type(self) -> str:
        """Get the type of host (VM or Baremetal)"""
        return self.content_type.model

    @property
    def all_names(self) -> list:
        """Get all names for this host (primary name + aliases)"""
        names = [self.host_name]
        if self.aliases:
            names.extend(self.aliases)
        return names


class AnsibleHostVariable(AbstractBase):
    """Structured host variables with type support"""

    host = models.ForeignKey(
        AnsibleHost, on_delete=models.CASCADE, related_name="structured_variables"
    )
    key = models.CharField(max_length=255, help_text="Variable name")
    value = models.TextField(help_text="Variable value (can be JSON)")
    value_type = models.CharField(
        max_length=32,
        choices=[
            ("string", "String"),
            ("integer", "Integer"),
            ("float", "Float"),
            ("boolean", "Boolean"),
            ("json", "JSON"),
            ("list", "List"),
            ("dict", "Dictionary"),
        ],
        default="string",
    )

    class Meta:
        unique_together = ["host", "key"]
        ordering = ["key"]

    def __str__(self) -> str:
        return f"{self.host.host_name}:{self.key}"

    def get_typed_value(self) -> Any:
        """Convert the stored string value back to its proper type"""
        import json

        if self.value_type == "string":
            return self.value
        elif self.value_type == "integer":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "boolean":
            return str(self.value).lower() in ("true", "1", "yes", "on")
        elif self.value_type in ("json", "list", "dict"):
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return self.value
        else:
            return self.value


class AnsibleInventoryPlugin(AbstractBase):
    """Dynamic inventory plugins configuration"""

    inventory = models.ForeignKey(
        AnsibleInventory, on_delete=models.CASCADE, related_name="plugins"
    )
    name = models.CharField(max_length=64, help_text="Plugin name")
    config = models.JSONField(default=dict, help_text="Plugin configuration")
    enabled = models.BooleanField(default=True, help_text="Whether plugin is enabled")
    priority = models.PositiveIntegerField(default=100, help_text="Plugin priority")
    cache_timeout = models.PositiveIntegerField(default=3600, help_text="Cache timeout in seconds")

    class Meta:
        unique_together = ["inventory", "name"]
        ordering = ["priority", "name"]

    def __str__(self) -> str:
        return f"{self.inventory.name}:{self.name}"


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
        default="yaml",
    )
    template_content = models.TextField(help_text="Template content")
    variables = models.JSONField(default=dict, blank=True, help_text="Template variables")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class AnsibleVariableSet(AbstractBase):
    """Independent variable sets that can be associated with multiple inventories"""

    name = models.CharField(max_length=255, unique=True, help_text="Variable set name")
    description = models.TextField(blank=True, help_text="Variable set description")
    content = models.TextField(help_text="Variable content (YAML/JSON format)")
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
        help_text="Variable set status",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_variable_sets",
    )

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = "Ansible Variable Set"
        verbose_name_plural = "Ansible Variable Sets"

    def __str__(self) -> str:
        return str(self.name)

    def get_parsed_content(self) -> dict:
        """Parse variable content"""
        import json

        import yaml

        try:
            if self.content_type == "yaml":
                return yaml.safe_load(self.content) or {}
            elif self.content_type == "json":
                return json.loads(self.content) or {}
            elif self.content_type == "ini":
                # Simple INI parsing
                result = {}
                for line in self.content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        result[key.strip()] = value.strip()
                return result
            elif self.content_type == "env":
                # Environment variable format parsing
                result = {}
                for line in self.content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        result[key.strip()] = value.strip()
                return result
            else:
                return {}
        except Exception:
            return {}

    def validate_content(self) -> bool:
        """Validate variable content format"""
        try:
            self.get_parsed_content()
            return True
        except Exception:
            return False


class AnsibleInventoryVariableSetAssociation(AbstractBase):
    """Association table for inventory and variable sets (for variable merging)"""

    inventory = models.ForeignKey(
        AnsibleInventory,
        on_delete=models.CASCADE,
        related_name="associated_variable_sets",
    )
    variable_set = models.ForeignKey(
        AnsibleVariableSet,
        on_delete=models.CASCADE,
        related_name="associated_inventories",
    )
    load_priority = models.PositiveIntegerField(
        default=100,
        help_text="Variable loading priority, lower numbers have higher priority",
    )
    enabled = models.BooleanField(default=True, help_text="Whether this variable set is enabled")
    load_tags = models.JSONField(
        default=list, blank=True, help_text="Conditional tags for loading"
    )
    load_config = models.JSONField(
        default=dict, blank=True, help_text="Loading configuration options"
    )

    class Meta:
        unique_together = ["inventory", "variable_set"]
        ordering = ["load_priority", "variable_set__priority"]
        verbose_name = "Inventory Variable Set Association"
        verbose_name_plural = "Inventory Variable Set Associations"

    def __str__(self) -> str:
        return f"{self.inventory.name} -> {self.variable_set.name}"
