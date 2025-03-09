from fastapi import APIRouter, HTTPException
from backend.models import MaintainerGroup
from backend.schemas import MaintainerGroupSchema
from typing import List

router = APIRouter()

@router.post("/maintainer-groups/", response_model=MaintainerGroupSchema)
def create_maintainer_group(group: MaintainerGroupSchema):
    db_group = MaintainerGroup(**group.dict())
    db_group.save()
    return db_group

@router.get("/maintainer-groups/", response_model=List[MaintainerGroupSchema])
def read_maintainer_groups():
    return MaintainerGroup.objects.all()

@router.get("/maintainer-groups/{group_id}", response_model=MaintainerGroupSchema)
def read_maintainer_group(group_id: int):
    group = MaintainerGroup.objects.get(id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Maintainer group not found")
    return group

@router.put("/maintainer-groups/{group_id}", response_model=MaintainerGroupSchema)
def update_maintainer_group(group_id: int, group: MaintainerGroupSchema):
    db_group = MaintainerGroup.objects.get(id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Maintainer group not found")
    for key, value in group.dict().items():
        setattr(db_group, key, value)
    db_group.save()
    return db_group

@router.delete("/maintainer-groups/{group_id}")
def delete_maintainer_group(group_id: int):
    db_group = MaintainerGroup.objects.get(id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Maintainer group not found")
    db_group.delete()
    return {"detail": "Maintainer group deleted"}