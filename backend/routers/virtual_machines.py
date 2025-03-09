from fastapi import APIRouter, HTTPException
from backend.models import VirtualMachine
from backend.schemas import VirtualMachineSchema

router = APIRouter()

@router.post("/virtual-machines/", response_model=VirtualMachineSchema)
def create_virtual_machine(vm: VirtualMachineSchema):
    db_vm = VirtualMachine(**vm.dict())
    db_vm.save()
    return db_vm

@router.get("/virtual-machines/{vm_id}", response_model=VirtualMachineSchema)
def read_virtual_machine(vm_id: int):
    vm = VirtualMachine.get(vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="Virtual Machine not found")
    return vm

@router.put("/virtual-machines/{vm_id}", response_model=VirtualMachineSchema)
def update_virtual_machine(vm_id: int, vm: VirtualMachineSchema):
    db_vm = VirtualMachine.get(vm_id)
    if not db_vm:
        raise HTTPException(status_code=404, detail="Virtual Machine not found")
    for key, value in vm.dict().items():
        setattr(db_vm, key, value)
    db_vm.save()
    return db_vm

@router.delete("/virtual-machines/{vm_id}")
def delete_virtual_machine(vm_id: int):
    vm = VirtualMachine.get(vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="Virtual Machine not found")
    vm.delete()
    return {"detail": "Virtual Machine deleted successfully"}