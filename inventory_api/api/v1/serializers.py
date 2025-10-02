from datetime import datetime  # noqa: F401
from uuid import UUID  # noqa: F401

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .. import models


# ------------------------------------------------------------------------------
# Helper Classes and Shared Serializers
# ------------------------------------------------------------------------------
class ResourceRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": str(value.id),
            "type": value._meta.model_name,
            "name": getattr(value, "name", str(value)),
        }

    # Silence abstract method warnings in strict linters; we only use this as
    # a read-only field.
    def to_internal_value(self, data):  # type: ignore[override]
        raise NotImplementedError("Read-only field")


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ["id", "username", "password", "email", "account", "status"]
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ["id", "username", "password", "email", "account", "status"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ["username", "email", "account", "status"]


# class UserProfileSerializer(serializers.ModelSerializer):
#     """Serializer for user profile information (excludes sensitive fields)"""

#     class Meta:
#         model = models.CustomUser
#         fields = ["id", "username", "email", "account", "status"]


# ------------------------------------------------------------------------------
# Ansible ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# AnsibleGroupVariable Serializers
class AnsibleGroupVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = [
            "id",
            "ansible_group",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
            "created_at",
            "updated_at",
        ]


class AnsibleGroupVariableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = [
            "id",
            "ansible_group",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
        ]


class AnsibleGroupVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroupVariable
        fields = ["name", "description", "content", "content_type", "tags", "priority", "status"]


# AnsibleGroup Serializers
class AnsibleGroupSerializer(serializers.ModelSerializer):
    ansible_group_variables = AnsibleGroupVariableSerializer(many=True, read_only=True)
    child_groups = serializers.SerializerMethodField()
    parent_groups = serializers.SerializerMethodField()
    ansible_hosts = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleGroup
        fields = [
            "id",
            "ansible_inventory",
            "name",
            "description",
            "is_special",
            "status",
            "ansible_group_variables",
            "child_groups",
            "parent_groups",
            "ansible_hosts",
            "created_at",
            "updated_at",
        ]

    def get_child_groups(self, obj):
        return [{"id": str(group.id), "name": group.name} for group in obj.child_groups]

    def get_parent_groups(self, obj):
        return [{"id": str(group.id), "name": group.name} for group in obj.parent_groups]

    def get_ansible_hosts(self, obj):
        hosts = obj.ansible_hosts.all()
        return [
            {
                "id": str(host.id),
                "host": str(host.host),
            }
            for host in hosts
        ]


class AnsibleGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroup
        fields = ["id", "ansible_inventory", "name", "description", "is_special", "status"]


class AnsibleGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleGroup
        fields = ["ansible_inventory", "name", "description", "is_special", "status"]


# AnsibleGroupRelationship Serializers
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


# AnsibleHost Serializers
class AnsibleHostSerializer(serializers.ModelSerializer):
    ansible_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    host = ResourceRelatedField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), write_only=True
    )
    object_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.AnsibleHost
        fields = [
            "id",
            "ansible_inventory",
            "ansible_groups",
            "host",
            "content_type",
            "object_id",
            "aliases",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "ansible_ssh_common_args",
            "ansible_ssh_extra_args",
            "ansible_ssh_pipelining",
            "ansible_ssh_executable",
            "ansible_python_interpreter",
            "ansible_shell_type",
            "status",
            "metadata",
            "created_at",
            "updated_at",
        ]


