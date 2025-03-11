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
# MaintainerGroupMember Router
# ----------------------------
maintainer_group_member_router = Router(tags=["MaintainerGroupMember"], auth=api_auth)

@maintainer_group_member_router.get("/", response=list[schemas.MaintainerGroupMemberSchemaOut])
def list_group_members(request):
    return models.MaintainerGroupMember.objects.all()

@maintainer_group_member_router.get("/{member_id}", response=schemas.MaintainerGroupMemberSchemaOut)
def get_group_member(request, member_id: UUID):
    return get_object_or_404(models.MaintainerGroupMember, id=member_id)

@maintainer_group_member_router.post("/", response=schemas.MaintainerGroupMemberSchemaOut)
def create_group_member(request, payload: schemas.MaintainerGroupMemberSchemaIn):
    member = models.MaintainerGroupMember.objects.create(**payload.dict())
    return member

@maintainer_group_member_router.put("/{member_id}", response=schemas.MaintainerGroupMemberSchemaOut)
def update_group_member(request, member_id: UUID, payload: schemas.MaintainerGroupMemberSchemaIn):
    member = get_object_or_404(models.MaintainerGroupMember, id=member_id)
    for attr, value in payload.dict().items():
        setattr(member, attr, value)
    member.save()
    return member

@maintainer_group_member_router.delete("/{member_id}")
def delete_group_member(request, member_id: UUID):
    member = get_object_or_404(models.MaintainerGroupMember, id=member_id)
    member.delete()
    return {"success": True}
