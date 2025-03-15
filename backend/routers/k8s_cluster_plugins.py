from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# K8sClusterPlugin Router
# ----------------------------
k8s_cluster_plugin_router = Router(tags=["K8sClusterPlugin"], auth=api_auth)

@k8s_cluster_plugin_router.get("/", response=list[schemas.K8sClusterPluginOutSchema])
def list_k8s_cluster_plugins(request):
    return models.K8sClusterPlugin.objects.all()

@k8s_cluster_plugin_router.get("/{plugin_id}", response=schemas.K8sClusterPluginOutSchema)
def get_k8s_cluster_plugin(request, plugin_id: UUID):
    return get_object_or_404(models.K8sClusterPlugin, id=plugin_id)

@k8s_cluster_plugin_router.post("/", response=schemas.K8sClusterPluginOutSchema)
def create_k8s_cluster_plugin(request, payload: schemas.K8sClusterPluginCreateSchema):
    plugin = models.K8sClusterPlugin.objects.create(**payload.dict())
    return plugin

@k8s_cluster_plugin_router.put("/{plugin_id}", response=schemas.K8sClusterPluginOutSchema)
def update_k8s_cluster_plugin(request, plugin_id: UUID, payload: schemas.K8sClusterPluginUpdateSchema):
    plugin = get_object_or_404(models.K8sClusterPlugin, id=plugin_id)
    for attr, value in payload.dict().items():
        setattr(plugin, attr, value)
    plugin.save()
    return plugin

@k8s_cluster_plugin_router.delete("/{plugin_id}")
def delete_k8s_cluster_plugin(request, plugin_id: UUID):
    plugin = get_object_or_404(models.K8sClusterPlugin, id=plugin_id)
    plugin.delete()
    return {"success": True}
