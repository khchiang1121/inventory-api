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
vm_router = Router(tags=["VirtualMachine"], auth=api_auth)

@vm_router.get("/", response=list[schemas.VirtualMachineSchemaOut])
def list_virtual_machines(request):
    return models.VirtualMachine.objects.all()

@vm_router.get("/{vm_id}", response=schemas.VirtualMachineSchemaOut)
def get_virtual_machine(request, vm_id: UUID):
    return get_object_or_404(models.VirtualMachine, id=vm_id)

@vm_router.post("/", response=schemas.VirtualMachineSchemaOut)
def create_virtual_machine(request, payload: schemas.VirtualMachineSchemaIn):
    vm = models.VirtualMachine.objects.create(**payload.dict())
    return vm

@vm_router.put("/{vm_id}", response=schemas.VirtualMachineSchemaOut)
def update_virtual_machine(request, vm_id: UUID, payload: schemas.VirtualMachineSchemaIn):
    vm = get_object_or_404(models.VirtualMachine, id=vm_id)
    for attr, value in payload.dict().items():
        setattr(vm, attr, value)
    vm.save()
    return vm

@vm_router.delete("/{vm_id}")
def delete_virtual_machine(request, vm_id: UUID):
    vm = get_object_or_404(models.VirtualMachine, id=vm_id)
    vm.delete()
    return {"success": True}
