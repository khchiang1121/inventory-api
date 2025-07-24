from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .. import models
from . import serializers
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from typing import Type
from rest_framework.serializers import BaseSerializer

# ------------------------------------------------------------------------------
# User ViewSets
# ------------------------------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

# ------------------------------------------------------------------------------
# Infrastructure ViewSets
# ------------------------------------------------------------------------------
class FabricationViewSet(viewsets.ModelViewSet):
    queryset = models.Fabrication.objects.all().order_by('id')
    serializer_class = serializers.FabricationSerializer

class PhaseViewSet(viewsets.ModelViewSet):
    queryset = models.Phase.objects.all().order_by('id')
    serializer_class = serializers.PhaseSerializer

class DataCenterViewSet(viewsets.ModelViewSet):
    queryset = models.DataCenter.objects.all().order_by('id')
    serializer_class = serializers.DataCenterSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all().order_by('id')
    serializer_class = serializers.RoomSerializer

# ------------------------------------------------------------------------------
# Network ViewSets
# ------------------------------------------------------------------------------
class VLANViewSet(viewsets.ModelViewSet):
    queryset = models.VLAN.objects.all().order_by('id')
    serializer_class = serializers.VLANSerializer

class VRFViewSet(viewsets.ModelViewSet):
    queryset = models.VRF.objects.all().order_by('id')
    serializer_class = serializers.VRFSerializer

class BGPConfigViewSet(viewsets.ModelViewSet):
    queryset = models.BGPConfig.objects.all().order_by('id')
    serializer_class = serializers.BGPConfigSerializer

class NetworkInterfaceViewSet(viewsets.ModelViewSet):
    queryset = models.NetworkInterface.objects.all().order_by('id')
    serializer_class = serializers.NetworkInterfaceSerializer

# ------------------------------------------------------------------------------
# Purchase ViewSets
# ------------------------------------------------------------------------------
class PurchaseRequisitionViewSet(viewsets.ModelViewSet):
    queryset = models.PurchaseRequisition.objects.all().order_by('id')
    serializer_class = serializers.PurchaseRequisitionSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = models.PurchaseOrder.objects.all().order_by('id')
    serializer_class = serializers.PurchaseOrderSerializer

# ------------------------------------------------------------------------------
# Baremetal ViewSets
# ------------------------------------------------------------------------------
class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all().order_by('id')
    serializer_class = serializers.BrandSerializer

class BaremetalModelViewSet(viewsets.ModelViewSet):
    queryset = models.BaremetalModel.objects.all().order_by('id')
    serializer_class = serializers.BaremetalModelSerializer

# ------------------------------------------------------------------------------
# Physical Infrastructure ViewSets
# ------------------------------------------------------------------------------
class RackViewSet(viewsets.ModelViewSet):
    queryset = models.Rack.objects.all().order_by('id')
    serializer_class = serializers.RackSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        # return serializers.RackSerializer

        if self.action == 'create':
            return serializers.RackCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.RackUpdateSerializer
        return serializers.RackSerializer

# Baremetal Group ViewSet
class BaremetalGroupViewSet(viewsets.ModelViewSet):
    queryset = models.BaremetalGroup.objects.all().order_by('id')
    serializer_class = serializers.BaremetalGroupSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.BaremetalGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupUpdateSerializer
        return serializers.BaremetalGroupSerializer

# Baremetal ViewSet
class BaremetalViewSet(viewsets.ModelViewSet):
    queryset = models.Baremetal.objects.all().order_by('id')
    serializer_class = serializers.BaremetalSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.BaremetalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalUpdateSerializer
        return serializers.BaremetalSerializer

# Baremetal Group Tenant Quota ViewSet
class BaremetalGroupTenantQuotaViewSet(viewsets.ModelViewSet):
    queryset = models.BaremetalGroupTenantQuota.objects.all().order_by('id')
    serializer_class = serializers.BaremetalGroupTenantQuotaSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.BaremetalGroupTenantQuotaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupTenantQuotaUpdateSerializer
        return serializers.BaremetalGroupTenantQuotaSerializer

