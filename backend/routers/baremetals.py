import time
from backend import schemas
from ninja import Router
from backend import models
from backend.dependencies import api_auth
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.db.models import Sum

baremetal_router = Router(tags=["Baremetal"], auth=api_auth)

@baremetal_router.get("/", response=list[schemas.BaremetalOutSchema], summary='取得實體機列表')
def list_hosts(request):
    """
    取得實體機列表
    """
    return models.Baremetal.objects.all()

@baremetal_router.get("/{host_id}", response=schemas.BaremetalOutSchema)
def get_host(request, host_id: UUID):
    host = get_object_or_404(models.Baremetal, id=host_id)
    return host

@baremetal_router.post("/", response=schemas.BaremetalOutSchema)
def create_host(request, payload: schemas.BaremetalCreateSchema):
    host = models.Baremetal.objects.create(**payload.dict())
    return host

@baremetal_router.put("/{host_id}", response=schemas.BaremetalOutSchema)
def update_host(request, host_id: UUID, payload: schemas.BaremetalUpdateSchema):
    host = get_object_or_404(models.Baremetal, id=host_id)
    for attr, value in payload.dict().items():
        setattr(host, attr, value)
    host.save()
    return host

@baremetal_router.delete("/{host_id}")
def delete_host(request, host_id: UUID):
    host = get_object_or_404(models.Baremetal, id=host_id)
    host.delete()
    return {"success": True}

# @baremetal_router.get("/{host_id}/usage", response=schemas.BaremetalResourceSchemaOut)
# def get_host_usage(request, host_id: str):
#     """ 查詢特定實體機的資源使用狀況 """
#     host = get_object_or_404(models.Baremetal, id=host_id)
    
#     # 計算該 Baremetal 上所有 VM 佔用的資源
#     vm_resources = models.VirtualMachine.objects.filter(host=host).aggregate(
#         total_cpu=Sum("specification__required_cpu"),
#         total_memory=Sum("specification__required_memory"),
#         total_storage=Sum("specification__required_storage")
#     )
    
#     return {
#         "id": str(host.id),
#         "name": host.name,
#         "total_cpu": host.total_cpu,
#         "available_cpu": host.available_cpu,
#         "used_cpu": vm_resources["total_cpu"] or 0,
#         "total_memory": host.total_memory,
#         "available_memory": host.available_memory,
#         "used_memory": vm_resources["total_memory"] or 0,
#         "total_storage": host.total_storage,
#         "available_storage": host.available_storage,
#         "used_storage": vm_resources["total_storage"] or 0
#     }