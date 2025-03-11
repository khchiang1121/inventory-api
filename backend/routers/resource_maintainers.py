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

@resource_maintainer_router.get("/", response=list[schemas.ResourceMaintainerSchemaOut])
def list_resource_maintainers(request):
    return models.ResourceMaintainer.objects.all()

@resource_maintainer_router.get("/{rm_id}", response=schemas.ResourceMaintainerSchemaOut)
def get_resource_maintainer(request, rm_id: UUID):
    return get_object_or_404(models.ResourceMaintainer, id=rm_id)

@resource_maintainer_router.post("/", response=schemas.ResourceMaintainerSchemaOut)
def create_resource_maintainer(request, payload: schemas.ResourceMaintainerSchemaIn):
    rm = models.ResourceMaintainer.objects.create(**payload.dict())
    return rm

@resource_maintainer_router.put("/{rm_id}", response=schemas.ResourceMaintainerSchemaOut)
def update_resource_maintainer(request, rm_id: UUID, payload: schemas.ResourceMaintainerSchemaIn):
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

# # from backend.models import ResourceMaintainer
# from backend.schemas.host import ResourceMaintainerSchema
# from typing import List

# router = APIRouter()

# @router.post("/resource-maintainers/", response_model=ResourceMaintainerSchema)
# def create_resource_maintainer(resource_maintainer: ResourceMaintainerSchema):
#     db_resource_maintainer = ResourceMaintainer(**resource_maintainer.dict())
#     db_resource_maintainer.save()
#     return db_resource_maintainer

# @router.get("/resource-maintainers/", response_model=List[ResourceMaintainerSchema])
# def read_resource_maintainers(skip: int = 0, limit: int = 10):
#     return ResourceMaintainer.objects.all()[skip: skip + limit]

# @router.get("/resource-maintainers/{resource_maintainer_id}", response_model=ResourceMaintainerSchema)
# def read_resource_maintainer(resource_maintainer_id: int):
#     resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
#     if not resource_maintainer:
#         raise HTTPException(status_code=404, detail="Resource maintainer not found")
#     return resource_maintainer

# @router.put("/resource-maintainers/{resource_maintainer_id}", response_model=ResourceMaintainerSchema)
# def update_resource_maintainer(resource_maintainer_id: int, resource_maintainer: ResourceMaintainerSchema):
#     db_resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
#     if not db_resource_maintainer:
#         raise HTTPException(status_code=404, detail="Resource maintainer not found")
#     for key, value in resource_maintainer.dict().items():
#         setattr(db_resource_maintainer, key, value)
#     db_resource_maintainer.save()
#     return db_resource_maintainer

# @router.delete("/resource-maintainers/{resource_maintainer_id}")
# def delete_resource_maintainer(resource_maintainer_id: int):
#     resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
#     if not resource_maintainer:
#         raise HTTPException(status_code=404, detail="Resource maintainer not found")
#     resource_maintainer.delete()
#     return {"detail": "Resource maintainer deleted"}