from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventory_api.api.v1 import views
from .permissions import ObjectPermissionViewSet

app_name = "v1"

router = DefaultRouter(trailing_slash=False)

# ---------------------------------------------------------------------------
# Ansible (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"ansible-groups", views.AnsibleGroupViewSet)
router.register(r"ansible-group-relationships", views.AnsibleGroupRelationshipViewSet)
router.register(r"ansible-group-variables", views.AnsibleGroupVariableViewSet)
router.register(r"ansible-hosts", views.AnsibleHostViewSet)
router.register(r"ansible-host-variables", views.AnsibleHostVariableViewSet)
router.register(r"ansible-inventories", views.AnsibleInventoryViewSet)
router.register(r"ansible-inventory-templates", views.AnsibleInventoryTemplateViewSet)
router.register(
    r"ansible-inventory-variable-set-associations",
    views.AnsibleInventoryVariableSetAssociationViewSet,
)
router.register(r"ansible-variable-sets", views.AnsibleVariableSetViewSet)

# ---------------------------------------------------------------------------
# Baremetal (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"baremetals", views.BaremetalViewSet)
router.register(r"baremetal-groups", views.BaremetalGroupViewSet)
router.register(r"baremetal-group-tenant-quotas", views.BaremetalGroupTenantQuotaViewSet)
router.register(r"baremetal-models", views.BaremetalModelViewSet)
router.register(r"baremetal-model-gpus", views.BaremetalModelGPUViewSet)
router.register(r"gpu-allocations", views.GPUAllocationViewSet)

# ---------------------------------------------------------------------------
# Base (AbstractBase 沒有 API endpoint, 可略過)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Common (shared models)
# ---------------------------------------------------------------------------
router.register(r"regions", views.RegionViewSet)
router.register(r"tenants", views.TenantViewSet)
router.register(r"vendors", views.VendorViewSet)

# ---------------------------------------------------------------------------
# GPU (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"gpu-profiles", views.GPUProfileViewSet)
router.register(r"physical-gpus", views.PhysicalGPUViewSet)
router.register(r"physical-gpu-models", views.PhysicalGPUModelViewSet)

# ---------------------------------------------------------------------------
# Infrastructure (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"available-groups", views.AvailableGroupViewSet)
router.register(r"data-centers", views.DataCenterViewSet)
router.register(r"fabs", views.FabViewSet)
router.register(r"phases", views.PhaseViewSet)
router.register(r"racks", views.RackViewSet)
router.register(r"rooms", views.RoomViewSet)
router.register(r"units", views.UnitViewSet)

# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------
router.register(r"vlans", views.VLANViewSet)
router.register(r"vrfs", views.VRFViewSet)
router.register(r"bgp-configs", views.BGPConfigViewSet)
router.register(r"network-interfaces", views.NetworkInterfaceViewSet)

# ---------------------------------------------------------------------------
# Purchase (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"purchase-orders", views.PurchaseOrderViewSet)
router.register(r"purchase-requisitions", views.PurchaseRequisitionViewSet)

# ---------------------------------------------------------------------------
# Scheduling (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"scheduling-strategies", views.SchedulingStrategyViewSet)
router.register(r"scheduling-strategy-models", views.SchedulingStrategyModelViewSet)

# ---------------------------------------------------------------------------
# Users (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"custom-groups", views.CustomGroupViewSet)
router.register(r"custom-users", views.CustomUserViewSet)

# ---------------------------------------------------------------------------
# Virtual (ordered per __all__)
# ---------------------------------------------------------------------------
router.register(r"bastion-cluster-associations", views.BastionClusterAssociationViewSet)
router.register(r"cluster-templates", views.ClusterTemplateViewSet)
router.register(r"cluster-template-vms", views.ClusterTemplateVirtualMachineViewSet)
router.register(r"k8s-clusters", views.K8sClusterViewSet)
router.register(r"k8s-cluster-plugins", views.K8sClusterPluginViewSet)
router.register(r"k8s-cluster-plugin-associations", views.K8sClusterPluginAssociationViewSet)
router.register(r"k8s-cluster-service-meshes", views.K8sClusterToServiceMeshViewSet)
router.register(r"service-meshes", views.ServiceMeshViewSet)
router.register(r"vms", views.VirtualMachineViewSet)
router.register(r"vm-roles", views.VirtualMachineRoleViewSet)
router.register(r"vm-specifications", views.VirtualMachineSpecificationViewSet)
router.register(
    r"vm-specification-required-gpus", views.VirtualMachineSpecificationRequiredGPUViewSet
)

# ---------------------------------------------------------------------------
# System & Permissions
# ---------------------------------------------------------------------------
router.register(r"system-info", views.SystemInfoViewSet, basename="system-info")
router.register(r"permissions", ObjectPermissionViewSet, basename="object-permissions")

urlpatterns = [
    path("", include(router.urls)),
]
