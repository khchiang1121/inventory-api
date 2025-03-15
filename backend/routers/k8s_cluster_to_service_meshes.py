from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# K8sClusterToServiceMesh Router
# ----------------------------
k8s_cluster_to_service_mesh_router = Router(tags=["K8sClusterToServiceMesh"], auth=api_auth)

@k8s_cluster_to_service_mesh_router.get("/", response=list[schemas.K8sClusterToServiceMeshOutSchema])
def list_k8s_cluster_to_service_meshes(request):
    return models.K8sClusterToServiceMesh.objects.all()

@k8s_cluster_to_service_mesh_router.get("/{association_id}", response=schemas.K8sClusterToServiceMeshOutSchema)
def get_k8s_cluster_to_service_mesh(request, association_id: UUID):
    return get_object_or_404(models.K8sClusterToServiceMesh, id=association_id)

@k8s_cluster_to_service_mesh_router.post("/", response=schemas.K8sClusterToServiceMeshOutSchema)
def create_k8s_cluster_to_service_mesh(request, payload: schemas.K8sClusterToServiceMeshCreateSchema):
    association = models.K8sClusterToServiceMesh.objects.create(**payload.dict())
    return association

@k8s_cluster_to_service_mesh_router.put("/{association_id}", response=schemas.K8sClusterToServiceMeshOutSchema)
def update_k8s_cluster_to_service_mesh(request, association_id: UUID, payload: schemas.K8sClusterToServiceMeshUpdateSchema):
    association = get_object_or_404(models.K8sClusterToServiceMesh, id=association_id)
    for attr, value in payload.dict().items():
        setattr(association, attr, value)
    association.save()
    return association

@k8s_cluster_to_service_mesh_router.delete("/{association_id}")
def delete_k8s_cluster_to_service_mesh(request, association_id: UUID):
    association = get_object_or_404(models.K8sClusterToServiceMesh, id=association_id)
    association.delete()
    return {"success": True}
