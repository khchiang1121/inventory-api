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
# MaintainerGroup Router
# ----------------------------
maintainer_group_router = Router(tags=["MaintainerGroup"], auth=api_auth)

@maintainer_group_router.get("/", response=list[schemas.MaintainerGroupSchemaOut])
def list_maintainer_groups(request):
    return models.MaintainerGroup.objects.all()

@maintainer_group_router.get("/{group_id}", response=schemas.MaintainerGroupSchemaOut)
def get_maintainer_group(request, group_id: UUID):
    return get_object_or_404(models.MaintainerGroup, id=group_id)

@maintainer_group_router.post("/", response=schemas.MaintainerGroupSchemaOut)
def create_maintainer_group(request, payload: schemas.MaintainerGroupSchemaIn):
    group = models.MaintainerGroup.objects.create(**payload.dict())
    return group

@maintainer_group_router.put("/{group_id}", response=schemas.MaintainerGroupSchemaOut)
def update_maintainer_group(request, group_id: UUID, payload: schemas.MaintainerGroupSchemaIn):
    group = get_object_or_404(models.MaintainerGroup, id=group_id)
    for attr, value in payload.dict().items():
        setattr(group, attr, value)
    group.save()
    return group

@maintainer_group_router.delete("/{group_id}")
def delete_maintainer_group(request, group_id: UUID):
    group = get_object_or_404(models.MaintainerGroup, id=group_id)
    group.delete()
    return {"success": True}

