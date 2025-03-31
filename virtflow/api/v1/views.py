from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .. import models
from . import serializers
from rest_framework import viewsets
from .serializers import CustomUserSerializer

# ------------------------------------------------------------------------------
# User ViewSets
# ------------------------------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

# ------------------------------------------------------------------------------
# Physical Infrastructure ViewSets
# ------------------------------------------------------------------------------
class RackViewSet(viewsets.ModelViewSet):
    queryset = models.Rack.objects.all().order_by('id')
    serializer_class = serializers.RackSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.RackCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.RackUpdateSerializer
        return serializers.RackSerializer

# Baremetal Group ViewSet
class BaremetalGroupViewSet(viewsets.ModelViewSet):
    queryset = models.BaremetalGroup.objects.all().order_by('id')
    serializer_class = serializers.BaremetalGroupSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalGroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupUpdateSerializer
        return serializers.BaremetalGroupSerializer

# Baremetal ViewSet
class BaremetalViewSet(viewsets.ModelViewSet):
    queryset = models.Baremetal.objects.all().order_by('id')
    serializer_class = serializers.BaremetalSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalUpdateSerializer
        return serializers.BaremetalSerializer

# Baremetal Group Tenant Quota ViewSet
class BaremetalGroupTenantQuotaViewSet(viewsets.ModelViewSet):
    queryset = models.BaremetalGroupTenantQuota.objects.all().order_by('id')
    serializer_class = serializers.BaremetalGroupTenantQuotaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BaremetalGroupTenantQuotaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BaremetalGroupTenantQuotaUpdateSerializer
        return serializers.BaremetalGroupTenantQuotaSerializer

# Tenant ViewSet
class TenantViewSet(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all().order_by('id')
    serializer_class = serializers.TenantSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.TenantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.TenantUpdateSerializer
        return serializers.TenantSerializer

# Virtual Machine Specification ViewSet
class VirtualMachineSpecificationViewSet(viewsets.ModelViewSet):
    queryset = models.VirtualMachineSpecification.objects.all().order_by('id')
    serializer_class = serializers.VirtualMachineSpecificationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.VirtualMachineSpecificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineSpecificationUpdateSerializer
        return serializers.VirtualMachineSpecificationSerializer

# K8s Cluster ViewSet
class K8sClusterViewSet(viewsets.ModelViewSet):
    queryset = models.K8sCluster.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterUpdateSerializer
        return serializers.K8sClusterSerializer

# K8s Cluster Plugin ViewSet
class K8sClusterPluginViewSet(viewsets.ModelViewSet):
    queryset = models.K8sClusterPlugin.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterPluginSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterPluginCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterPluginUpdateSerializer
        return serializers.K8sClusterPluginSerializer

# Bastion Cluster Association ViewSet
class BastionClusterAssociationViewSet(viewsets.ModelViewSet):
    queryset = models.BastionClusterAssociation.objects.all().order_by('id')
    serializer_class = serializers.BastionClusterAssociationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BastionClusterAssociationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.BastionClusterAssociationUpdateSerializer
        return serializers.BastionClusterAssociationSerializer

# K8s Cluster To Service Mesh ViewSet
class K8sClusterToServiceMeshViewSet(viewsets.ModelViewSet):
    queryset = models.K8sClusterToServiceMesh.objects.all().order_by('id')
    serializer_class = serializers.K8sClusterToServiceMeshSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.K8sClusterToServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.K8sClusterToServiceMeshUpdateSerializer
        return serializers.K8sClusterToServiceMeshSerializer

# Service Mesh ViewSet
class ServiceMeshViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceMesh.objects.all().order_by('id')
    serializer_class = serializers.ServiceMeshSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ServiceMeshCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.ServiceMeshUpdateSerializer
        return serializers.ServiceMeshSerializer

# Virtual Machine ViewSet
class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = models.VirtualMachine.objects.all().order_by('id')
    serializer_class = serializers.VirtualMachineSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.VirtualMachineCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.VirtualMachineUpdateSerializer
        return serializers.VirtualMachineSerializer 