# Tenant ViewSet
class TenantViewSet(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all().order_by('id')
    serializer_class = serializers.TenantSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.TenantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.TenantUpdateSerializer
        return serializers.TenantSerializer

# Virtual Machine Specification ViewSet
class VirtualMachineSpecificationViewSet(viewsets.ModelViewSet):
    queryset = models.VirtualMachineSpecification.objects.all().order_by('id')
    serializer_class = serializers.VirtualMachineSpecificationSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.VirtualMachineSpecificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineSpecificationUpdateSerializer
        return serializers.VirtualMachineSpecificationSerializer

# K8s Cluster ViewSet
class K8sClusterViewSet(viewsets.ModelViewSet):
    queryset = models.K8sCluster.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.K8sClusterCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterUpdateSerializer
        return serializers.K8sClusterSerializer

# K8s Cluster Plugin ViewSet
class K8sClusterPluginViewSet(viewsets.ModelViewSet):
    queryset = models.K8sClusterPlugin.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterPluginSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.K8sClusterPluginCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterPluginUpdateSerializer
        return serializers.K8sClusterPluginSerializer

# Bastion Cluster Association ViewSet
class BastionClusterAssociationViewSet(viewsets.ModelViewSet):
    queryset = models.BastionClusterAssociation.objects.all().order_by('id')
    serializer_class = serializers.BastionClusterAssociationSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.BastionClusterAssociationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BastionClusterAssociationUpdateSerializer
        return serializers.BastionClusterAssociationSerializer

# K8s Cluster To Service Mesh ViewSet
class K8sClusterToServiceMeshViewSet(viewsets.ModelViewSet):
    queryset = models.K8sClusterToServiceMesh.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterToServiceMeshSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.K8sClusterToServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterToServiceMeshUpdateSerializer
        return serializers.K8sClusterToServiceMeshSerializer

# Service Mesh ViewSet
class ServiceMeshViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceMesh.objects.all().order_by('id')
    serializer_class = serializers.ServiceMeshSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.ServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.ServiceMeshUpdateSerializer
        return serializers.ServiceMeshSerializer

# Virtual Machine ViewSet
class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = models.VirtualMachine.objects.all().order_by('id')
    serializer_class = serializers.VirtualMachineSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.VirtualMachineCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineUpdateSerializer
        return serializers.VirtualMachineSerializer 

# ------------------------------------------------------------------------------
# Ansible ViewSets
# ------------------------------------------------------------------------------
class AnsibleGroupViewSet(viewsets.ModelViewSet):
    queryset = models.AnsibleGroup.objects.all().order_by('name')
    serializer_class = serializers.AnsibleGroupSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.AnsibleGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.AnsibleGroupUpdateSerializer
        return serializers.AnsibleGroupSerializer
    
    @action(detail=True, methods=['get'])
    def variables(self, request, pk=None):
        """Get all variables for a group including inherited ones"""
        group = self.get_object()
        return Response(group.all_variables)
    
    @action(detail=True, methods=['get'])
    def hosts(self, request, pk=None):
        """Get all hosts in a group including child groups"""
        group = self.get_object()
        hosts = group.all_hosts
        return Response([{'id': str(host.id), 'name': getattr(host, 'name', str(host)), 'type': host._meta.model_name} for host in hosts])

class AnsibleGroupVariableViewSet(viewsets.ModelViewSet):
    queryset = models.AnsibleGroupVariable.objects.all().order_by('group__name', 'key')
    serializer_class = serializers.AnsibleGroupVariableSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.AnsibleGroupVariableCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.AnsibleGroupVariableUpdateSerializer
        return serializers.AnsibleGroupVariableSerializer

class AnsibleGroupRelationshipViewSet(viewsets.ModelViewSet):
    queryset = models.AnsibleGroupRelationship.objects.all().order_by('parent_group__name', 'child_group__name')
    serializer_class = serializers.AnsibleGroupRelationshipSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.AnsibleGroupRelationshipCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.AnsibleGroupRelationshipUpdateSerializer
        return serializers.AnsibleGroupRelationshipSerializer

class AnsibleHostViewSet(viewsets.ModelViewSet):
    queryset = models.AnsibleHost.objects.all().order_by('group__name')
    serializer_class = serializers.AnsibleHostSerializer
    
    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == 'create':
            return serializers.AnsibleHostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.AnsibleHostUpdateSerializer
        return serializers.AnsibleHostSerializer 