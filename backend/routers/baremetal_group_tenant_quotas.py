from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.models import MaintainerGroup
from backend import schemas
from typing import List
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# BaremetalGroupTenantQuota Router
# ----------------------------
baremetal_group_tenant_quota_router = Router(tags=["BaremetalGroupTenantQuota"], auth=api_auth)

@baremetal_group_tenant_quota_router.get("/", response=list[schemas.BaremetalGroupTenantQuotaOutSchema])
def list_hostgroup_tenant_quotas(request):
    return models.BaremetalGroupTenantQuota.objects.all()

@baremetal_group_tenant_quota_router.get("/{quota_id}", response=schemas.BaremetalGroupTenantQuotaOutSchema)
def get_hostgroup_tenant_quota(request, quota_id: UUID):
    return get_object_or_404(models.BaremetalGroupTenantQuota, id=quota_id)

@baremetal_group_tenant_quota_router.post("/", response=schemas.BaremetalGroupTenantQuotaOutSchema)
def create_hostgroup_tenant_quota(request, payload: schemas.BaremetalGroupTenantQuotaCreateSchema):
    quota = models.BaremetalGroupTenantQuota.objects.create(**payload.dict())
    return quota

@baremetal_group_tenant_quota_router.put("/{quota_id}", response=schemas.BaremetalGroupTenantQuotaOutSchema)
def update_hostgroup_tenant_quota(request, quota_id: UUID, payload: schemas.BaremetalGroupTenantQuotaUpdateSchema):
    quota = get_object_or_404(models.BaremetalGroupTenantQuota, id=quota_id)
    for attr, value in payload.dict().items():
        setattr(quota, attr, value)
    quota.save()
    return quota

@baremetal_group_tenant_quota_router.delete("/{quota_id}")
def delete_hostgroup_tenant_quota(request, quota_id: UUID):
    quota = get_object_or_404(models.BaremetalGroupTenantQuota, id=quota_id)
    quota.delete()
    return {"success": True}
