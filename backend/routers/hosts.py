from backend import schemas
from ninja import Router
from backend import models
from backend.dependencies import api_auth
from uuid import UUID
from django.shortcuts import get_object_or_404

host_router = Router(tags=["Host"], auth=api_auth)

@host_router.get("/", response=list[schemas.HostSchemaOut], summary='取得s文章列表')
def list_hosts(request):
    """
    取得文章列表
    """
    return models.Host.objects.all()

@host_router.get("/{host_id}", response=schemas.HostSchemaOut)
def get_host(request, host_id: UUID):
    host = get_object_or_404(models.Host, id=host_id)
    return host

@host_router.post("/", response=schemas.HostSchemaOut)
def create_host(request, payload: schemas.HostSchemaIn):
    host = models.Host.objects.create(**payload.dict())
    return host

@host_router.put("/{host_id}", response=schemas.HostSchemaOut)
def update_host(request, host_id: UUID, payload: schemas.HostSchemaIn):
    host = get_object_or_404(models.Host, id=host_id)
    for attr, value in payload.dict().items():
        setattr(host, attr, value)
    host.save()
    return host

@host_router.delete("/{host_id}")
def delete_host(request, host_id: UUID):
    host = get_object_or_404(models.Host, id=host_id)
    host.delete()
    return {"success": True}
