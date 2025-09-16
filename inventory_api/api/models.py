import uuid
from typing import Any, Dict, List

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.mixins import GuardianUserMixin


class AbstractBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------------------------------
# User Models
# --------------------------------------------------------------------------
class CustomUser(GuardianUserMixin, AbstractUser):
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


# --------------------------------------------------------------------------
# Physical Infrastructure Models
# --------------------------------------------------------------------------
class Fabrication(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Fabrication identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )


class Phase(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Phase identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )


class DataCenter(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Data center identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )


class Room(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Room identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )


class Rack(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Rack identifier")
    bgp_number = models.CharField(max_length=20, unique=True, help_text="Associated BGP number")
    as_number = models.PositiveIntegerField(help_text="Autonomous System Number")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    height_units = models.PositiveIntegerField(
        default=42, help_text="Total height units in the rack"
    )
    used_units = models.PositiveIntegerField(
        default=0, help_text="Number of units currently in use"
    )
    available_units = models.PositiveIntegerField(
        default=42, help_text="Number of units available"
    )
    power_capacity = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Power capacity in kW"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("maintenance", "Maintenance"),
            ("full", "Full"),
        ],
        default="active",
        help_text="Rack status",
    )


# --------------------------------------------------------------------------
# Network Models
# --------------------------------------------------------------------------
class VLAN(AbstractBase):
    vlan_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=64)


class VRF(AbstractBase):
    name = models.CharField(max_length=64, unique=True)
    route_distinguisher = models.CharField(max_length=64)


class BGPConfig(AbstractBase):
    asn = models.PositiveIntegerField(help_text="Autonomous System Number")
    peer_ip = models.GenericIPAddressField(protocol="IPv4", help_text="BGP peer IP")
    local_ip = models.GenericIPAddressField(protocol="IPv4", help_text="Local BGP IP")
    password = models.CharField(max_length=64, blank=True)


class NetworkInterface(AbstractBase):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    resource = GenericForeignKey("content_type", "object_id")

    name = models.CharField(max_length=64, help_text="Interface name, e.g., eth0")
    mac_address = models.CharField(max_length=32, help_text="MAC address")
    is_primary = models.BooleanField(default=False, help_text="Marks primary interface")

    ipv4_address = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
    ipv4_netmask = models.GenericIPAddressField(
        protocol="IPv4", null=True, blank=True, help_text="IPv4 netmask"
    )
    ipv6_address = models.GenericIPAddressField(
        protocol="IPv6", null=True, blank=True, help_text="IPv6 address"
    )
    ipv6_netmask = models.GenericIPAddressField(
        protocol="IPv6", null=True, blank=True, help_text="IPv6 netmask"
    )
    gateway = models.GenericIPAddressField(null=True, blank=True, help_text="Default gateway")
    dns_servers = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated list of DNS servers"
    )

    vlan = models.ForeignKey(VLAN, null=True, blank=True, on_delete=models.SET_NULL)
    vrf = models.ForeignKey(VRF, null=True, blank=True, on_delete=models.SET_NULL)
    bgp_config = models.OneToOneField(BGPConfig, null=True, blank=True, on_delete=models.SET_NULL)


# --------------------------------------------------------------------------
# Purchase Models
# --------------------------------------------------------------------------
class PurchaseRequisition(AbstractBase):
    pr_number = models.CharField(max_length=64, unique=True, help_text="PR number")
    requested_by = models.CharField(max_length=100, help_text="Requester name or ID")
    department = models.CharField(max_length=100, blank=True, help_text="Requesting department")
    reason = models.TextField(blank=True, help_text="Purpose or justification for the requisition")
    submit_date = models.DateField(auto_now_add=True)


class PurchaseOrder(AbstractBase):
    po_number = models.CharField(max_length=64, unique=True, help_text="PO number")
    vendor_name = models.CharField(max_length=255, help_text="Vendor name")
    payment_terms = models.CharField(max_length=128, blank=True, help_text="Payment terms")
    delivery_date = models.DateField(null=True, blank=True)
    issued_by = models.CharField(
        max_length=100, blank=True, help_text="Procurement staff name or ID"
    )


# --------------------------------------------------------------------------
# Baremetal Models
# --------------------------------------------------------------------------
class BaremetalGroup(AbstractBase):
    name = models.CharField(max_length=255, help_text="Name of the baremetal group")
    description = models.TextField(blank=True, help_text="Description of the group")
    total_cpu = models.IntegerField(help_text="Total CPU capacity")
    total_memory = models.IntegerField(help_text="Total memory capacity")
    total_storage = models.IntegerField(help_text="Total storage capacity")
    available_cpu = models.IntegerField(help_text="Available CPU capacity")
    available_memory = models.IntegerField(help_text="Available memory capacity")
    available_storage = models.IntegerField(help_text="Available storage capacity")
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Group status",
    )


