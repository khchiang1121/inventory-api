from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.models import MaintainerGroup
from backend import schemas
from typing import List
from backend.dependencies import api_auth

# ----------------------------
# HostGroup Router
# ----------------------------
hostgroup_router = Router(tags=["HostGroup"], auth=api_auth)

@hostgroup_router.get("/", response=list[schemas.HostGroupSchemaOut])
def list_hostgroups(request):
    return models.HostGroup.objects.all()

@hostgroup_router.get("/{group_id}", response=schemas.HostGroupSchemaOut)
def get_hostgroup(request, group_id: UUID):
    return models.HostGroup.objects.get(id=group_id)

@hostgroup_router.post("/", response=schemas.HostGroupSchemaOut)
def create_hostgroup(request, payload: schemas.HostGroupSchemaIn):
    group = models.HostGroup.objects.create(**payload.dict())
    return group

@hostgroup_router.put("/{group_id}", response=schemas.HostGroupSchemaOut)
def update_hostgroup(request, group_id: UUID, payload: schemas.HostGroupSchemaIn):
    group = models.HostGroup.objects.get(id=group_id)
    for attr, value in payload.dict().items():
        setattr(group, attr, value)
    group.save()
    return group

@hostgroup_router.delete("/{group_id}")
def delete_hostgroup(request, group_id: UUID):
    group = models.HostGroup.objects.get(id=group_id)
    group.delete()
    return {"success": True}
