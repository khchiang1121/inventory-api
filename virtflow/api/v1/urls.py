from django.urls import path, include
from rest_framework.routers import DefaultRouter
from virtflow.api.v1 import views
from .permissions import ObjectPermissionViewSet

app_name = 'v1'

# router = DefaultRouter()
router = DefaultRouter(trailing_slash=False)

router.register(r'users', views.CustomUserViewSet)
router.register(r'racks', views.RackViewSet)
router.register(r'baremetal-groups', views.BaremetalGroupViewSet)
router.register(r'baremetals', views.BaremetalViewSet)
router.register(r'baremetal-group-tenant-quotas', views.BaremetalGroupTenantQuotaViewSet)
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
