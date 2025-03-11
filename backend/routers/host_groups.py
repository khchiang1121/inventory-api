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


# # from backend.models import HostGroup
# from backend.schemas.host import HostGroupSchema

# router = APIRouter()

# @router.post("/host-groups/", response_model=HostGroupSchema)
# def create_host_group(host_group: HostGroupSchema):
#     db_host_group = HostGroup(**host_group.dict())
#     db_host_group.save()
#     return db_host_group

# @router.get("/host-groups/{host_group_id}", response_model=HostGroupSchema)
# def read_host_group(host_group_id: int):
#     host_group = HostGroup.get_by_id(host_group_id)
#     if not host_group:
#         raise HTTPException(status_code=404, detail="Host group not found")
#     return host_group

# @router.put("/host-groups/{host_group_id}", response_model=HostGroupSchema)
# def update_host_group(host_group_id: int, host_group: HostGroupSchema):
#     db_host_group = HostGroup.get_by_id(host_group_id)
#     if not db_host_group:
#         raise HTTPException(status_code=404, detail="Host group not found")
#     for key, value in host_group.dict().items():
#         setattr(db_host_group, key, value)
#     db_host_group.save()
#     return db_host_group

# @router.delete("/host-groups/{host_group_id}")
# def delete_host_group(host_group_id: int):
#     host_group = HostGroup.get_by_id(host_group_id)
#     if not host_group:
#         raise HTTPException(status_code=404, detail="Host group not found")
#     host_group.delete()
#     return {"detail": "Host group deleted"}