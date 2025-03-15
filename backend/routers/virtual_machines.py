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
# VirtualMachine Router
# ----------------------------
virtual_machine_router = Router(tags=["VirtualMachine"], auth=api_auth)

@virtual_machine_router.get("/", response=list[schemas.VirtualMachineOutSchema])
def list_virtual_machines(request):
    return models.VirtualMachine.objects.all()

@virtual_machine_router.get("/{vm_id}", response=schemas.VirtualMachineOutSchema)
def get_virtual_machine(request, vm_id: UUID):
    return get_object_or_404(models.VirtualMachine, id=vm_id)

@virtual_machine_router.post("/", response=schemas.VirtualMachineOutSchema)
def create_virtual_machine(request, payload: schemas.VirtualMachineCreateSchema):
    vm = models.VirtualMachine.objects.create(**payload.dict())
    return vm

@virtual_machine_router.put("/{vm_id}", response=schemas.VirtualMachineOutSchema)
def update_virtual_machine(request, vm_id: UUID, payload: schemas.VirtualMachineUpdateSchema):
    vm = get_object_or_404(models.VirtualMachine, id=vm_id)
    for attr, value in payload.dict().items():
        setattr(vm, attr, value)
    vm.save()
    return vm

@virtual_machine_router.delete("/{vm_id}")
def delete_virtual_machine(request, vm_id: UUID):
    vm = get_object_or_404(models.VirtualMachine, id=vm_id)
    vm.delete()
    return {"success": True}
