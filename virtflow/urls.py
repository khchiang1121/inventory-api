"""
URL configuration for virtflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from virtflow.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

# from django.contrib import admin
# from django.urls import path
# from ninja import NinjaAPI

# from backend.routers import (
#     maintainers,
#     maintainer_groups,
#     maintainer_group_members,
#     resource_maintainers,
#     hosts,
#     host_groups,
#     tenants,
#     virtual_machines,
#     vm_specifications,
#     k8s_clusters,
#     host_group_tenant_quotas,
# )

# api = NinjaAPI(title="Production Backend API", version="1.0.0")

# # 註冊各模組 router
# api.add_router("/maintainers", maintainers.router)
# api.add_router("/maintainer-groups", maintainer_groups.router)
# api.add_router("/maintainer-group-members", maintainer_group_members.router)
# api.add_router("/resource-maintainers", resource_maintainers.router)
# api.add_router("/hosts", hosts.router)
# api.add_router("/host-groups", host_groups.router)
# api.add_router("/tenants", tenants.router)
# api.add_router("/virtual-machines", virtual_machines.router)
# api.add_router("/vm-specifications", vm_specifications.router)
# api.add_router("/k8s-clusters", k8s_clusters.router)
# api.add_router("/host-group-tenant-quotas", host_group_tenant_quotas.router)

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", api.urls),
# ]
