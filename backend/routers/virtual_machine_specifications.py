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
# # from pydantic import BaseModel
# from typing import List

# # Define the Pydantic model for VM Specifications
# class VMSpecification(BaseModel):
#     id: int
#     name: str
#     cpu: int
#     memory: int
#     disk_size: int

# # In-memory storage for VM Specifications
# vm_specifications_db = []

# router = APIRouter()

# @router.post("/vm-specifications/", response_model=VMSpecification)
# def create_vm_specification(vm_spec: VMSpecification):
#     vm_specifications_db.append(vm_spec)
#     return vm_spec

# @router.get("/vm-specifications/", response_model=List[VMSpecification])
# def get_vm_specifications():
#     return vm_specifications_db

# @router.get("/vm-specifications/{vm_id}", response_model=VMSpecification)
# def get_vm_specification(vm_id: int):
#     for vm in vm_specifications_db:
#         if vm.id == vm_id:
#             return vm
#     raise HTTPException(status_code=404, detail="VM Specification not found")

# @router.put("/vm-specifications/{vm_id}", response_model=VMSpecification)
# def update_vm_specification(vm_id: int, vm_spec: VMSpecification):
#     for index, vm in enumerate(vm_specifications_db):
#         if vm.id == vm_id:
#             vm_specifications_db[index] = vm_spec
#             return vm_spec
#     raise HTTPException(status_code=404, detail="VM Specification not found")

# @router.delete("/vm-specifications/{vm_id}", response_model=VMSpecification)
# def delete_vm_specification(vm_id: int):
#     for index, vm in enumerate(vm_specifications_db):
#         if vm.id == vm_id:
#             return vm_specifications_db.pop(index)
#     raise HTTPException(status_code=404, detail="VM Specification not found")