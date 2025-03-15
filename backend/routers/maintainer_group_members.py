from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend import schemas
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# MaintainerToMaintainerGroup Router
# ----------------------------
maintainer_group_member_router = Router(tags=["MaintainerToMaintainerGroup"], auth=api_auth)

@maintainer_group_member_router.get("/", response=list[schemas.MaintainerToMaintainerGroupOutSchema])
def list_group_members(request):
    return models.MaintainerToMaintainerGroup.objects.all()

@maintainer_group_member_router.get("/{member_id}", response=schemas.MaintainerToMaintainerGroupOutSchema)
def get_group_member(request, member_id: UUID):
    return get_object_or_404(models.MaintainerToMaintainerGroup, id=member_id)

@maintainer_group_member_router.post("/", response=schemas.MaintainerToMaintainerGroupOutSchema)
def create_group_member(request, payload: schemas.MaintainerToMaintainerGroupCreateSchema):
    member = models.MaintainerToMaintainerGroup.objects.create(**payload.dict())
    return member

@maintainer_group_member_router.put("/{member_id}", response=schemas.MaintainerToMaintainerGroupOutSchema)
def update_group_member(request, member_id: UUID, payload: schemas.MaintainerToMaintainerGroupUpdateSchema):
    member = get_object_or_404(models.MaintainerToMaintainerGroup, id=member_id)
    for attr, value in payload.dict().items():
        setattr(member, attr, value)
    member.save()
    return member

@maintainer_group_member_router.delete("/{member_id}")
def delete_group_member(request, member_id: UUID):
    member = get_object_or_404(models.MaintainerToMaintainerGroup, id=member_id)
    member.delete()
    return {"success": True}
