from ninja import Router
from backend import models, schemas
from backend.dependencies import api_auth
from uuid import UUID

router = Router(tags=["Host"], auth=api_auth)

@router.get(path='/', response=list[schemas.HostSchema], auth=api_auth)
def list_hosts(request):
    return models.Host.objects.all()


# @router.post("/", response=schemas.HostSchema, auth=api_auth, status=201)
# def create_host(request, payload: schemas.HostCreateSchema):
#     host = models.Host.objects.create(**payload.dict())
#     return host

# @router.get("/", response=list(schemas.HostSchema), auth=api_auth)
# def list_hosts(request):
#     return models.Host.objects.all()

# @router.get("/{host_id}", response=schemas.HostSchema, auth=api_auth)
# def get_host(request, host_id: UUID):
#     try:
#         host = models.Host.objects.get(id=host_id)
#     except models.Host.DoesNotExist:
#         return api_auth.error("Host not found", status=404)
#     return host

# @router.put("/{host_id}", response=schemas.HostSchema, auth=api_auth)
# def update_host(request, host_id: UUID, payload: schemas.HostCreateSchema):
#     try:
#         host = models.Host.objects.get(id=host_id)
#     except models.Host.DoesNotExist:
#         return api_auth.error("Host not found", status=404)
#     for attr, value in payload.dict().items():
#         setattr(host, attr, value)
#     host.save()
#     return host

# @router.delete("/{host_id}", auth=api_auth)
# def delete_host(request, host_id: UUID):
#     try:
#         host = models.Host.objects.get(id=host_id)
#     except models.Host.DoesNotExist:
#         return api_auth.error("Host not found", status=404)
#     host.delete()
#     return {"message": "Host deleted successfully"}
