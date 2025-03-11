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
# HostGroupTenantQuota Router
# ----------------------------
hostgroup_tenant_quota_router = Router(tags=["HostGroupTenantQuota"], auth=api_auth)

@hostgroup_tenant_quota_router.get("/", response=list[schemas.HostGroupTenantQuotaSchemaOut])
def list_hostgroup_tenant_quotas(request):
    return models.HostGroupTenantQuota.objects.all()

@hostgroup_tenant_quota_router.get("/{quota_id}", response=schemas.HostGroupTenantQuotaSchemaOut)
def get_hostgroup_tenant_quota(request, quota_id: UUID):
    return get_object_or_404(models.HostGroupTenantQuota, id=quota_id)

@hostgroup_tenant_quota_router.post("/", response=schemas.HostGroupTenantQuotaSchemaOut)
def create_hostgroup_tenant_quota(request, payload: schemas.HostGroupTenantQuotaSchemaIn):
    quota = models.HostGroupTenantQuota.objects.create(**payload.dict())
    return quota

@hostgroup_tenant_quota_router.put("/{quota_id}", response=schemas.HostGroupTenantQuotaSchemaOut)
def update_hostgroup_tenant_quota(request, quota_id: UUID, payload: schemas.HostGroupTenantQuotaSchemaIn):
    quota = get_object_or_404(models.HostGroupTenantQuota, id=quota_id)
    for attr, value in payload.dict().items():
        setattr(quota, attr, value)
    quota.save()
    return quota

@hostgroup_tenant_quota_router.delete("/{quota_id}")
def delete_hostgroup_tenant_quota(request, quota_id: UUID):
    quota = get_object_or_404(models.HostGroupTenantQuota, id=quota_id)
    quota.delete()
    return {"success": True}