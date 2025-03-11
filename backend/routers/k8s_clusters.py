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
# K8sCluster Router
# ----------------------------
k8s_cluster_router = Router(tags=["K8sCluster"], auth=api_auth)

@k8s_cluster_router.get("/", response=list[schemas.K8sClusterSchemaOut])
def list_k8s_clusters(request):
    return models.K8sCluster.objects.all()

@k8s_cluster_router.get("/{cluster_id}", response=schemas.K8sClusterSchemaOut)
def get_k8s_cluster(request, cluster_id: UUID):
    return get_object_or_404(models.K8sCluster, id=cluster_id)

@k8s_cluster_router.post("/", response=schemas.K8sClusterSchemaOut)
def create_k8s_cluster(request, payload: schemas.K8sClusterSchemaIn):
    cluster = models.K8sCluster.objects.create(**payload.dict())
    return cluster

@k8s_cluster_router.put("/{cluster_id}", response=schemas.K8sClusterSchemaOut)
def update_k8s_cluster(request, cluster_id: UUID, payload: schemas.K8sClusterSchemaIn):
    cluster = get_object_or_404(models.K8sCluster, id=cluster_id)
    for attr, value in payload.dict().items():
        setattr(cluster, attr, value)
    cluster.save()
    return cluster

@k8s_cluster_router.delete("/{cluster_id}")
def delete_k8s_cluster(request, cluster_id: UUID):
    cluster = get_object_or_404(models.K8sCluster, id=cluster_id)
    cluster.delete()
    return {"success": True}

# # from backend.schemas.host import K8sClusterSchema
# from backend.models import K8sCluster

# router = APIRouter()

# @router.post("/k8s_clusters/", response_model=K8sClusterSchema)
# def create_k8s_cluster(cluster: K8sClusterSchema):
#     db_cluster = K8sCluster(**cluster.dict())
#     db_cluster.save()
#     return db_cluster

# @router.get("/k8s_clusters/{cluster_id}", response_model=K8sClusterSchema)
# def read_k8s_cluster(cluster_id: int):
#     cluster = K8sCluster.get(cluster_id)
#     if not cluster:
#         raise HTTPException(status_code=404, detail="Cluster not found")
#     return cluster

# @router.put("/k8s_clusters/{cluster_id}", response_model=K8sClusterSchema)
# def update_k8s_cluster(cluster_id: int, cluster: K8sClusterSchema):
#     db_cluster = K8sCluster.get(cluster_id)
#     if not db_cluster:
#         raise HTTPException(status_code=404, detail="Cluster not found")
#     for key, value in cluster.dict().items():
#         setattr(db_cluster, key, value)
#     db_cluster.save()
#     return db_cluster

# @router.delete("/k8s_clusters/{cluster_id}")
# def delete_k8s_cluster(cluster_id: int):
#     cluster = K8sCluster.get(cluster_id)
#     if not cluster:
#         raise HTTPException(status_code=404, detail="Cluster not found")
#     cluster.delete()
#     return {"detail": "Cluster deleted successfully"}