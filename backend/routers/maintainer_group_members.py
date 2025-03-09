from fastapi import APIRouter, HTTPException
from backend.models import MaintainerGroupMember
from backend.schemas import MaintainerGroupMemberSchema
from typing import List

router = APIRouter()

@router.post("/maintainer_group_members/", response_model=MaintainerGroupMemberSchema)
def create_maintainer_group_member(member: MaintainerGroupMemberSchema):
    db_member = MaintainerGroupMember(**member.dict())
    db_member.save()
    return db_member

@router.get("/maintainer_group_members/", response_model=List[MaintainerGroupMemberSchema])
def read_maintainer_group_members(skip: int = 0, limit: int = 10):
    members = MaintainerGroupMember.objects.all()[skip: skip + limit]
    return members

@router.get("/maintainer_group_members/{member_id}", response_model=MaintainerGroupMemberSchema)
def read_maintainer_group_member(member_id: int):
    member = MaintainerGroupMember.objects.get(id=member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.put("/maintainer_group_members/{member_id}", response_model=MaintainerGroupMemberSchema)
def update_maintainer_group_member(member_id: int, member: MaintainerGroupMemberSchema):
    db_member = MaintainerGroupMember.objects.get(id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    db_member.save()
    return db_member

@router.delete("/maintainer_group_members/{member_id}")
def delete_maintainer_group_member(member_id: int):
    member = MaintainerGroupMember.objects.get(id=member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    member.delete()
    return {"detail": "Member deleted"}