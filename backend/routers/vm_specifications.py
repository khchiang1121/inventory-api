from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Define the Pydantic model for VM Specifications
class VMSpecification(BaseModel):
    id: int
    name: str
    cpu: int
    memory: int
    disk_size: int

# In-memory storage for VM Specifications
vm_specifications_db = []

router = APIRouter()

@router.post("/vm-specifications/", response_model=VMSpecification)
def create_vm_specification(vm_spec: VMSpecification):
    vm_specifications_db.append(vm_spec)
    return vm_spec

@router.get("/vm-specifications/", response_model=List[VMSpecification])
def get_vm_specifications():
    return vm_specifications_db

@router.get("/vm-specifications/{vm_id}", response_model=VMSpecification)
def get_vm_specification(vm_id: int):
    for vm in vm_specifications_db:
        if vm.id == vm_id:
            return vm
    raise HTTPException(status_code=404, detail="VM Specification not found")

@router.put("/vm-specifications/{vm_id}", response_model=VMSpecification)
def update_vm_specification(vm_id: int, vm_spec: VMSpecification):
    for index, vm in enumerate(vm_specifications_db):
        if vm.id == vm_id:
            vm_specifications_db[index] = vm_spec
            return vm_spec
    raise HTTPException(status_code=404, detail="VM Specification not found")

@router.delete("/vm-specifications/{vm_id}", response_model=VMSpecification)
def delete_vm_specification(vm_id: int):
    for index, vm in enumerate(vm_specifications_db):
        if vm.id == vm_id:
            return vm_specifications_db.pop(index)
    raise HTTPException(status_code=404, detail="VM Specification not found")