class AnsibleHostCreateSerializer(serializers.ModelSerializer):
    ansible_groups = serializers.PrimaryKeyRelatedField(
        queryset=models.AnsibleGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = models.AnsibleHost
        fields = [
            "id",
            "ansible_inventory",
            "ansible_groups",
            "content_type",
            "object_id",
            "aliases",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "ansible_ssh_common_args",
            "ansible_ssh_extra_args",
            "ansible_ssh_pipelining",
            "ansible_ssh_executable",
            "ansible_python_interpreter",
            "ansible_shell_type",
            "status",
            "metadata",
        ]

    def create(self, validated_data):
        ansible_groups = validated_data.pop("ansible_groups", [])
        host = models.AnsibleHost.objects.create(**validated_data)
        if ansible_groups:
            host.ansible_groups.set(ansible_groups)
        return host


class AnsibleHostUpdateSerializer(serializers.ModelSerializer):
    ansible_groups = serializers.PrimaryKeyRelatedField(
        queryset=models.AnsibleGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = models.AnsibleHost
        fields = [
            "ansible_inventory",
            "ansible_groups",
            "aliases",
            "ansible_host",
            "ansible_port",
            "ansible_user",
            "ansible_ssh_private_key_file",
            "ansible_ssh_common_args",
            "ansible_ssh_extra_args",
            "ansible_ssh_pipelining",
            "ansible_ssh_executable",
            "ansible_python_interpreter",
            "ansible_shell_type",
            "status",
            "metadata",
        ]

    def update(self, instance, validated_data):
        ansible_groups = validated_data.pop("ansible_groups", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update groups if provided
        if ansible_groups is not None:
            instance.ansible_groups.set(ansible_groups)

        return instance


# AnsibleHostVariable Serializers
class AnsibleHostVariableSerializer(serializers.ModelSerializer):
    ansible_host = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.AnsibleHostVariable
        fields = [
            "id",
            "ansible_host",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
            "created_at",
            "updated_at",
        ]


class AnsibleHostVariableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleHostVariable
        fields = [
            "id",
            "ansible_host",
            "name",
            "description",
            "content",
            "content_type",
            "tags",
            "priority",
            "status",
        ]


class AnsibleHostVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleHostVariable
        fields = ["name", "description", "content", "content_type", "tags", "priority", "status"]


# AnsibleInventory Serializers
class AnsibleInventorySerializer(serializers.ModelSerializer):
    groups_count = serializers.SerializerMethodField()
    hosts_count = serializers.SerializerMethodField()
    associated_variable_sets_count = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleInventory
        fields = [
            "id",
            "name",
            "description",
            "source_type",
            "status",
            "groups_count",
            "hosts_count",
            "associated_variable_sets_count",
            "created_at",
            "updated_at",
        ]

    def get_groups_count(self, obj) -> int:
        return obj.ansible_groups.count()

    def get_hosts_count(self, obj) -> int:
        return obj.ansible_hosts.count()

    def get_associated_variable_sets_count(self, obj) -> int:
        return obj.associated_variable_sets.count()


class AnsibleInventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventory
        fields = [
            "id",
            "name",
            "description",
            "source_type",
            "status",
        ]


class AnsibleInventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventory
        fields = [
            "name",
            "description",
            "source_type",
            "status",
        ]


# AnsibleInventoryTemplate Serializers
class AnsibleInventoryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryTemplate
        fields = [
            "id",
            "name",
            "description",
            "template_type",
            "template_content",
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
        ]


class AnsibleInventoryTemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryTemplate
        fields = [
            "name",
            "description",
            "template_type",
            "template_content",
        ]


# AnsibleVariableSet Serializers
class AnsibleVariableSetSerializer(serializers.ModelSerializer):
    associated_inventories_count = serializers.SerializerMethodField()

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
            "associated_inventories_count",
            "created_at",
            "updated_at",
        ]

    def get_associated_inventories_count(self, obj) -> int:
        return obj.associated_inventories.count()


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


# AnsibleInventoryVariableSetAssociation Serializers
class AnsibleInventoryVariableSetAssociationSerializer(serializers.ModelSerializer):
    ansible_inventory = AnsibleInventorySerializer(read_only=True)
    ansible_variable_set = AnsibleVariableSetSerializer(read_only=True)

    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "id",
            "ansible_inventory",
            "ansible_variable_set",
            "load_priority",
            "enabled",
            "created_at",
            "updated_at",
        ]


class AnsibleInventoryVariableSetAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "id",
            "ansible_inventory",
            "ansible_variable_set",
            "load_priority",
            "enabled",
        ]


class AnsibleInventoryVariableSetAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnsibleInventoryVariableSetAssociation
        fields = [
            "load_priority",
            "enabled",
        ]


# ------------------------------------------------------------------------------
# Purchase ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------
# PurchaseRequisition Serializers
class PurchaseRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRequisition
        fields = [
            "id",
            "name",
            "description",
            "pr_number",
            "requested_by",
            "department",
            "reason",
            "submit_date",
            "created_at",
            "updated_at",
        ]


class PurchaseRequisitionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRequisition
        fields = [
            "id",
            "name",
            "description",
            "pr_number",
            "requested_by",
            "department",
            "reason",
        ]


class PurchaseRequisitionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRequisition
        fields = [
            "name",
            "description",
            "pr_number",
            "requested_by",
            "department",
            "reason",
        ]


# PurchaseOrder Serializers
class PurchaseOrderSerializer(serializers.ModelSerializer):
    purchase_requisition = PurchaseRequisitionSerializer(read_only=True)

    class Meta:
        model = models.PurchaseOrder
        fields = [
            "id",
            "po_number",
            "purchase_requisition",
            "supplier",
            "payment_terms",
            "amount",
            "used",
            "description",
            "created_at",
            "updated_at",
        ]


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseOrder
        fields = [
            "id",
            "po_number",
            "purchase_requisition",
            "supplier",
            "payment_terms",
            "amount",
            "used",
            "description",
        ]


class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseOrder
        fields = [
            "po_number",
            "purchase_requisition",
            "supplier",
            "payment_terms",
            "amount",
            "used",
            "description",
        ]


# ------------------------------------------------------------------------------
# Baremetal ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# Unit Serializers
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = ["id", "name", "unit_number", "rack", "bgp", "created_at", "updated_at"]


class UnitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = ["id", "name", "unit_number", "rack", "bgp"]


class UnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = ["name", "unit_number", "rack", "bgp"]


# BaremetalGroup Serializers
class BaremetalGroupSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True, read_only=True)
    user_group = serializers.SerializerMethodField()

    class Meta:
        model = models.BaremetalGroup
        fields = [
            "id",
            "name",
            "description",
            "total_cpu_cores",
            "total_memory_mib",
            "total_storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "status",
            "user",
            "user_group",
            "is_multi_tenant",
            "labels",
            "created_at",
            "updated_at",
        ]

    def get_user_group(self, obj):
        return [{"id": str(ug.id), "name": ug.name} for ug in obj.user_group.all()]


class BaremetalGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = [
            "id",
            "name",
            "description",
            "total_cpu_cores",
            "total_memory_mib",
            "total_storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "status",
            "user",
            "user_group",
            "is_multi_tenant",
            "labels",
        ]


class BaremetalGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = [
            "name",
            "description",
            "total_cpu_cores",
            "total_memory_mib",
            "total_storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "status",
            "user",
            "user_group",
            "is_multi_tenant",
            "labels",
        ]


# BaremetalModel Serializers
class BaremetalModelSerializer(serializers.ModelSerializer):
    gpus = serializers.SerializerMethodField()
    gpu_specifications = serializers.SerializerMethodField()

    class Meta:
        model = models.BaremetalModel
        fields = [
            "id",
            "name",
            "description",
            "model_name",
            "short_model_name",
            "manufacturer",
            "cpu_model",
            "cpu_count",
            "disks",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "unit_size",
            "type",
            "gpus",
            "gpu_specifications",
            "created_at",
            "updated_at",
        ]

    def get_gpus(self, obj):
        return [{"id": str(gpu.id), "name": gpu.name} for gpu in obj.gpus.all()]

    def get_gpu_specifications(self, obj):
        return [
            {
                "id": str(bmg.id),
                "physical_gpu_model": bmg.physical_gpu_model.name,
                "count": bmg.count,
            }
            for bmg in obj.gpu_specifications.all()
        ]


class BaremetalModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModel
        fields = [
            "id",
            "name",
            "description",
            "model_name",
            "short_model_name",
            "manufacturer",
            "cpu_model",
            "cpu_count",
            "disks",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "unit_size",
            "type",
        ]


class BaremetalModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModel
        fields = [
            "name",
            "description",
            "model_name",
            "short_model_name",
            "manufacturer",
            "cpu_model",
            "cpu_count",
            "disks",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "unit_size",
            "type",
        ]


