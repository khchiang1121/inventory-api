from ninja import NinjaAPI
from django.contrib import admin
from django.urls import path

# from ninja import NinjaAPI
# api = NinjaAPI()

# api.add_router(prefix='/users/', router='user.api.router')
# api.add_router(prefix='/posts/', router='post.api.router')


# from user.api import router as user_router
# from post.api import router as post_router

# api.add_router(prefix='/users/', router=user_router)
# api.add_router(prefix='/posts/', router=post_router)


from backend.routers import (
    # maintainers,
    # maintainer_groups,
    # maintainer_group_members,
    # resource_maintainers,
    hosts,
    # host_groups,
    # tenants,
    # virtual_machines,
    # vm_specifications,
    # k8s_clusters,
    # host_group_tenant_quotas,
)
api = NinjaAPI(title="Production Backend API", version="1.0.0")

# # 註冊各模組 router
# api.add_router("/maintainers", maintainers.router)
# api.add_router("/maintainer-groups", maintainer_groups.router)
# api.add_router("/maintainer-group-members", maintainer_group_members.router)
# api.add_router("/resource-maintainers", resource_maintainers.router)
api.add_router("/hosts", hosts.router)
# api.add_router("/host-groups", host_groups.router)
# api.add_router("/tenants", tenants.router)
# api.add_router("/virtual-machines", virtual_machines.router)
# api.add_router("/vm-specifications", vm_specifications.router)
# api.add_router("/k8s-clusters", k8s_clusters.router)
# api.add_router("/host-group-tenant-quotas", host_group_tenant_quotas.router)
