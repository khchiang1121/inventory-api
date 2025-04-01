from django.urls import path, include
from rest_framework.routers import DefaultRouter
from virtflow.api.v1 import views
from .permissions import ObjectPermissionViewSet

app_name = 'v1'

router = DefaultRouter(trailing_slash=False)

# User routes
router.register(r'users', views.CustomUserViewSet)

# Infrastructure routes
router.register(r'fabrications', views.FabricationViewSet)
router.register(r'phases', views.PhaseViewSet)
router.register(r'data-centers', views.DataCenterViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'racks', views.RackViewSet)

# Network routes
router.register(r'vlans', views.VLANViewSet)
router.register(r'vrfs', views.VRFViewSet)
router.register(r'bgp-configs', views.BGPConfigViewSet)
router.register(r'network-interfaces', views.NetworkInterfaceViewSet)

# Purchase routes
router.register(r'purchase-requisitions', views.PurchaseRequisitionViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)

# Baremetal routes
router.register(r'brands', views.BrandViewSet)
router.register(r'baremetal-models', views.BaremetalModelViewSet)
router.register(r'baremetal-groups', views.BaremetalGroupViewSet)
router.register(r'baremetals', views.BaremetalViewSet)
router.register(r'baremetal-group-tenant-quotas', views.BaremetalGroupTenantQuotaViewSet)

# Tenant and VM routes
router.register(r'tenants', views.TenantViewSet)
router.register(r'vm-specifications', views.VirtualMachineSpecificationViewSet)
router.register(r'k8s-clusters', views.K8sClusterViewSet)
router.register(r'k8s-cluster-plugins', views.K8sClusterPluginViewSet)
router.register(r'bastion-cluster-associations', views.BastionClusterAssociationViewSet)
router.register(r'k8s-cluster-service-meshes', views.K8sClusterToServiceMeshViewSet)
router.register(r'service-meshes', views.ServiceMeshViewSet)
router.register(r'virtual-machines', views.VirtualMachineViewSet)
router.register(r'permissions', ObjectPermissionViewSet, basename='object-permissions')

urlpatterns = [
    path('', include(router.urls)),
]
