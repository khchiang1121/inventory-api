import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from guardian.mixins import GuardianUserMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
    account = models.CharField(max_length=32, unique=True, null=True, blank=True, help_text="Unique account identifier")
    status = models.CharField(max_length=32, choices=[('active', 'Active'), ('inactive', 'Inactive')], help_text="Account status")


# --------------------------------------------------------------------------
# Physical Infrastructure Models
# --------------------------------------------------------------------------
class Fabrication(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Fabrication identifier")
    old_system_id = models.CharField(max_length=100, blank=True, help_text="Identifier from legacy system")


class Phase(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Phase identifier")
    old_system_id = models.CharField(max_length=100, blank=True, help_text="Identifier from legacy system")


class DataCenter(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Data center identifier")
    old_system_id = models.CharField(max_length=100, blank=True, help_text="Identifier from legacy system")


class Room(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Room identifier")
    old_system_id = models.CharField(max_length=100, blank=True, help_text="Identifier from legacy system")


class Rack(AbstractBase):
    name = models.CharField(max_length=32, unique=True, help_text="Rack identifier")
    bgp_number = models.CharField(max_length=20, unique=True, help_text="Associated BGP number")
    as_number = models.PositiveIntegerField(help_text="Autonomous System Number")
    old_system_id = models.CharField(max_length=100, blank=True, help_text="Identifier from legacy system")


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
    ipv4_netmask = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True, help_text="IPv4 netmask")
    ipv6_address = models.GenericIPAddressField(protocol="IPv6", null=True, blank=True, help_text="IPv6 address")
    ipv6_netmask = models.GenericIPAddressField(protocol="IPv6", null=True, blank=True, help_text="IPv6 netmask")
    gateway = models.GenericIPAddressField(null=True, blank=True, help_text="Default gateway")
    dns_servers = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of DNS servers")

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
    issued_by = models.CharField(max_length=100, blank=True, help_text="Procurement staff name or ID")


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
    status = models.CharField(max_length=32, choices=[('active', 'Active'), ('inactive', 'Inactive')], help_text="Group status")


class Brand(AbstractBase):
    name = models.CharField(max_length=100, unique=True, help_text="Vendor brand, e.g., Dell, HPE, etc.")


class BaremetalModel(AbstractBase):
    name = models.CharField(max_length=100, help_text="Model name, e.g., PowerEdge R740")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models", help_text="Server brand")
    total_cpu = models.IntegerField(help_text="Total CPU capacity")
    total_memory = models.IntegerField(help_text="Total memory capacity")
    total_storage = models.IntegerField(help_text="Total storage capacity")


class Baremetal(AbstractBase):
    name = models.CharField(max_length=255, help_text="Server name")
    serial_number = models.CharField(max_length=255, unique=True, help_text="Unique serial number")
    model = models.ForeignKey(BaremetalModel, on_delete=models.PROTECT, related_name="baremetals")
    fabrication = models.ForeignKey(Fabrication, on_delete=models.SET_NULL, null=True, related_name="baremetals")
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True, related_name="baremetals")
    data_center = models.ForeignKey(DataCenter, on_delete=models.SET_NULL, null=True, related_name="baremetals")
    room = models.CharField(max_length=32, blank=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, related_name="baremetals")
    unit = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=32, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('retired', 'Retired')])
    available_cpu = models.IntegerField()
    available_memory = models.IntegerField()
    available_storage = models.IntegerField()
    group = models.ForeignKey(BaremetalGroup, on_delete=models.CASCADE, related_name="baremetals")
    pr = models.ForeignKey(PurchaseRequisition, on_delete=models.PROTECT, related_name="baremetals")
    po = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name="baremetals")
    old_system_id = models.CharField(max_length=100, blank=True)


class Tenant(AbstractBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=[('active', 'Active'), ('inactive', 'Inactive')])


class BaremetalGroupTenantQuota(AbstractBase):
    group = models.ForeignKey(BaremetalGroup, on_delete=models.CASCADE, related_name="tenant_quotas")
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
    scheduling_mode = models.CharField(max_length=50, choices=[("spread_rack", "SpreadByRack"), ("spread_resource", "SpreadByResource"), ("balanced", "Balanced"), ("default", "Default")], default="default")
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)


class K8sClusterPlugin(AbstractBase):
    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE, related_name="plugins")
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    status = models.CharField(max_length=64, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('error', 'Error')])
    additional_info = models.JSONField(blank=True, null=True)


class BastionClusterAssociation(AbstractBase):
    bastion = models.ForeignKey("VirtualMachine", on_delete=models.CASCADE, related_name="managed_clusters")
    k8s_cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE, related_name="bastion_machines")


class ServiceMesh(AbstractBase):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('cilium', 'Cilium'), ('istio', 'Istio'), ('other', 'Other')])
    description = models.TextField(blank=True)
    status = models.CharField(max_length=64, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('error', 'Error')])


class K8sClusterToServiceMesh(AbstractBase):
    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE, related_name="service_meshes")
    service_mesh = models.ForeignKey(ServiceMesh, on_delete=models.CASCADE, related_name="clusters")
    role = models.CharField(max_length=50, choices=[('primary', 'Primary'), ('secondary', 'Secondary')])


class VirtualMachine(AbstractBase):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="virtual_machines")
    baremetal = models.ForeignKey(Baremetal, null=True, on_delete=models.CASCADE, related_name="virtual_machines")
    specification = models.ForeignKey(VirtualMachineSpecification, on_delete=models.CASCADE, related_name="virtual_machines")
    k8s_cluster = models.ForeignKey(K8sCluster, on_delete=models.SET_NULL, blank=True, null=True, related_name="virtual_machines")
    type = models.CharField(max_length=50, choices=[('control-plane', 'K8s Control Plane'), ('worker', 'K8s Worker'), ('management', 'Management'), ('other', "Other")], default='other')
    status = models.CharField(max_length=50)
