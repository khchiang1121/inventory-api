from ninja import NinjaAPI
from django.contrib import admin
from django.urls import path

from backend.routers import (
    maintainers,
    maintainer_groups,
    maintainer_group_members,
    resource_maintainers,
    host_groups,
    hosts,
    tenants,
    virtual_machines,
    k8s_clusters,
    virtual_machine_specifications,
    host_group_tenant_quotas
)
from ninja import Redoc, Swagger

# api = NinjaAPI(title="Production Backend API", version="1.0.0")
api = NinjaAPI(title="Virtflow Backend API", version="1.0.0", docs=Redoc(settings={"persistAuthorization": True}))
# api = NinjaAPI(title="Production Backend API", version="1.0.0", docs=Swagger(settings={"persistAuthorization": True}))

# # 註冊各模組 router
# api.add_router("/maintainers", maintainers.router)
# api.add_router("/maintainer-groups", maintainer_groups.router)
# api.add_router("/maintainer-group-members", maintainer_group_members.router)
# api.add_router("/resource-maintainers", resource_maintainers.router)
# api.add_router("/hosts", hosts.host_router)
# api.add_router("/host-groups", host_groups.router)
# api.add_router("/tenants", tenants.router)
# api.add_router("/virtual-machines", virtual_machines.router)
# api.add_router("/vm-specifications", vm_specifications.router)
# api.add_router("/k8s-clusters", k8s_clusters.router)
# api.add_router("/host-group-tenant-quotas", host_group_tenant_quotas.router)

api.add_router("/maintainers", maintainers.maintainer_router)
api.add_router("/maintainer-groups", maintainer_groups.maintainer_group_router)
api.add_router("/group-members", maintainer_group_members.maintainer_group_member_router)
api.add_router("/resource-maintainers", resource_maintainers.resource_maintainer_router)
api.add_router("/host-groups", host_groups.hostgroup_router)
api.add_router("/hosts", hosts.host_router)
api.add_router("/tenants", tenants.tenant_router)
api.add_router("/vm-specifications", virtual_machine_specifications.vmspec_router)
api.add_router("/k8s-clusters", k8s_clusters.k8s_cluster_router)
api.add_router("/virtual-machines", virtual_machines.vm_router)
api.add_router("/hostgroup-tenant-quotas", host_group_tenant_quotas.hostgroup_tenant_quota_router)