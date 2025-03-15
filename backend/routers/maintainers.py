from uuid import UUID
from ninja import Router
from backend import models, schemas
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

maintainer_router = Router(tags=["Maintainer"], auth = api_auth)

@maintainer_router.get("/", response=list[schemas.MaintainerOutSchema])
def list_maintainers(request):
    return models.Maintainer.objects.all()

@maintainer_router.get("/{maintainer_id}", response=schemas.MaintainerOutSchema)
def get_maintainer(request, maintainer_id: UUID):
    return get_object_or_404(models.Maintainer, id=maintainer_id)

@maintainer_router.post("/", response=schemas.MaintainerOutSchema)
def create_maintainer(request, payload: schemas.MaintainerCreateSchema):
    maintainer = models.Maintainer.objects.create(**payload.dict())
    return maintainer

@maintainer_router.put("/{maintainer_id}", response=schemas.MaintainerOutSchema)
def update_maintainer(request, maintainer_id: UUID, payload: schemas.MaintainerUpdateSchema):
    maintainer = get_object_or_404(models.Maintainer, id=maintainer_id)
    for attr, value in payload.dict().items():
        setattr(maintainer, attr, value)
    maintainer.save()
    return maintainer

@maintainer_router.delete("/{maintainer_id}")
def delete_maintainer(request, maintainer_id: UUID):
    maintainer = get_object_or_404(models.Maintainer, id=maintainer_id)
    maintainer.delete()
    return {"success": True}
