from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .. import models
from . import serializers
from ..authentication import CustomTokenAuthentication, TokenPermission
from rest_framework.authentication import TokenAuthentication
class BaseViewSet(viewsets.ModelViewSet):
    # authentication_classes = [CustomTokenAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [TokenPermission]

# Maintainer ViewSet
class MaintainerViewSet(BaseViewSet):
    queryset = models.Maintainer.objects.all()
    serializer_class = serializers.MaintainerSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaintainerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.MaintainerUpdateSerializer
        return serializers.MaintainerSerializer

# Maintainer Group ViewSet
class MaintainerGroupViewSet(BaseViewSet):
    queryset = models.MaintainerGroup.objects.all()
    serializer_class = serializers.MaintainerGroupSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaintainerGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.MaintainerGroupUpdateSerializer
        return serializers.MaintainerGroupSerializer

# Maintainer Group Member ViewSet
class MaintainerToMaintainerGroupViewSet(BaseViewSet):
    queryset = models.MaintainerToMaintainerGroup.objects.all()
    serializer_class = serializers.MaintainerToMaintainerGroupSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaintainerToMaintainerGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.MaintainerToMaintainerGroupUpdateSerializer
        return serializers.MaintainerToMaintainerGroupSerializer

# Resource Maintainer ViewSet
class ResourceMaintainerViewSet(BaseViewSet):
    queryset = models.ResourceMaintainer.objects.all()
    serializer_class = serializers.ResourceMaintainerSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ResourceMaintainerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.ResourceMaintainerUpdateSerializer
        return serializers.ResourceMaintainerSerializer

# Rack ViewSet
class RackViewSet(BaseViewSet):
    queryset = models.Rack.objects.all()
    serializer_class = serializers.RackSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.RackCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.RackUpdateSerializer
        return serializers.RackSerializer

# Baremetal Group ViewSet
class BaremetalGroupViewSet(BaseViewSet):
    queryset = models.BaremetalGroup.objects.all()
    serializer_class = serializers.BaremetalGroupSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupUpdateSerializer
        return serializers.BaremetalGroupSerializer

# Baremetal ViewSet
class BaremetalViewSet(BaseViewSet):
    queryset = models.Baremetal.objects.all()
    serializer_class = serializers.BaremetalSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalUpdateSerializer
        return serializers.BaremetalSerializer

# Baremetal Group Tenant Quota ViewSet
class BaremetalGroupTenantQuotaViewSet(BaseViewSet):
    queryset = models.BaremetalGroupTenantQuota.objects.all()
    serializer_class = serializers.BaremetalGroupTenantQuotaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalGroupTenantQuotaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupTenantQuotaUpdateSerializer
        return serializers.BaremetalGroupTenantQuotaSerializer

# Tenant ViewSet
class TenantViewSet(BaseViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.TenantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.TenantUpdateSerializer
        return serializers.TenantSerializer

# Virtual Machine Specification ViewSet
class VirtualMachineSpecificationViewSet(BaseViewSet):
    queryset = models.VirtualMachineSpecification.objects.all()
    serializer_class = serializers.VirtualMachineSpecificationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.VirtualMachineSpecificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineSpecificationUpdateSerializer
        return serializers.VirtualMachineSpecificationSerializer

# K8s Cluster ViewSet
class K8sClusterViewSet(BaseViewSet):
    queryset = models.K8sCluster.objects.all()
    serializer_class = serializers.K8sClusterSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterUpdateSerializer
        return serializers.K8sClusterSerializer

# K8s Cluster Plugin ViewSet
class K8sClusterPluginViewSet(BaseViewSet):
    queryset = models.K8sClusterPlugin.objects.all()
    serializer_class = serializers.K8sClusterPluginSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterPluginCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterPluginUpdateSerializer
        return serializers.K8sClusterPluginSerializer

# Bastion Cluster Association ViewSet
class BastionClusterAssociationViewSet(BaseViewSet):
    queryset = models.BastionClusterAssociation.objects.all()
    serializer_class = serializers.BastionClusterAssociationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BastionClusterAssociationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BastionClusterAssociationUpdateSerializer
        return serializers.BastionClusterAssociationSerializer

# K8s Cluster To Service Mesh ViewSet
class K8sClusterToServiceMeshViewSet(BaseViewSet):
    queryset = models.K8sClusterToServiceMesh.objects.all()
    serializer_class = serializers.K8sClusterToServiceMeshSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterToServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterToServiceMeshUpdateSerializer
        return serializers.K8sClusterToServiceMeshSerializer

# Service Mesh ViewSet
class ServiceMeshViewSet(BaseViewSet):
    queryset = models.ServiceMesh.objects.all()
    serializer_class = serializers.ServiceMeshSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.ServiceMeshUpdateSerializer
        return serializers.ServiceMeshSerializer

# Virtual Machine ViewSet
class VirtualMachineViewSet(BaseViewSet):
    queryset = models.VirtualMachine.objects.all()
    serializer_class = serializers.VirtualMachineSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.VirtualMachineCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineUpdateSerializer
        return serializers.VirtualMachineSerializer 