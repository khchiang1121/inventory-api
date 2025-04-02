from rest_framework import serializers
from .. import models
from uuid import UUID
from datetime import datetime
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'password', 'email','account', 'status']

# ------------------------------------------------------------------------------
# Infrastructure Serializers
# ------------------------------------------------------------------------------
class FabricationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fabrication
        fields = ['id', 'name', 'old_system_id', 'created_at', 'updated_at']

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phase
        fields = ['id', 'name', 'old_system_id', 'created_at', 'updated_at']

class DataCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataCenter
        fields = ['id', 'name', 'old_system_id', 'created_at', 'updated_at']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['id', 'name', 'old_system_id', 'created_at', 'updated_at']

# ------------------------------------------------------------------------------
# Network Serializers
# ------------------------------------------------------------------------------
class VLANSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VLAN
        fields = ['id', 'vlan_id', 'name', 'created_at', 'updated_at']

class VRFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VRF
        fields = ['id', 'name', 'route_distinguisher', 'created_at', 'updated_at']

class BGPConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGPConfig
        fields = ['id', 'asn', 'peer_ip', 'local_ip', 'password', 'created_at', 'updated_at']

class ResourceRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': str(value.id),
            'type': value._meta.model_name,
            'name': value.name
        }

class NetworkInterfaceSerializer(serializers.ModelSerializer):
    vlan = VLANSerializer(read_only=True)
    vrf = VRFSerializer(read_only=True)
    bgp_config = BGPConfigSerializer(read_only=True)
    resource = ResourceRelatedField(read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), write_only=True)
    object_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = models.NetworkInterface
        fields = ['id', 'resource', 'content_type', 'object_id', 'name', 'mac_address', 
                 'is_primary', 'ipv4_address', 'ipv4_netmask', 'ipv6_address', 'ipv6_netmask', 
                 'gateway', 'dns_servers', 'vlan', 'vrf', 'bgp_config', 'created_at', 'updated_at']

# Rack Serializers
class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        fields = ['id', 'name', 'bgp_number', 'as_number', 'old_system_id', 'created_at', 'updated_at']

class RackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        # fields = ['name', 'bgp_number', 'as_number', 'old_system_id']
        fields = ['id', 'name', 'bgp_number', 'as_number', 'old_system_id', 'created_at', 'updated_at']


class RackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rack
        fields = ['name', 'bgp_number', 'as_number', 'old_system_id']

# Baremetal Group Serializers
class BaremetalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = ['id', 'name', 'description', 'total_cpu', 'total_memory', 'total_storage', 
                 'available_cpu', 'available_memory', 'available_storage', 'status', 
                 'created_at', 'updated_at']

class BaremetalGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = ['name', 'description', 'total_cpu', 'total_memory', 'total_storage', 
                 'available_cpu', 'available_memory', 'available_storage', 'status']

class BaremetalGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroup
        fields = ['name', 'description', 'total_cpu', 'total_memory', 'total_storage', 
                 'available_cpu', 'available_memory', 'available_storage', 'status']

# ------------------------------------------------------------------------------
# Purchase Serializers
# ------------------------------------------------------------------------------
class PurchaseRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseRequisition
        fields = ['id', 'pr_number', 'requested_by', 'department', 'reason', 'submit_date', 'created_at', 'updated_at']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseOrder
        fields = ['id', 'po_number', 'vendor_name', 'payment_terms', 'delivery_date', 'issued_by', 'created_at', 'updated_at']

# ------------------------------------------------------------------------------
# Baremetal Serializers
# ------------------------------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['id', 'name', 'created_at', 'updated_at']

class BaremetalModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    
    class Meta:
        model = models.BaremetalModel
        fields = ['id', 'name', 'brand', 'total_cpu', 'total_memory', 'total_storage', 'created_at', 'updated_at'] 
# Baremetal Serializers
class BaremetalSerializer(serializers.ModelSerializer):
    rack = RackSerializer(read_only=True)
    group = BaremetalGroupSerializer(read_only=True)
    model = BaremetalModelSerializer(read_only=True)
    fabrication = FabricationSerializer(read_only=True)
    phase = PhaseSerializer(read_only=True)
    data_center = DataCenterSerializer(read_only=True)
    pr = PurchaseRequisitionSerializer(read_only=True)
    po = PurchaseOrderSerializer(read_only=True)
    
    class Meta:
        model = models.Baremetal
        fields = ['id', 'name', 'serial_number', 'model', 'fabrication', 'phase', 'data_center', 
                 'room', 'rack', 'unit', 'status', 'available_cpu', 'available_memory', 
                 'available_storage', 'group', 'pr', 'po', 'old_system_id', 'created_at', 'updated_at']

class BaremetalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = ['name', 'serial_number', 'model', 'fabrication', 'phase', 'data_center', 
                 'room', 'rack', 'unit', 'status', 'available_cpu', 'available_memory', 
                 'available_storage', 'group', 'old_system_id']

class BaremetalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Baremetal
        fields = ['name', 'serial_number', 'model', 'fabrication', 'phase', 'data_center', 
                 'room', 'rack', 'unit', 'status', 'available_cpu', 'available_memory', 
                 'available_storage', 'group', 'old_system_id']

# Baremetal Group Tenant Quota Serializers
class BaremetalGroupTenantQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = ['id', 'group', 'tenant', 'cpu_quota_percentage', 'memory_quota', 
                 'storage_quota', 'created_at', 'updated_at']

class BaremetalGroupTenantQuotaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = ['group', 'tenant', 'cpu_quota_percentage', 'memory_quota', 'storage_quota']

class BaremetalGroupTenantQuotaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaremetalGroupTenantQuota
        fields = ['group', 'tenant', 'cpu_quota_percentage', 'memory_quota', 'storage_quota']

# Tenant Serializers
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']

class TenantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ['name', 'description', 'status']

class TenantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ['name', 'description', 'status']

# Virtual Machine Specification Serializers
class VirtualMachineSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = ['id', 'name', 'generation', 'required_cpu', 'required_memory', 
                 'required_storage', 'created_at', 'updated_at']

class VirtualMachineSpecificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = ['name', 'generation', 'required_cpu', 'required_memory', 'required_storage']

class VirtualMachineSpecificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachineSpecification
        fields = ['name', 'generation', 'required_cpu', 'required_memory', 'required_storage']

# K8s Cluster Serializers
class K8sClusterSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    
    class Meta:
        model = models.K8sCluster
        fields = ['id', 'name', 'version', 'tenant', 'scheduling_mode', 'description', 
                 'status', 'created_at', 'updated_at']

class K8sClusterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = ['name', 'version', 'tenant', 'scheduling_mode', 'description', 'status']

class K8sClusterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sCluster
        fields = ['name', 'version', 'tenant', 'scheduling_mode', 'description', 'status']

# K8s Cluster Plugin Serializers
class K8sClusterPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ['id', 'cluster', 'name', 'version', 'status', 'additional_info', 
                 'created_at', 'updated_at']

class K8sClusterPluginCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ['cluster', 'name', 'version', 'status', 'additional_info']

class K8sClusterPluginUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterPlugin
        fields = ['cluster', 'name', 'version', 'status', 'additional_info']

# Bastion Cluster Association Serializers
class BastionClusterAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ['id', 'bastion', 'k8s_cluster', 'created_at', 'updated_at']

class BastionClusterAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ['bastion', 'k8s_cluster']

class BastionClusterAssociationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BastionClusterAssociation
        fields = ['bastion', 'k8s_cluster']

# K8s Cluster To Service Mesh Serializers
class K8sClusterToServiceMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ['id', 'cluster', 'service_mesh', 'role', 'created_at', 'updated_at']

class K8sClusterToServiceMeshCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ['cluster', 'service_mesh', 'role']

class K8sClusterToServiceMeshUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.K8sClusterToServiceMesh
        fields = ['cluster', 'service_mesh', 'role']

# Service Mesh Serializers
class ServiceMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = ['id', 'name', 'type', 'description', 'status', 'created_at', 'updated_at']

class ServiceMeshCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = ['name', 'type', 'description', 'status']

class ServiceMeshUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceMesh
        fields = ['name', 'type', 'description', 'status']

# Virtual Machine Serializers
class VirtualMachineSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    baremetal = BaremetalSerializer(read_only=True)
    specification = VirtualMachineSpecificationSerializer(read_only=True)
    k8s_cluster = K8sClusterSerializer(read_only=True)
    
    class Meta:
        model = models.VirtualMachine
        fields = ['id', 'name', 'tenant', 'baremetal', 'specification', 'k8s_cluster', 
                 'type', 'status', 'created_at', 'updated_at']

class VirtualMachineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = ['name', 'tenant', 'baremetal', 'specification', 'k8s_cluster', 'type', 'status']

class VirtualMachineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VirtualMachine
        fields = ['name', 'tenant', 'baremetal', 'specification', 'k8s_cluster', 'type', 'status']

# ------------------------------------------------------------------------------
# Permission Serializers
# ------------------------------------------------------------------------------
class ObjectPermissionSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    object_id = serializers.CharField()
    user_id = serializers.CharField(required=False)
    group_id = serializers.CharField(required=False)
    permission = serializers.CharField()