class Brand(AbstractBase):
    name = models.CharField(
        max_length=100, unique=True, help_text="Vendor brand, e.g., Dell, HPE, etc."
    )


class BaremetalModel(AbstractBase):
    name = models.CharField(max_length=100, help_text="Model name, e.g., PowerEdge R740")
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="models", help_text="Server brand"
    )
    total_cpu = models.IntegerField(help_text="Total CPU capacity")
    total_memory = models.IntegerField(help_text="Total memory capacity")
    total_storage = models.IntegerField(help_text="Total storage capacity")


class Baremetal(AbstractBase):
    name = models.CharField(max_length=255, help_text="Server name")
    serial_number = models.CharField(max_length=255, unique=True, help_text="Unique serial number")
    model = models.ForeignKey(BaremetalModel, on_delete=models.PROTECT, related_name="baremetals")
    fabrication = models.ForeignKey(
        Fabrication, on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    phase = models.ForeignKey(
        Phase, on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    data_center = models.ForeignKey(
        DataCenter, on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    room = models.CharField(max_length=32, blank=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, related_name="baremetals")
    unit = models.CharField(max_length=32, blank=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("pending", "Pending"),
            ("retired", "Retired"),
        ],
    )
    available_cpu = models.IntegerField()
    available_memory = models.IntegerField()
    available_storage = models.IntegerField()
    group = models.ForeignKey(BaremetalGroup, on_delete=models.CASCADE, related_name="baremetals")
    pr = models.ForeignKey(
        PurchaseRequisition, on_delete=models.PROTECT, related_name="baremetals"
    )
    po = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name="baremetals")
    external_system_id = models.CharField(max_length=100, blank=True)


class Tenant(AbstractBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )


class BaremetalGroupTenantQuota(AbstractBase):
    group = models.ForeignKey(
        BaremetalGroup, on_delete=models.CASCADE, related_name="tenant_quotas"
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="group_quotas")
    cpu_quota_percentage = models.FloatField()
    memory_quota = models.IntegerField()
    storage_quota = models.IntegerField()


# --------------------------------------------------------------------------
# Virtual Resources & Cloud Models
# --------------------------------------------------------------------------
class VirtualMachineSpecification(AbstractBase):
    name = models.CharField(max_length=255)
    generation = models.CharField(max_length=32)
    required_cpu = models.IntegerField()
    required_memory = models.IntegerField()
    required_storage = models.IntegerField()


class K8sCluster(AbstractBase):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="k8s_clusters")
    scheduling_mode = models.CharField(
        max_length=50,
        choices=[
            ("spread_rack", "SpreadByRack"),
            ("spread_resource", "SpreadByResource"),
            ("balanced", "Balanced"),
            ("default", "Default"),
        ],
        default="default",
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)


class K8sClusterPlugin(AbstractBase):
    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE, related_name="plugins")
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
    )
    additional_info = models.JSONField(blank=True, null=True)


class BastionClusterAssociation(AbstractBase):
    bastion = models.ForeignKey(
        "VirtualMachine", on_delete=models.CASCADE, related_name="managed_clusters"
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="bastion_machines"
    )


class ServiceMesh(AbstractBase):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[("cilium", "Cilium"), ("istio", "Istio"), ("other", "Other")],
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
    )


class K8sClusterToServiceMesh(AbstractBase):
    cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="service_meshes"
    )
    service_mesh = models.ForeignKey(
        ServiceMesh, on_delete=models.CASCADE, related_name="clusters"
    )
    role = models.CharField(
        max_length=50, choices=[("primary", "Primary"), ("secondary", "Secondary")]
    )


class VirtualMachine(AbstractBase):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="virtual_machines")
    baremetal = models.ForeignKey(
        Baremetal, null=True, on_delete=models.CASCADE, related_name="virtual_machines"
    )
    specification = models.ForeignKey(
        VirtualMachineSpecification,
        on_delete=models.CASCADE,
        related_name="virtual_machines",
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="virtual_machines",
    )
    type = models.CharField(
        max_length=50,
        choices=[
            ("control-plane", "K8s Control Plane"),
            ("worker", "K8s Worker"),
            ("management", "Management"),
            ("other", "Other"),
        ],
        default="other",
    )
    status = models.CharField(max_length=50)


# --------------------------------------------------------------------------
# Enhanced Ansible Inventory Models
# --------------------------------------------------------------------------


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
    group = models.ForeignKey(AnsibleGroup, on_delete=models.CASCADE, related_name="hosts")

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
        unique_together = ["inventory", "group", "content_type", "object_id"]
        verbose_name = "Ansible Host"
        verbose_name_plural = "Ansible Hosts"

    def __str__(self) -> str:
        return f"{self.host} in {self.group.name}"

    @property
    def host_name(self) -> str:
        """Get the name of the host (VM or Baremetal)"""
        if hasattr(self.host, "name"):
            return self.host.name
        return str(self.host)

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
