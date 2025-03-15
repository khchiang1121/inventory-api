from ninja import NinjaAPI
from django.contrib import admin
from django.urls import path
from backend.dependencies import AuthBearer
from backend.routers import (
    baremetal_group_tenant_quotas,
    baremetal_groups_router,
    baremetals,
    maintainers,
    maintainer_groups,
    maintainer_group_members,
    resource_maintainers,
    tenants,
    virtual_machines,
    k8s_clusters,
    virtual_machine_specifications,
    racks,
    k8s_cluster_plugins,
    bastion_cluster_associations,
    k8s_cluster_to_service_meshes,
    service_meshes
)
from ninja import Redoc, Swagger

# api = NinjaAPI(title="Virtflow Backend API", version="1.0.0")
api = NinjaAPI(title="Virtflow Backend API", version="1.0.0", docs=Redoc(settings={"persistAuthorization": True}))
# api = NinjaAPI(title="Production Backend API", version="1.0.0", docs=Swagger(settings={"persistAuthorization": True}))

api.add_router("/maintainers", maintainers.maintainer_router)
api.add_router("/maintainer-groups", maintainer_groups.maintainer_group_router)
api.add_router("/maintainer-group-members", maintainer_group_members.maintainer_group_member_router)
api.add_router("/resource-maintainers", resource_maintainers.resource_maintainer_router)
api.add_router("/baremetal-groups", baremetal_groups_router.baremetal_router)
api.add_router("/baremetals", baremetals.baremetal_router)
api.add_router("/tenants", tenants.tenant_router)
api.add_router("/virtual-machine-specifications", virtual_machine_specifications.virtual_machine_specification_router)
api.add_router("/k8s-clusters", k8s_clusters.k8s_cluster_router)
api.add_router("/virtual-machines", virtual_machines.virtual_machine_router)
api.add_router("/baremetal-group-tenant-quotas", baremetal_group_tenant_quotas.baremetal_group_tenant_quota_router)
api.add_router("/racks", racks.rack_router)
api.add_router("/k8s-cluster-plugins", k8s_cluster_plugins.k8s_cluster_plugin_router)
api.add_router("/bastion-cluster-associations", bastion_cluster_associations.bastion_cluster_association_router)
api.add_router("/k8s-cluster-to-service-meshes", k8s_cluster_to_service_meshes.k8s_cluster_to_service_mesh_router)
api.add_router("/service-meshes", service_meshes.service_mesh_router)
