from fastapi import APIRouter, HTTPException
from backend.models import HostGroup
from backend.schemas import HostGroupSchema

router = APIRouter()

@router.post("/host-groups/", response_model=HostGroupSchema)
def create_host_group(host_group: HostGroupSchema):
    db_host_group = HostGroup(**host_group.dict())
    db_host_group.save()
    return db_host_group

@router.get("/host-groups/{host_group_id}", response_model=HostGroupSchema)
def read_host_group(host_group_id: int):
    host_group = HostGroup.get_by_id(host_group_id)
    if not host_group:
        raise HTTPException(status_code=404, detail="Host group not found")
    return host_group

@router.put("/host-groups/{host_group_id}", response_model=HostGroupSchema)
def update_host_group(host_group_id: int, host_group: HostGroupSchema):
    db_host_group = HostGroup.get_by_id(host_group_id)
    if not db_host_group:
        raise HTTPException(status_code=404, detail="Host group not found")
    for key, value in host_group.dict().items():
        setattr(db_host_group, key, value)
    db_host_group.save()
    return db_host_group

@router.delete("/host-groups/{host_group_id}")
def delete_host_group(host_group_id: int):
    host_group = HostGroup.get_by_id(host_group_id)
    if not host_group:
        raise HTTPException(status_code=404, detail="Host group not found")
    host_group.delete()
    return {"detail": "Host group deleted"}