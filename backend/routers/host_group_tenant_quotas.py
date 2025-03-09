from fastapi import APIRouter, HTTPException
from backend.models import HostGroupTenantQuota
from backend.schemas import HostGroupTenantQuotaSchema
from typing import List

router = APIRouter()

@router.post("/host-group-tenant-quotas/", response_model=HostGroupTenantQuotaSchema)
def create_host_group_tenant_quota(quota: HostGroupTenantQuotaSchema):
    db_quota = HostGroupTenantQuota(**quota.dict())
    db_quota.save()
    return db_quota

@router.get("/host-group-tenant-quotas/", response_model=List[HostGroupTenantQuotaSchema])
def read_host_group_tenant_quotas():
    return HostGroupTenantQuota.objects.all()

@router.get("/host-group-tenant-quotas/{quota_id}", response_model=HostGroupTenantQuotaSchema)
def read_host_group_tenant_quota(quota_id: int):
    quota = HostGroupTenantQuota.objects.get(id=quota_id)
    if not quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    return quota

@router.put("/host-group-tenant-quotas/{quota_id}", response_model=HostGroupTenantQuotaSchema)
def update_host_group_tenant_quota(quota_id: int, quota: HostGroupTenantQuotaSchema):
    db_quota = HostGroupTenantQuota.objects.get(id=quota_id)
    if not db_quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    for key, value in quota.dict().items():
        setattr(db_quota, key, value)
    db_quota.save()
    return db_quota

@router.delete("/host-group-tenant-quotas/{quota_id}")
def delete_host_group_tenant_quota(quota_id: int):
    quota = HostGroupTenantQuota.objects.get(id=quota_id)
    if not quota:
        raise HTTPException(status_code=404, detail="Quota not found")
    quota.delete()
    return {"detail": "Quota deleted"}