# Baremetal Serializers
class BaremetalSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    baremetal_group = BaremetalGroupSerializer(read_only=True)
    model = BaremetalModelSerializer(read_only=True)
    purchase_requisition = PurchaseRequisitionSerializer(read_only=True)
    purchase_order = PurchaseOrderSerializer(read_only=True)
    user = CustomUserSerializer(many=True, read_only=True)
    user_group = serializers.SerializerMethodField()

    class Meta:
        model = models.Baremetal
        fields = [
            "id",
            "name",
            "serial_number",
            "model",
            "unit",
            "status",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "baremetal_group",
            "purchase_requisition",
            "purchase_order",
            "user",
            "user_group",
            "external_system_id",
            "max_virtual_machine",
            "max_utilization",
            "labels",
            "failure_zone",
            "created_at",
            "updated_at",
        ]

    def get_user_group(self, obj):
        return [{"id": str(ug.id), "name": ug.name} for ug in obj.user_group.all()]


class BaremetalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = [
            "id",
            "name",
            "serial_number",
            "model",
            "unit",
            "status",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "baremetal_group",
            "purchase_requisition",
            "purchase_order",
            "user",
            "user_group",
            "external_system_id",
            "max_virtual_machine",
            "max_utilization",
            "labels",
            "failure_zone",
        ]


class BaremetalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = [
            "name",
            "serial_number",
            "model",
            "unit",
            "status",
            "cpu_cores",
            "memory_mib",
            "storage_gb",
            "available_cpu_cores",
            "available_memory_mib",
            "available_storage_gb",
            "baremetal_group",
            "purchase_requisition",
            "purchase_order",
            "user",
            "user_group",
            "external_system_id",
            "max_virtual_machine",
            "max_utilization",
            "labels",
            "failure_zone",
        ]


# BaremetalGroupTenantQuota Serializers
class BaremetalGroupTenantQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "id",
            "baremetal_group",
            "tenant",
            "cpu_quota",
            "memory_quota",
            "storage_quota",
            "created_at",
            "updated_at",
        ]


class BaremetalGroupTenantQuotaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "id",
            "baremetal_group",
            "tenant",
            "cpu_quota",
            "memory_quota",
            "storage_quota",
        ]


class BaremetalGroupTenantQuotaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = [
            "baremetal_group",
            "tenant",
            "cpu_quota",
            "memory_quota",
            "storage_quota",
        ]


# BaremetalModelGPU Serializers (PhysicalGPUModel needed here)
class PhysicalGPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhysicalGPUModel
        fields = [
            "id",
            "name",
            "description",
            "vendor",
            "architecture",
            "memory_mib",
            "api_support",
            "power_consumption",
            "release_date",
            "end_of_life",
            "is_multi_instance_supported",
            "created_at",
            "updated_at",
        ]


class PhysicalGPUModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhysicalGPUModel
        fields = [
            "id",
            "name",
            "description",
            "vendor",
            "architecture",
            "memory_mib",
            "api_support",
            "power_consumption",
            "release_date",
            "end_of_life",
            "is_multi_instance_supported",
        ]


class PhysicalGPUModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhysicalGPUModel
        fields = [
            "name",
            "description",
            "vendor",
            "architecture",
            "memory_mib",
            "api_support",
            "power_consumption",
            "release_date",
            "end_of_life",
            "is_multi_instance_supported",
        ]


class BaremetalModelGPUSerializer(serializers.ModelSerializer):
    baremetal_model = serializers.SerializerMethodField()
    physical_gpu_model = PhysicalGPUModelSerializer(read_only=True)

    class Meta:
        model = models.BaremetalModelGPU
        fields = [
            "id",
            "baremetal_model",
            "physical_gpu_model",
            "count",
            "created_at",
            "updated_at",
        ]

    def get_baremetal_model(self, obj):
        return {"id": str(obj.baremetal_model.id), "name": obj.baremetal_model.name}


class BaremetalModelGPUCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModelGPU
        fields = ["id", "baremetal_model", "physical_gpu_model", "count"]


class BaremetalModelGPUUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalModelGPU
        fields = ["baremetal_model", "physical_gpu_model", "count"]


# GPUAllocation Serializers (GPUProfile needed here)
class GPUProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUProfile
        fields = ["id", "name", "memory_mib", "cores", "created_at", "updated_at"]


class GPUProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUProfile
        fields = ["id", "name", "memory_mib", "cores"]


class GPUProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUProfile
        fields = ["name", "memory_mib", "cores"]


