from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# ServiceMesh Router
# ----------------------------
service_mesh_router = Router(tags=["ServiceMesh"], auth=api_auth)

@service_mesh_router.get("/", response=list[schemas.ServiceMeshOutSchema])
def list_service_meshes(request):
    return models.ServiceMesh.objects.all()

@service_mesh_router.get("/{service_mesh_id}", response=schemas.ServiceMeshOutSchema)
def get_service_mesh(request, service_mesh_id: UUID):
    return get_object_or_404(models.ServiceMesh, id=service_mesh_id)

@service_mesh_router.post("/", response=schemas.ServiceMeshOutSchema)
def create_service_mesh(request, payload: schemas.ServiceMeshCreateSchema):
    service_mesh = models.ServiceMesh.objects.create(**payload.dict())
    return service_mesh

@service_mesh_router.put("/{service_mesh_id}", response=schemas.ServiceMeshOutSchema)
def update_service_mesh(request, service_mesh_id: UUID, payload: schemas.ServiceMeshUpdateSchema):
    service_mesh = get_object_or_404(models.ServiceMesh, id=service_mesh_id)
    for attr, value in payload.dict().items():
        setattr(service_mesh, attr, value)
    service_mesh.save()
    return service_mesh

@service_mesh_router.delete("/{service_mesh_id}")
def delete_service_mesh(request, service_mesh_id: UUID):
    service_mesh = get_object_or_404(models.ServiceMesh, id=service_mesh_id)
    service_mesh.delete()
    return {"success": True}
