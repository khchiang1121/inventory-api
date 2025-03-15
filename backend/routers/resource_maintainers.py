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
# ResourceMaintainer Router
# ----------------------------
resource_maintainer_router = Router(tags=["ResourceMaintainer"], auth=api_auth)

@resource_maintainer_router.get("/", response=list[schemas.ResourceMaintainerOutSchema])
def list_resource_maintainers(request):
    return models.ResourceMaintainer.objects.all()

@resource_maintainer_router.get("/{rm_id}", response=schemas.ResourceMaintainerOutSchema)
def get_resource_maintainer(request, rm_id: UUID):
    return get_object_or_404(models.ResourceMaintainer, id=rm_id)

@resource_maintainer_router.post("/", response=schemas.ResourceMaintainerOutSchema)
def create_resource_maintainer(request, payload: schemas.ResourceMaintainerCreateSchema):
    rm = models.ResourceMaintainer.objects.create(**payload.dict())
    return rm

@resource_maintainer_router.put("/{rm_id}", response=schemas.ResourceMaintainerOutSchema)
def update_resource_maintainer(request, rm_id: UUID, payload: schemas.ResourceMaintainerUpdateSchema):
    rm = get_object_or_404(models.ResourceMaintainer, id=rm_id)
    for attr, value in payload.dict().items():
        setattr(rm, attr, value)
    rm.save()
    return rm

@resource_maintainer_router.delete("/{rm_id}")
def delete_resource_maintainer(request, rm_id: UUID):
    rm = get_object_or_404(models.ResourceMaintainer, id=rm_id)
    rm.delete()
    return {"success": True}
