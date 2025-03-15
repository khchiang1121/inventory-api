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
# Tenant Router
# ----------------------------
tenant_router = Router(tags=["Tenant"], auth=api_auth)

@tenant_router.get("/", response=list[schemas.TenantOutSchema])
def list_tenants(request):
    return models.Tenant.objects.all()

@tenant_router.get("/{tenant_id}", response=schemas.TenantOutSchema)
def get_tenant(request, tenant_id: UUID):
    return get_object_or_404(models.Tenant, id=tenant_id)

@tenant_router.post("/", response=schemas.TenantOutSchema)
def create_tenant(request, payload: schemas.TenantCreateSchema):
    tenant = models.Tenant.objects.create(**payload.dict())
    return tenant

@tenant_router.put("/{tenant_id}", response=schemas.TenantOutSchema)
def update_tenant(request, tenant_id: UUID, payload: schemas.TenantUpdateSchema):
    tenant = get_object_or_404(models.Tenant, id=tenant_id)
    for attr, value in payload.dict().items():
        setattr(tenant, attr, value)
    tenant.save()
    return tenant

@tenant_router.delete("/{tenant_id}")
def delete_tenant(request, tenant_id: UUID):
    tenant = get_object_or_404(models.Tenant, id=tenant_id)
    tenant.delete()
    return {"success": True}
