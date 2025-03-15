from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# Rack Router
# ----------------------------
rack_router = Router(tags=["Rack"], auth=api_auth)

@rack_router.get("/", response=list[schemas.RackOutSchema])
def list_racks(request):
    return models.Rack.objects.all()

@rack_router.get("/{rack_id}", response=schemas.RackOutSchema)
def get_rack(request, rack_id: UUID):
    return get_object_or_404(models.Rack, id=rack_id)

@rack_router.post("/", response=schemas.RackOutSchema)
def create_rack(request, payload: schemas.RackCreateSchema):
    rack = models.Rack.objects.create(**payload.dict())
    return rack

@rack_router.put("/{rack_id}", response=schemas.RackOutSchema)
def update_rack(request, rack_id: UUID, payload: schemas.RackUpdateSchema):
    rack = get_object_or_404(models.Rack, id=rack_id)
    for attr, value in payload.dict().items():
        setattr(rack, attr, value)
    rack.save()
    return rack

@rack_router.delete("/{rack_id}")
def delete_rack(request, rack_id: UUID):
    rack = get_object_or_404(models.Rack, id=rack_id)
    rack.delete()
    return {"success": True}
