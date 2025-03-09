from fastapi import APIRouter, HTTPException
from backend.models import Tenant
from backend.schemas import TenantSchema

router = APIRouter()

@router.post("/tenants/", response_model=TenantSchema)
def create_tenant(tenant: TenantSchema):
    db_tenant = Tenant(**tenant.dict())
    db_tenant.save()
    return db_tenant

@router.get("/tenants/{tenant_id}", response_model=TenantSchema)
def read_tenant(tenant_id: int):
    tenant = Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/tenants/{tenant_id}", response_model=TenantSchema)
def update_tenant(tenant_id: int, tenant: TenantSchema):
    db_tenant = Tenant.get(tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for key, value in tenant.dict().items():
        setattr(db_tenant, key, value)
    db_tenant.save()
    return db_tenant

@router.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: int):
    tenant = Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant.delete()
    return {"detail": "Tenant deleted"}