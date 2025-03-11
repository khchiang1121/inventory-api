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
# VirtualMachineSpecification Router
# ----------------------------
vmspec_router = Router(tags=["VirtualMachineSpecification"], auth=api_auth)

@vmspec_router.get("/", response=list[schemas.VirtualMachineSpecificationSchemaOut])
def list_vmspecs(request):
    return models.VirtualMachineSpecification.objects.all()

@vmspec_router.get("/{spec_id}", response=schemas.VirtualMachineSpecificationSchemaOut)
def get_vmspec(request, spec_id: UUID):
    return get_object_or_404(models.VirtualMachineSpecification, id=spec_id)

@vmspec_router.post("/", response=schemas.VirtualMachineSpecificationSchemaOut)
def create_vmspec(request, payload: schemas.VirtualMachineSpecificationSchemaIn):
    spec = models.VirtualMachineSpecification.objects.create(**payload.dict())
    return spec

@vmspec_router.put("/{spec_id}", response=schemas.VirtualMachineSpecificationSchemaOut)
def update_vmspec(request, spec_id: UUID, payload: schemas.VirtualMachineSpecificationSchemaIn):
    spec = get_object_or_404(models.VirtualMachineSpecification, id=spec_id)
    for attr, value in payload.dict().items():
        setattr(spec, attr, value)
    spec.save()
    return spec

@vmspec_router.delete("/{spec_id}")
def delete_vmspec(request, spec_id: UUID):
    spec = get_object_or_404(models.VirtualMachineSpecification, id=spec_id)
    spec.delete()
    return {"success": True}
