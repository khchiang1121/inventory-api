import pytest

from .base import auth_client


@pytest.mark.django_db
def test_k8s_cluster_and_plugins(auth_client):
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tk", "status": "active"}, format="json"
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "c1",
            "version": "1.28",
            "tenant": tenant["id"],
            "scheduling_mode": "default",
            "status": "active",
        },
        format="json",
    ).data

    plugin = auth_client.post(
        "/api/v1/k8s-cluster-plugins",
        {
            "cluster": cluster["id"],
            "name": "cilium",
            "version": "1.0",
            "status": "active",
        },
        format="json",
    )
    assert plugin.status_code == 201


@pytest.mark.django_db
def test_service_mesh_and_binding(auth_client):
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tm", "status": "active"}, format="json"
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "c2",
            "version": "1.28",
            "tenant": tenant["id"],
            "scheduling_mode": "default",
            "status": "active",
        },
        format="json",
    ).data
    mesh = auth_client.post(
        "/api/v1/service-meshes",
        {"name": "cilium", "type": "cilium", "status": "active"},
        format="json",
    ).data

    binding = auth_client.post(
        "/api/v1/k8s-cluster-service-meshes",
        {"cluster": cluster["id"], "service_mesh": mesh["id"], "role": "primary"},
        format="json",
    )
    assert binding.status_code == 201
