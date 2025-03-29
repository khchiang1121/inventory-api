from django.urls import path, include
from rest_framework.routers import DefaultRouter
from virtflow.api.v1 import views

app_name = 'v1'

router = DefaultRouter()
router.register(r'maintainers', views.MaintainerViewSet)
router.register(r'maintainer-groups', views.MaintainerGroupViewSet)
router.register(r'maintainer-group-members', views.MaintainerToMaintainerGroupViewSet)
router.register(r'resource-maintainers', views.ResourceMaintainerViewSet)
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

urlpatterns = [
    path('', include(router.urls)),
] 