class GPUAllocationSerializer(serializers.ModelSerializer):
    physical_gpu = serializers.SerializerMethodField()
    virtual_machine = serializers.SerializerMethodField()
    profile = GPUProfileSerializer(read_only=True)

    class Meta:
        model = models.GPUAllocation
        fields = [
            "id",
            "physical_gpu",
            "virtual_machine",
            "allocated_memory_mib",
            "allocated_cores",
            "profile",
            "created_at",
            "updated_at",
        ]

    def get_virtual_machine(self, obj):
        return {"id": str(obj.virtual_machine.id), "name": obj.virtual_machine.name}

    def get_physical_gpu(self, obj):
        return {"id": str(obj.physical_gpu.id), "name": obj.physical_gpu.name}


class GPUAllocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUAllocation
        fields = [
            "id",
            "physical_gpu",
            "virtual_machine",
            "allocated_memory_mib",
            "allocated_cores",
            "profile",
        ]


class GPUAllocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GPUAllocation
        fields = [
            "physical_gpu",
            "virtual_machine",
            "allocated_memory_mib",
            "allocated_cores",
            "profile",
        ]


# ------------------------------------------------------------------------------
# Common ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# Region Serializers
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ["id", "name", "description", "status", "created_at", "updated_at"]


class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ["id", "name", "description", "status"]


class RegionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ["name", "description", "status"]


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
        fields = ["name", "description", "status"]


# Vendor Serializers
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ["id", "name", "created_at", "updated_at"]


class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ["id", "name", "contact_email", "contact_phone", "address"]


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ["name", "contact_email", "contact_phone", "address"]

# TODO: 為什麼需要這個 serializer？
class VendorBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ["id", "name"]


# ------------------------------------------------------------------------------
# GPU ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# PhysicalGPU Serializers
class PhysicalGPUSerializer(serializers.ModelSerializer):
    physical_gpu_model = PhysicalGPUModelSerializer(read_only=True)
    baremetal = serializers.SerializerMethodField()

    class Meta:
        model = models.PhysicalGPU
        fields = [
            "id",
            "name",
            "serial_number",
            "physical_gpu_model",
            "description",
            "baremetal",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_baremetal(self, obj):
        if obj.baremetal:
            return {"id": str(obj.baremetal.id), "name": obj.baremetal.name}
        return None


class PhysicalGPUCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhysicalGPU
        fields = [
            "id",
            "name",
            "serial_number",
            "physical_gpu_model",
            "description",
            "baremetal",
            "status",
        ]


class PhysicalGPUUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhysicalGPU
        fields = [
            "name",
            "serial_number",
            "physical_gpu_model",
            "description",
            "baremetal",
            "status",
        ]


# ------------------------------------------------------------------------------
# Infrastructure ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# AvailableGroup Serializers
class AvailableGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailableGroup
        fields = ["id", "name", "description", "status", "created_at", "updated_at"]


class AvailableGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailableGroup
        fields = ["id", "name", "description", "status"]


class AvailableGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailableGroup
        fields = ["name", "description", "status"]


# Fab Serializers
class FabSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["id", "name", "external_system_id", "created_at", "updated_at"]


class FabCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["id", "name", "external_system_id"]


class FabUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fab
        fields = ["name", "external_system_id"]


# Phase Serializers
class PhaseSerializer(serializers.ModelSerializer):
    fab = FabSerializer(read_only=True)

    class Meta:
        model = models.Phase
        fields = ["id", "name", "external_system_id", "fab", "created_at", "updated_at"]


class PhaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phase
        fields = ["id", "name", "external_system_id", "fab"]


class PhaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phase
        fields = ["name", "external_system_id", "fab"]


# DataCenter Serializers
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
        fields = ["name", "external_system_id", "phase"]


# Room Serializers
class RoomSerializer(serializers.ModelSerializer):
    datacenter = DataCenterSerializer(read_only=True)

    class Meta:
        model = models.Room
        fields = ["id", "name", "external_system_id", "datacenter", "created_at", "updated_at"]


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["id", "name", "external_system_id", "datacenter"]


class RoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["name", "external_system_id", "datacenter"]



# Rack Serializers
class RackSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    available_group = AvailableGroupSerializer(read_only=True)

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
            "status",
            "available_group",
            "created_at",
            "updated_at",
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
            "status",
            "available_group",
        ]


class RackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        fields = [
            "name",
            "external_system_id",
            "room",
            "bgp_number",
            "as_number",
            "height_units",
            "used_units",
            "available_units",
            "status",
            "available_group",
        ]



# ------------------------------------------------------------------------------
# Network ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# VLAN Serializers
class VLANSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VLAN
        fields = ["id", "vlan_id", "name", "description", "created_at", "updated_at"]


class VLANCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VLAN
        fields = ["id", "vlan_id", "name", "description"]


class VLANUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VLAN
        fields = ["vlan_id", "name", "description"]


# VRF Serializers
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


class VRFCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VRF
        fields = [
            "id",
            "name",
            "route_distinguisher",
        ]


class VRFUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VRF
        fields = [
            "name",
            "route_distinguisher",
        ]


# BGPConfig Serializers
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


class BGPConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGPConfig
        fields = [
            "id",
            "asn",
            "peer_ip",
            "local_ip",
            "password",
        ]


class BGPConfigUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGPConfig
        fields = [
            "asn",
            "peer_ip",
            "local_ip",
            "password",
        ]


# NetworkInterface Serializers
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


class NetworkInterfaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NetworkInterface
        fields = [
            "id",
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
        ]


class NetworkInterfaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NetworkInterface
        fields = [
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
        ]


# ------------------------------------------------------------------------------
# Scheduling ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# SchedulingStrategy Serializers
class SchedulingStrategySerializer(serializers.ModelSerializer):
    tenant = serializers.SerializerMethodField()
    available_group = AvailableGroupSerializer(many=True, read_only=True)
    baremetal_group_tenant_quota = serializers.SerializerMethodField()

    class Meta:
        model = models.SchedulingStrategy
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "tenant",
            "status",
            "available_group",
            "baremetal_group_tenant_quota",
            "created_at",
            "updated_at",
        ]

    def get_tenant(self, obj):
        if obj.tenant:
            return {"id": str(obj.tenant.id), "name": obj.tenant.name, "status": obj.tenant.status}
        return None

    def get_baremetal_group_tenant_quota(self, obj):
        if obj.baremetal_group_tenant_quota:
            return {
                "id": str(obj.baremetal_group_tenant_quota.id),
                "baremetal_group": obj.baremetal_group_tenant_quota.baremetal_group.name,
                "tenant": obj.baremetal_group_tenant_quota.tenant.name,
            }
        return None


class SchedulingStrategyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingStrategy
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "tenant",
            "status",
            "available_group",
            "baremetal_group_tenant_quota",
        ]


class SchedulingStrategyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingStrategy
        fields = [
            "name",
            "description",
            "priority",
            "tenant",
            "status",
            "available_group",
            "baremetal_group_tenant_quota",
        ]


# SchedulingStrategyModel Serializers
class SchedulingStrategyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingStrategyModel
        fields = [
            "id",
            "name",
            "description",
            "mode",
            "priority",
            "dc_failure_zone_affinity",
            "phase_failure_zone_affinity",
            "room_failure_zone_affinity",
            "rack_failure_zone_affinity",
            "ttl_seconds",
            "created_at",
            "updated_at",
        ]


class SchedulingStrategyModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingStrategyModel
        fields = [
            "id",
            "name",
            "description",
            "mode",
            "priority",
            "dc_failure_zone_affinity",
            "phase_failure_zone_affinity",
            "room_failure_zone_affinity",
            "rack_failure_zone_affinity",
            "ttl_seconds",
        ]


class SchedulingStrategyModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchedulingStrategyModel
        fields = [
            "name",
            "description",
            "mode",
            "priority",
            "dc_failure_zone_affinity",
            "phase_failure_zone_affinity",
            "room_failure_zone_affinity",
            "rack_failure_zone_affinity",
            "ttl_seconds",
        ]


# ------------------------------------------------------------------------------
# Users ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# CustomGroup Serializers
class CustomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomGroup
        fields = ["id", "name", "description", "status"]


class CustomGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomGroup
        fields = ["id", "name", "description", "status"]


class CustomGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomGroup
        fields = ["name", "description", "status"]


