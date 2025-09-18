from datetime import datetime  # noqa: F401
from uuid import UUID  # noqa: F401

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .. import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ["id", "username", "password", "email", "account", "status"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile information (excludes sensitive fields)"""

    class Meta:
        model = models.CustomUser
        fields = ["id", "username", "email", "account", "status"]


# ------------------------------------------------------------------------------
# Infrastructure Serializers
# ------------------------------------------------------------------------------
class FabSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["id", "name", "external_system_id", "created_at", "updated_at"]


class FabCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["id", "name", "external_system_id", "created_at", "updated_at"]


class FabUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["id", "name", "external_system_id", "created_at", "updated_at"]


class PhaseSerializer(serializers.ModelSerializer):
    fab = FabSerializer(read_only=True)

    class Meta:
        model = models.Phase
        fields = ["id", "name", "external_system_id", "fab", "created_at", "updated_at"]


class PhaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phase
        fields = ["id", "name", "external_system_id", "fab", "created_at", "updated_at"]


class PhaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phase
        fields = ["id", "name", "external_system_id", "fab", "created_at", "updated_at"]


class DataCenterSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer(read_only=True)

    class Meta:
        model = models.DataCenter
        fields = ["id", "name", "external_system_id", "phase", "created_at", "updated_at"]


class DataCenterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataCenter
        fields = ["id", "name", "external_system_id", "phase", "created_at", "updated_at"]


class DataCenterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataCenter
        fields = ["id", "name", "external_system_id", "phase", "created_at", "updated_at"]


class RoomSerializer(serializers.ModelSerializer):
    datacenter = DataCenterSerializer(read_only=True)

    class Meta:
        model = models.Room
        fields = ["id", "name", "external_system_id", "datacenter", "created_at", "updated_at"]


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["id", "name", "external_system_id", "datacenter", "created_at", "updated_at"]


class RoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["id", "name", "external_system_id", "datacenter", "created_at", "updated_at"]


class RackSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = models.Rack
        fields = [
            "id",
            "name",
            "room",
            "external_system_id",
            "bgp_number",
            "as_number",
            "height_units",
            "used_units",
            "available_units",
            "power_capacity",
            "status",
            "created_at",
            "updated_at"
        ]


class RackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        fields = [
            "id",
            "name",
            "external_system_id",
            "room",
            "bgp_number",
            "as_number",
            "height_units",
            "used_units",
            "available_units",
            "power_capacity",
            "status",
            "created_at",
            "updated_at"
        ]


class RackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        fields = [
            "id",
            "name",
            "external_system_id",
            "room",
            "bgp_number",
            "as_number",
            "height_units",
            "used_units",
            "available_units",
            "power_capacity",
            "status",
            "created_at",
            "updated_at"
        ]


class UnitSerializer(serializers.ModelSerializer):
    rack = RackSerializer(read_only=True)

    class Meta:
        model = models.Unit
        fields = ["id", "name", "unit_number", "rack", "created_at", "updated_at"]


class UnitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = ["id", "name", "unit_number", "rack", "created_at", "updated_at"]


class UnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = ["id", "name", "unit_number", "rack", "created_at", "updated_at"]


# ------------------------------------------------------------------------------
# Network Serializers
# ------------------------------------------------------------------------------
class VLANSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VLAN
        fields = ["id", "vlan_id", "name", "created_at", "updated_at"]


class VRFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VRF
        fields = [
            "id",
            "name",
            "route_distinguisher",
            "created_at",
            "updated_at",
        ]


class BGPConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGPConfig
        fields = [
            "id",
            "asn",
            "peer_ip",
            "local_ip",
            "password",
            "created_at",
            "updated_at",
        ]


class ResourceRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": str(value.id),
            "type": value._meta.model_name,
            "name": value.name,
        }

    # Silence abstract method warnings in strict linters; we only use this as
    # a read-only field.
    def to_internal_value(self, data):  # type: ignore[override]
        raise NotImplementedError("Read-only field")


class NetworkInterfaceSerializer(serializers.ModelSerializer):
    vlan = VLANSerializer(read_only=True)
    vrf = VRFSerializer(read_only=True)
    bgp_config = BGPConfigSerializer(read_only=True)
    resource = ResourceRelatedField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), write_only=True
    )
    object_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.NetworkInterface
        fields = [
            "id",
            "resource",
            "content_type",
            "object_id",
            "name",
            "mac_address",
            "is_primary",
            "ipv4_address",
            "ipv4_netmask",
            "ipv6_address",
            "ipv6_netmask",
            "gateway",
            "dns_servers",
            "vlan",
            "vrf",
            "bgp_config",
            "created_at",
            "updated_at",
        ]


# Baremetal Group Serializers
class BaremetalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = [
            "id",
            "name",
            "description",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "status",
            "created_at",
            "updated_at",
        ]


class BaremetalGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = [
            "id",
            "name",
            "description",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "status",
        ]


class BaremetalGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = [
            "name",
            "description",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "status",
        ]


# ------------------------------------------------------------------------------
# Purchase Serializers
# ------------------------------------------------------------------------------
class PurchaseRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRequisition
        fields = [
            "id",
            "pr_number",
            "requested_by",
            "department",
            "reason",
            "submit_date",
            "created_at",
            "updated_at",
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseOrder
        fields = [
            "id",
            "po_number",
            "vendor_name",
            "payment_terms",
            "delivery_date",
            "issued_by",
            "created_at",
            "updated_at",
        ]


# ------------------------------------------------------------------------------
# Baremetal Serializers
# ------------------------------------------------------------------------------
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ["id", "name", "created_at", "updated_at"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = [
            "id",
            "name",
            "contact_email",
            "contact_phone",
            "address",
            "website",
            "created_at",
            "updated_at",
        ]


class BaremetalModelSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    suppliers = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = models.BaremetalModel
        fields = [
            "id",
            "name",
            "manufacturer",
            "suppliers",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
            "created_at",
            "updated_at",
        ]


class BaremetalModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModel
        fields = [
            "id",
            "name",
            "manufacturer",
            "suppliers",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
        ]
        read_only_fields = ["id"]


class BaremetalModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModel
        fields = [
            "id",
            "name",
            "manufacturer",
            "suppliers",
            "total_cpu",
            "total_memory",
            "total_storage",
            "total_gpu",
        ]
        read_only_fields = ["id"]


# Baremetal Serializers
class BaremetalSerializer(serializers.ModelSerializer):
    rack = RackSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)
    group = BaremetalGroupSerializer(read_only=True)
    model = BaremetalModelSerializer(read_only=True)
    fabrication = FabSerializer(read_only=True)
    phase = PhaseSerializer(read_only=True)
    data_center = DataCenterSerializer(read_only=True)
    pr = PurchaseRequisitionSerializer(read_only=True)
    po = PurchaseOrderSerializer(read_only=True)

    class Meta:
        model = models.Baremetal
        fields = [
            "id",
            "name",
            "serial_number",
            "model",
            "fabrication",
            "phase",
            "data_center",
            "room",
            "rack",
            "unit",
            "status",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "group",
            "pr",
            "po",
            "external_system_id",
            "created_at",
            "updated_at",
        ]


class BaremetalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = [
            "id",
            "name",
            "serial_number",
            "model",
            "fabrication",
            "phase",
            "data_center",
            "room",
            "rack",
            "unit",
            "status",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "group",
            "pr",
            "po",
            "external_system_id",
        ]


class BaremetalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = [
            "id",
            "name",
            "serial_number",
            "model",
            "fabrication",
            "phase",
            "data_center",
            "room",
            "rack",
            "unit",
            "status",
            "available_cpu",
            "available_memory",
            "available_storage",
            "available_gpu",
            "group",
            "pr",
            "po",
            "external_system_id",
        ]


# Baremetal Group Tenant Quota Serializers
class BaremetalGroupTenantQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "id",
            "group",
            "tenant",
            "cpu_quota_percentage",
            "memory_quota",
            "storage_quota",
            "gpu_quota",
            "created_at",
            "updated_at",
        ]


class BaremetalGroupTenantQuotaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "id",
            "group",
            "tenant",
            "cpu_quota_percentage",
            "memory_quota",
            "storage_quota",
            "gpu_quota",
        ]


class BaremetalGroupTenantQuotaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "id",
            "group",
            "tenant",
            "cpu_quota_percentage",
            "memory_quota",
            "storage_quota",
            "gpu_quota",
        ]


# Tenant Serializers
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ["id", "name", "description", "status", "created_at", "updated_at"]


class TenantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ["id", "name", "description", "status"]


class TenantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ["id", "name", "description", "status"]


# Virtual Machine Specification Serializers
class VirtualMachineSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = [
            "id",
            "name",
            "generation",
            "required_cpu",
            "required_memory",
            "required_storage",
            "created_at",
            "updated_at",
        ]


class VirtualMachineSpecificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = [
            "id",
            "name",
            "generation",
            "required_cpu",
            "required_memory",
            "required_storage",
        ]


class VirtualMachineSpecificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = [
            "id",
            "name",
            "generation",
            "required_cpu",
            "required_memory",
            "required_storage",
        ]


# K8s Cluster Serializers
class K8sClusterSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = models.K8sCluster
        fields = [
            "id",
            "name",
            "version",
            "tenant",
            "scheduling_mode",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]


class K8sClusterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = [
            "id",
            "name",
            "version",
            "tenant",
            "scheduling_mode",
            "description",
            "status",
        ]


class K8sClusterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = [
            "id",
            "name",
            "version",
            "tenant",
            "scheduling_mode",
            "description",
            "status",
        ]


# K8s Cluster Plugin Serializers
class K8sClusterPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = [
            "id",
            "cluster",
            "name",
            "version",
            "status",
            "additional_info",
            "created_at",
            "updated_at",
        ]


class K8sClusterPluginCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ["id", "cluster", "name", "version", "status", "additional_info"]


class K8sClusterPluginUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ["id", "cluster", "name", "version", "status", "additional_info"]


# Bastion Cluster Association Serializers
class BastionClusterAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ["id", "bastion", "k8s_cluster", "created_at", "updated_at"]


class BastionClusterAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ["id", "bastion", "k8s_cluster"]


class BastionClusterAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ["id", "bastion", "k8s_cluster"]


# K8s Cluster To Service Mesh Serializers
class K8sClusterToServiceMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = [
            "id",
            "cluster",
            "service_mesh",
            "role",
            "created_at",
            "updated_at",
        ]


class K8sClusterToServiceMeshCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ["id", "cluster", "service_mesh", "role"]


class K8sClusterToServiceMeshUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ["id", "cluster", "service_mesh", "role"]


# Service Mesh Serializers
class ServiceMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = [
            "id",
            "name",
            "type",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]


class ServiceMeshCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = ["id", "name", "type", "description", "status"]


class ServiceMeshUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = ["id", "name", "type", "description", "status"]


# Virtual Machine Serializers
class VirtualMachineSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    baremetal = BaremetalSerializer(read_only=True)
    specification = VirtualMachineSpecificationSerializer(read_only=True)
    k8s_cluster = K8sClusterSerializer(read_only=True)

    class Meta:
        model = models.VirtualMachine
        fields = [
            "id",
            "name",
            "tenant",
            "baremetal",
            "specification",
            "k8s_cluster",
            "type",
            "status",
            "created_at",
            "updated_at",
        ]


class VirtualMachineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = [
            "id",
            "name",
            "tenant",
            "baremetal",
            "specification",
            "k8s_cluster",
            "type",
            "status",
        ]


class VirtualMachineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = [
            "name",
            "tenant",
            "baremetal",
            "specification",
            "k8s_cluster",
            "type",
            "status",
        ]


# ------------------------------------------------------------------------------
# Permission Serializers
# ------------------------------------------------------------------------------
class ObjectPermissionSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    object_id = serializers.CharField()
    user_id = serializers.CharField(required=False)
    group_id = serializers.CharField(required=False)
    permission = serializers.CharField()


# ------------------------------------------------------------------------------
# Ansible Inventory Serializers
# ------------------------------------------------------------------------------
class AnsibleInventorySerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    groups_count = serializers.SerializerMethodField()
    hosts_count = serializers.SerializerMethodField()
    associated_variable_sets_count = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleInventory
        fields = [
            "id",
            "name",
            "description",
            "version",
            "source_type",
            "source_plugin",
            "source_config",
            "status",
            "created_by",
            "groups_count",
            "hosts_count",
            "associated_variable_sets_count",
            "created_at",
            "updated_at",
        ]

    def get_groups_count(self, obj) -> int:
        return obj.groups.count()

    def get_hosts_count(self, obj) -> int:
        return obj.hosts.count()

    def get_associated_variable_sets_count(self, obj) -> int:
        return obj.associated_variable_sets.count()


class AnsibleInventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventory
        fields = [
            "id",
            "name",
            "description",
            "version",
            "source_type",
            "source_plugin",
            "source_config",
            "status",
        ]


class AnsibleInventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventory
        fields = [
            "name",
            "description",
            "version",
            "source_type",
            "source_plugin",
            "source_config",
            "status",
        ]


class AnsibleInventoryVariableSerializer(serializers.ModelSerializer):
    inventory = AnsibleInventorySerializer(read_only=True)

    class Meta:
        model = models.AnsibleInventoryVariable
        fields = [
            "id",
            "inventory",
            "key",
            "value",
            "value_type",
            "created_at",
            "updated_at",
        ]


class AnsibleInventoryVariableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariable
        fields = ["id", "inventory", "key", "value", "value_type"]


class AnsibleInventoryVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariable
        fields = ["key", "value", "value_type"]


# ------------------------------------------------------------------------------
# Ansible Variable Set Serializers
# ------------------------------------------------------------------------------
class AnsibleVariableSetSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    associated_inventories_count = serializers.SerializerMethodField()
    parsed_content = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleVariableSet
        fields = [
            "id",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
            "created_by",
            "associated_inventories_count",
            "parsed_content",
            "created_at",
            "updated_at",
        ]

    def get_associated_inventories_count(self, obj) -> int:
        return obj.associated_inventories.count()

    def get_parsed_content(self, obj) -> dict:
        return obj.get_parsed_content()


class AnsibleVariableSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleVariableSet
        fields = [
            "id",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
        ]


class AnsibleVariableSetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleVariableSet
        fields = [
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
        ]


class AnsibleInventoryVariableSetAssociationSerializer(serializers.ModelSerializer):
    inventory = AnsibleInventorySerializer(read_only=True)
    variable_set = AnsibleVariableSetSerializer(read_only=True)

    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "id",
            "inventory",
            "variable_set",
            "load_priority",
            "enabled",
            "load_tags",
            "load_config",
            "created_at",
            "updated_at",
        ]


class AnsibleInventoryVariableSetAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "id",
            "inventory",
            "variable_set",
            "load_priority",
            "enabled",
            "load_tags",
            "load_config",
        ]


class AnsibleInventoryVariableSetAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "load_priority",
            "enabled",
            "load_tags",
            "load_config",
        ]


# ------------------------------------------------------------------------------
# Ansible Host Variable Serializers
# ------------------------------------------------------------------------------
class AnsibleHostVariableSerializer(serializers.ModelSerializer):
    host: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.AnsibleHostVariable
        fields = [
            "id",
            "host",
            "key",
            "value",
            "value_type",
            "created_at",
            "updated_at",
        ]


class AnsibleHostVariableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleHostVariable
        fields = ["id", "host", "key", "value", "value_type"]


class AnsibleHostVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleHostVariable
        fields = ["key", "value", "value_type"]


# ------------------------------------------------------------------------------
# Ansible Inventory Plugin Serializers
# ------------------------------------------------------------------------------
class AnsibleInventoryPluginSerializer(serializers.ModelSerializer):
    inventory = AnsibleInventorySerializer(read_only=True)

    class Meta:
        model = models.AnsibleInventoryPlugin
        fields = [
            "id",
            "inventory",
            "name",
            "config",
            "enabled",
            "priority",
            "cache_timeout",
            "created_at",
            "updated_at",
        ]


class AnsibleInventoryPluginCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryPlugin
        fields = [
            "id",
            "inventory",
            "name",
            "config",
            "enabled",
            "priority",
            "cache_timeout",
        ]


class AnsibleInventoryPluginUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryPlugin
        fields = [
            "name",
            "config",
            "enabled",
            "priority",
            "cache_timeout",
        ]


# ------------------------------------------------------------------------------
# Ansible Inventory Template Serializers
# ------------------------------------------------------------------------------
class AnsibleInventoryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryTemplate
        fields = [
            "id",
            "name",
            "description",
            "template_type",
            "template_content",
            "variables",
            "created_at",
            "updated_at",
        ]


class AnsibleInventoryTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryTemplate
        fields = [
            "id",
            "name",
            "description",
            "template_type",
            "template_content",
            "variables",
        ]


class AnsibleInventoryTemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryTemplate
        fields = [
            "name",
            "description",
            "template_type",
            "template_content",
            "variables",
        ]


class AnsibleGroupVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = [
            "id",
            "group",
            "key",
            "value",
            "value_type",
            "created_at",
            "updated_at",
        ]


class AnsibleGroupVariableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = ["id", "group", "key", "value", "value_type"]


class AnsibleGroupVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = ["key", "value", "value_type"]


class AnsibleGroupRelationshipSerializer(serializers.ModelSerializer):
    parent_group = serializers.PrimaryKeyRelatedField(queryset=models.AnsibleGroup.objects.all())
    child_group = serializers.PrimaryKeyRelatedField(queryset=models.AnsibleGroup.objects.all())

    class Meta:
        model = models.AnsibleGroupRelationship
        fields = ["id", "parent_group", "child_group", "created_at", "updated_at"]


class AnsibleGroupRelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupRelationship
        fields = ["id", "parent_group", "child_group"]


class AnsibleGroupRelationshipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupRelationship
        fields = ["parent_group", "child_group"]


class AnsibleGroupSerializer(serializers.ModelSerializer):
    variables = AnsibleGroupVariableSerializer(many=True, read_only=True)
    child_groups = serializers.SerializerMethodField()
    parent_groups = serializers.SerializerMethodField()
    all_variables = serializers.SerializerMethodField()
    all_hosts = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleGroup
        fields = [
            "id",
            "inventory",
            "name",
            "description",
            "is_special",
            "status",
            "variables",
            "child_groups",
            "parent_groups",
            "all_variables",
            "all_hosts",
            "created_at",
            "updated_at",
        ]

    def get_child_groups(self, obj):
        return [{"id": str(group.id), "name": group.name} for group in obj.child_groups]

    def get_parent_groups(self, obj):
        return [{"id": str(group.id), "name": group.name} for group in obj.parent_groups]

    def get_all_variables(self, obj):
        return obj.all_variables

    def get_all_hosts(self, obj):
        hosts = obj.all_hosts
        return [
            {
                "id": str(host.id),
                "name": getattr(host, "name", str(host)),
                "type": host._meta.model_name,
            }
            for host in hosts
        ]


class AnsibleGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroup
        fields = ["id", "inventory", "name", "description", "is_special", "status"]


class AnsibleGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroup
        fields = ["id", "inventory", "name", "description", "is_special", "status"]


class AnsibleHostSerializer(serializers.ModelSerializer):
    groups = AnsibleGroupSerializer(many=True, read_only=True)
    host = ResourceRelatedField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), write_only=True
    )
    object_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.AnsibleHost
        fields = [
            "id",
            "groups",
            "host",
            "content_type",
            "object_id",
            "metadata",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "created_at",
            "updated_at",
        ]


class AnsibleHostCreateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=models.AnsibleGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = models.AnsibleHost
        fields = [
            "id",
            "inventory",
            "groups",
            "content_type",
            "object_id",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "metadata",
        ]

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        host = models.AnsibleHost.objects.create(**validated_data)
        if groups:
            host.groups.set(groups)
        return host


class AnsibleHostUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=models.AnsibleGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = models.AnsibleHost
        fields = [
            "inventory",
            "groups",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "metadata",
        ]

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update groups if provided
        if groups is not None:
            instance.groups.set(groups)

        return instance
