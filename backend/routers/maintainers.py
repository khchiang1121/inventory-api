from ninja import Router
from backend import models, schemas
from backend.dependencies import api_auth
from uuid import UUID

router = Router(tags=["Maintainer"], auth=api_auth)

@router.post("/", response=schemas.MaintainerSchema, auth=api_auth, status=201)
def create_maintainer(request, payload: schemas.MaintainerCreateSchema):
    maintainer = models.Maintainer.objects.create(**payload.dict())
    return maintainer

@router.get("/", response=list(schemas.MaintainerSchema), auth=api_auth)
def list_maintainers(request, page: int = 1, per_page: int = 10):
    qs = models.Maintainer.objects.all()[(page-1)*per_page:page*per_page]
    return qs

@router.get("/{maintainer_id}", response=schemas.MaintainerSchema, auth=api_auth)
def get_maintainer(request, maintainer_id: UUID):
    try:
        maintainer = models.Maintainer.objects.get(id=maintainer_id)
    except models.Maintainer.DoesNotExist:
        return api_auth.error("Maintainer not found", status=404)
    return maintainer

@router.put("/{maintainer_id}", response=schemas.MaintainerSchema, auth=api_auth)
def update_maintainer(request, maintainer_id: UUID, payload: schemas.MaintainerCreateSchema):
    try:
        maintainer = models.Maintainer.objects.get(id=maintainer_id)
    except models.Maintainer.DoesNotExist:
        return api_auth.error("Maintainer not found", status=404)
    for attr, value in payload.dict().items():
        setattr(maintainer, attr, value)
    maintainer.save()
    return maintainer

@router.delete("/{maintainer_id}", auth=api_auth)
def delete_maintainer(request, maintainer_id: UUID):
    try:
        maintainer = models.Maintainer.objects.get(id=maintainer_id)
    except models.Maintainer.DoesNotExist:
        return api_auth.error("Maintainer not found", status=404)
    maintainer.delete()
    return {"message": "Maintainer deleted successfully"}