# ------------------------------------------------------------------------------
# Virtual ViewSets (ordered per views.py)
# ------------------------------------------------------------------------------


# BastionClusterAssociation Serializers
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
        fields = ["bastion", "k8s_cluster"]


# ClusterTemplate Serializers
class ClusterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterTemplate
        fields = [
            "id",
            "name",
            "description",
            "routable_ratio",
            "created_at",
            "updated_at",
        ]


class ClusterTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterTemplate
        fields = ["id", "name", "description", "routable_ratio", "user", "user_group"]


class ClusterTemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterTemplate
        fields = ["name", "description", "routable_ratio", "user", "user_group"]


# ClusterTemplateVirtualMachine Serializers
class ClusterTemplateVirtualMachineSerializer(serializers.ModelSerializer):
    cluster_template = serializers.SerializerMethodField()
    vm_role = serializers.SerializerMethodField()
    vm_spec = serializers.SerializerMethodField()

    class Meta:
        model = models.ClusterTemplateVirtualMachine
        fields = [
            "id",
            "cluster_template",
            "vm_role",
            "vm_spec",
            "is_routable",
            "count",
            "created_at",
            "updated_at",
        ]

    def get_cluster_template(self, obj):
        return {"id": str(obj.cluster_template.id), "name": obj.cluster_template.name}

    def get_vm_role(self, obj):
        return {"id": str(obj.vm_role.id), "name": obj.vm_role.name}

    def get_vm_spec(self, obj):
        return {"id": str(obj.vm_spec.id), "name": obj.vm_spec.name}


class ClusterTemplateVirtualMachineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterTemplateVirtualMachine
        fields = ["id", "cluster_template", "vm_role", "vm_spec", "is_routable", "count"]


class ClusterTemplateVirtualMachineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterTemplateVirtualMachine
        fields = ["cluster_template", "vm_role", "vm_spec", "is_routable", "count"]


