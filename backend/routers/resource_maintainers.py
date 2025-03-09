from fastapi import APIRouter, HTTPException
from backend.models import ResourceMaintainer
from backend.schemas import ResourceMaintainerSchema
from typing import List

router = APIRouter()

@router.post("/resource-maintainers/", response_model=ResourceMaintainerSchema)
def create_resource_maintainer(resource_maintainer: ResourceMaintainerSchema):
    db_resource_maintainer = ResourceMaintainer(**resource_maintainer.dict())
    db_resource_maintainer.save()
    return db_resource_maintainer

@router.get("/resource-maintainers/", response_model=List[ResourceMaintainerSchema])
def read_resource_maintainers(skip: int = 0, limit: int = 10):
    return ResourceMaintainer.objects.all()[skip: skip + limit]

@router.get("/resource-maintainers/{resource_maintainer_id}", response_model=ResourceMaintainerSchema)
def read_resource_maintainer(resource_maintainer_id: int):
    resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
    if not resource_maintainer:
        raise HTTPException(status_code=404, detail="Resource maintainer not found")
    return resource_maintainer

@router.put("/resource-maintainers/{resource_maintainer_id}", response_model=ResourceMaintainerSchema)
def update_resource_maintainer(resource_maintainer_id: int, resource_maintainer: ResourceMaintainerSchema):
    db_resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
    if not db_resource_maintainer:
        raise HTTPException(status_code=404, detail="Resource maintainer not found")
    for key, value in resource_maintainer.dict().items():
        setattr(db_resource_maintainer, key, value)
    db_resource_maintainer.save()
    return db_resource_maintainer

@router.delete("/resource-maintainers/{resource_maintainer_id}")
def delete_resource_maintainer(resource_maintainer_id: int):
    resource_maintainer = ResourceMaintainer.objects.get(id=resource_maintainer_id)
    if not resource_maintainer:
        raise HTTPException(status_code=404, detail="Resource maintainer not found")
    resource_maintainer.delete()
    return {"detail": "Resource maintainer deleted"}