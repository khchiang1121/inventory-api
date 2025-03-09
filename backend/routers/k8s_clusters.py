from fastapi import APIRouter, HTTPException
from backend.schemas import K8sClusterSchema
from backend.models import K8sCluster

router = APIRouter()

@router.post("/k8s_clusters/", response_model=K8sClusterSchema)
def create_k8s_cluster(cluster: K8sClusterSchema):
    db_cluster = K8sCluster(**cluster.dict())
    db_cluster.save()
    return db_cluster

@router.get("/k8s_clusters/{cluster_id}", response_model=K8sClusterSchema)
def read_k8s_cluster(cluster_id: int):
    cluster = K8sCluster.get(cluster_id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster

@router.put("/k8s_clusters/{cluster_id}", response_model=K8sClusterSchema)
def update_k8s_cluster(cluster_id: int, cluster: K8sClusterSchema):
    db_cluster = K8sCluster.get(cluster_id)
    if not db_cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    for key, value in cluster.dict().items():
        setattr(db_cluster, key, value)
    db_cluster.save()
    return db_cluster

@router.delete("/k8s_clusters/{cluster_id}")
def delete_k8s_cluster(cluster_id: int):
    cluster = K8sCluster.get(cluster_id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    cluster.delete()
    return {"detail": "Cluster deleted successfully"}