# K8sCluster Serializers
class K8sClusterSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    scheduling_strategy = SchedulingStrategySerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    failure_zone_cluster = serializers.SerializerMethodField()

    class Meta:
        model = models.K8sCluster
        fields = [
            "id",
            "name",
            "version",
            "tenant",
            "region",
            "scheduling_strategy",
            "description",
            "user",
            "failure_zone_cluster",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_failure_zone_cluster(self, obj):
        if obj.failure_zone_cluster:
            return {"id": str(obj.failure_zone_cluster.id), "name": obj.failure_zone_cluster.name}
        return None


class K8sClusterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = [
            "id",
            "name",
            "version",
            "tenant",
            "region",
            "scheduling_strategy",
            "description",
            "user",
            "failure_zone_cluster",
            "status",
        ]


class K8sClusterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = [
            "name",
            "version",
            "tenant",
            "region",
            "scheduling_strategy",
            "description",
            "user",
            "failure_zone_cluster",
            "status",
        ]


# K8sClusterPlugin Serializers
class K8sClusterPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = [
            "id",
            "k8s_clusters",
            "name",
            "status",
            "additional_info",
            "created_at",
            "updated_at",
        ]


class K8sClusterPluginCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ["id", "name", "status", "additional_info", "k8s_clusters"]


class K8sClusterPluginUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ["name", "status", "additional_info", "k8s_clusters"]


# K8sClusterPluginAssociation Serializers
class K8sClusterPluginAssociationSerializer(serializers.ModelSerializer):
    k8s_cluster = serializers.SerializerMethodField()
    k8s_cluster_plugin = serializers.SerializerMethodField()

    class Meta:
        model = models.K8sClusterPluginAssociation
        fields = [
            "id",
            "k8s_cluster",
            "k8s_cluster_plugin",
            "version",
            "created_at",
            "updated_at",
        ]

    def get_k8s_cluster(self, obj):
        return {"id": str(obj.k8s_cluster.id), "name": obj.k8s_cluster.name}

    def get_k8s_cluster_plugin(self, obj):
        return {"id": str(obj.k8s_cluster_plugin.id), "name": obj.k8s_cluster_plugin.name}


class K8sClusterPluginAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPluginAssociation
        fields = ["id", "k8s_cluster", "k8s_cluster_plugin", "version"]


class K8sClusterPluginAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPluginAssociation
        fields = ["k8s_cluster", "k8s_cluster_plugin", "version"]


# K8sClusterToServiceMesh Serializers
class K8sClusterToServiceMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = [
            "id",
            "k8s_cluster",
            "service_mesh",
            "role",
            "created_at",
            "updated_at",
        ]


class K8sClusterToServiceMeshCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ["id", "k8s_cluster", "service_mesh", "role"]


class K8sClusterToServiceMeshUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ["k8s_cluster", "service_mesh", "role"]


# ServiceMesh Serializers
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
        fields = ["name", "type", "description", "status"]


# VirtualMachineSpecification Serializers
class VirtualMachineSpecificationSerializer(serializers.ModelSerializer):
    required_gpu = PhysicalGPUModelSerializer(many=True, read_only=True)

    class Meta:
        model = models.VirtualMachineSpecification
        fields = [
            "id",
            "name",
            "generation",
            "required_cpu_cores",
            "required_memory_mib",
            "required_storage_gb",
            "required_gpu",
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
            "required_cpu_cores",
            "required_memory_mib",
            "required_storage_gb",
            "required_gpu",
        ]


class VirtualMachineSpecificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = [
            "name",
            "generation",
            "required_cpu_cores",
            "required_memory_mib",
            "required_storage_gb",
            "required_gpu",
        ]


# VirtualMachine Serializers
class VirtualMachineSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    baremetal = BaremetalSerializer(read_only=True)
    specification = VirtualMachineSpecificationSerializer(read_only=True)
    k8s_cluster = K8sClusterSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    user_group = serializers.SerializerMethodField()

    class Meta:
        model = models.VirtualMachine
        fields = [
            "id",
            "name",
            "tenant",
            "region",
            "baremetal",
            "specification",
            "k8s_cluster",
            "virtual_machine_role",
            "routable",
            "baremetal_selector",
            "user",
            "user_group",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_user_group(self, obj):
        return [{"id": str(ug.id), "name": ug.name} for ug in obj.user_group.all()]


class VirtualMachineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = [
            "id",
            "name",
            "tenant",
            "region",
            "baremetal",
            "specification",
            "k8s_cluster",
            "virtual_machine_role",
            "routable",
            "baremetal_selector",
            "user",
            "user_group",
            "status",
        ]


class VirtualMachineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = [
            "name",
            "tenant",
            "region",
            "baremetal",
            "specification",
            "k8s_cluster",
            "virtual_machine_role",
            "routable",
            "baremetal_selector",
            "user",
            "user_group",
            "status",
        ]


# VirtualMachineRole Serializers
class VirtualMachineRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineRole
        fields = ["id", "name", "description", "created_at", "updated_at"]


class VirtualMachineRoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineRole
        fields = ["id", "name", "description"]


class VirtualMachineRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineRole
        fields = ["name", "description"]


# VirtualMachineSpecificationRequiredGPU Serializers
class VirtualMachineSpecificationRequiredGPUSerializer(serializers.ModelSerializer):
    virtual_machine_specification = serializers.SerializerMethodField()
    physical_gpu_model = PhysicalGPUModelSerializer(read_only=True)

    class Meta:
        model = models.VirtualMachineSpecificationRequiredGPU
        fields = [
            "id",
            "virtual_machine_specification",
            "physical_gpu_model",
            "count",
            "created_at",
            "updated_at",
        ]

    def get_virtual_machine_specification(self, obj):
        return {
            "id": str(obj.virtual_machine_specification.id),
            "name": obj.virtual_machine_specification.name,
        }


class VirtualMachineSpecificationRequiredGPUCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecificationRequiredGPU
        fields = ["id", "virtual_machine_specification", "physical_gpu_model", "count"]


class VirtualMachineSpecificationRequiredGPUUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecificationRequiredGPU
        fields = ["virtual_machine_specification", "physical_gpu_model", "count"]


# ------------------------------------------------------------------------------
# Permission Serializers
# ------------------------------------------------------------------------------
class ObjectPermissionSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    object_id = serializers.CharField()
    user_id = serializers.CharField(required=False)
    group_id = serializers.CharField(required=False)
    permission = serializers.CharField()

# TODO: 為什麼需要這個 serializer？
# Django Group Serializers (using built-in Group model)
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
