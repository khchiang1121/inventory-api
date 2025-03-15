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
virtual_machine_specification_router = Router(tags=["VirtualMachineSpecification"], auth=api_auth)

@virtual_machine_specification_router.get("/", response=list[schemas.VirtualMachineSpecificationOutSchema])
def list_vmspecs(request):
    return models.VirtualMachineSpecification.objects.all()

@virtual_machine_specification_router.get("/{spec_id}", response=schemas.VirtualMachineSpecificationOutSchema)
def get_vmspec(request, spec_id: UUID):
    return get_object_or_404(models.VirtualMachineSpecification, id=spec_id)

@virtual_machine_specification_router.post("/", response=schemas.VirtualMachineSpecificationOutSchema)
def create_vmspec(request, payload: schemas.VirtualMachineSpecificationCreateSchema):
    spec = models.VirtualMachineSpecification.objects.create(**payload.dict())
    return spec

@virtual_machine_specification_router.put("/{spec_id}", response=schemas.VirtualMachineSpecificationOutSchema)
def update_vmspec(request, spec_id: UUID, payload: schemas.VirtualMachineSpecificationUpdateSchema):
    spec = get_object_or_404(models.VirtualMachineSpecification, id=spec_id)
    for attr, value in payload.dict().items():
        setattr(spec, attr, value)
    spec.save()
    return spec

@virtual_machine_specification_router.delete("/{spec_id}")
def delete_vmspec(request, spec_id: UUID):
    spec = get_object_or_404(models.VirtualMachineSpecification, id=spec_id)
    spec.delete()
    return {"success": True}
