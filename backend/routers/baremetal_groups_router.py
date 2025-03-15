from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.models import MaintainerGroup
from backend import schemas
from typing import List
from backend.dependencies import api_auth

# ----------------------------
# BaremetalGroup Router
# ----------------------------
baremetal_router = Router(tags=["BaremetalGroup"], auth=api_auth)

@baremetal_router.get("/", response=list[schemas.BaremetalGroupOutSchema])
def list_hostgroups(request):
    return models.BaremetalGroup.objects.all()

@baremetal_router.get("/{group_id}", response=schemas.BaremetalGroupOutSchema)
def get_hostgroup(request, group_id: UUID):
    return models.BaremetalGroup.objects.get(id=group_id)

@baremetal_router.post("/", response=schemas.BaremetalGroupOutSchema)
def create_hostgroup(request, payload: schemas.BaremetalGroupCreateSchema):
    group = models.BaremetalGroup.objects.create(**payload.dict())
    return group

@baremetal_router.put("/{group_id}", response=schemas.BaremetalGroupOutSchema)
def update_hostgroup(request, group_id: UUID, payload: schemas.BaremetalGroupUpdateSchema):
    group = models.BaremetalGroup.objects.get(id=group_id)
    for attr, value in payload.dict().items():
        setattr(group, attr, value)
    group.save()
    return group

@baremetal_router.delete("/{group_id}")
def delete_hostgroup(request, group_id: UUID):
    group = models.BaremetalGroup.objects.get(id=group_id)
    group.delete()
    return {"success": True}
