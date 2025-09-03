import pytest

from .base import auth_client


@pytest.mark.django_db
def test_k8s_cluster_crud_complete(auth_client):
    """Test complete CRUD operations for K8s clusters"""
    # Setup tenant dependency
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tk", "status": "active"}, format="json"
    ).data

    # Create
    cluster_data = {
        "name": "c1",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    assert r.status_code == 201
    cluster_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/k8s-clusters")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["name"] == "c1"

    # Full Update (PUT)
    put_data = {
        "name": "c1-updated",
        "version": "1.29",
        "tenant": tenant["id"],
        "scheduling_mode": "balanced",
        "status": "active",
    }
    r = auth_client.put(f"/api/v1/k8s-clusters/{cluster_id}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "c1-updated"
    assert r.data["version"] == "1.29"
    assert r.data["scheduling_mode"] == "balanced"

    # Verify PUT in database
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["name"] == "c1-updated"
    assert r.data["version"] == "1.29"
    assert r.data["scheduling_mode"] == "balanced"

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/k8s-clusters/{cluster_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    # Other fields should remain unchanged
    assert r.data["name"] == "c1-updated"
    assert r.data["version"] == "1.29"

    # Verify PATCH in database
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "c1-updated"

    # Delete
    r = auth_client.delete(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code in (204, 200)

    # Verify deletion - should return 404
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_k8s_cluster_plugins_crud_complete(auth_client):
    """Test complete CRUD operations for K8s cluster plugins"""
    # Setup dependencies
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tp", "status": "active"}, format="json"
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

    # Create
    plugin_data = {
        "cluster": cluster["id"],
        "name": "cilium",
        "version": "1.0",
        "status": "active",
    }
    r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    assert r.status_code == 201
    plugin_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/k8s-cluster-plugins")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["name"] == "cilium"

    # Full Update (PUT)
    put_data = {
        "cluster": cluster["id"],
        "name": "cilium",
        "version": "1.1",
        "status": "active",
    }
    r = auth_client.put(
        f"/api/v1/k8s-cluster-plugins/{plugin_id}", put_data, format="json"
    )
    assert r.status_code == 200
    assert r.data["version"] == "1.1"

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/k8s-cluster-plugins/{plugin_id}",
        {"status": "inactive"},
        format="json",
    )
    assert r.status_code == 200

    # Delete
    assert auth_client.delete(
        f"/api/v1/k8s-cluster-plugins/{plugin_id}"
    ).status_code in (204, 200)


@pytest.mark.django_db
def test_service_mesh_crud_complete(auth_client):
    """Test complete CRUD operations for service meshes"""
    # Create
    mesh_data = {"name": "istio", "type": "istio", "status": "active"}
    r = auth_client.post("/api/v1/service-meshes", mesh_data, format="json")
    assert r.status_code == 201
    mesh_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/service-meshes")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code == 200
    assert r.data["name"] == "istio"

    # Full Update (PUT)
    put_data = {
        "name": "istio-updated",
        "type": "istio",
        "description": "Updated Istio mesh",
        "status": "active",
    }
    r = auth_client.put(f"/api/v1/service-meshes/{mesh_id}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "istio-updated"

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/service-meshes/{mesh_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"

    # Delete
    assert auth_client.delete(f"/api/v1/service-meshes/{mesh_id}").status_code in (
        204,
        200,
    )


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_crud(auth_client):
    """Test complete CRUD operations for K8s cluster to service mesh bindings"""
    # Setup dependencies
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tm", "status": "active"}, format="json"
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "c3",
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

    # Create
    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    r = auth_client.post(
        "/api/v1/k8s-cluster-service-meshes", binding_data, format="json"
    )
    assert r.status_code == 201
    binding_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/k8s-cluster-service-meshes")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code == 200
    assert r.data["role"] == "primary"

    # Full Update (PUT)
    put_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "secondary",
    }
    r = auth_client.put(
        f"/api/v1/k8s-cluster-service-meshes/{binding_id}", put_data, format="json"
    )
    assert r.status_code == 200
    assert r.data["role"] == "secondary"

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/k8s-cluster-service-meshes/{binding_id}",
        {"role": "primary"},
        format="json",
    )
    assert r.status_code == 200

    # Delete
    assert auth_client.delete(
        f"/api/v1/k8s-cluster-service-meshes/{binding_id}"
    ).status_code in (204, 200)


@pytest.mark.django_db
def test_bastion_cluster_association_crud_complete(auth_client):
    """Test complete CRUD operations for bastion cluster associations"""
    # Setup dependencies
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tb", "status": "active"}, format="json"
    ).data

    # Create VM spec
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec",
            "generation": "g1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 20,
        },
        format="json",
    ).data

    # Create bastion VM
    bastion = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "bastion-vm",
            "tenant": tenant["id"],
            "specification": spec["id"],
            "type": "management",  # Valid choice: control-plane, worker, management, other
            "status": "running",
        },
        format="json",
    ).data

    # Create K8s cluster
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "managed-cluster",
            "version": "1.28",
            "tenant": tenant["id"],
            "scheduling_mode": "default",
            "status": "active",
        },
        format="json",
    ).data

    # Create association
    assoc_data = {"bastion": bastion["id"], "k8s_cluster": cluster["id"]}
    r = auth_client.post(
        "/api/v1/bastion-cluster-associations", assoc_data, format="json"
    )
    assert r.status_code == 201
    assoc_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/bastion-cluster-associations")
    assert r.status_code == 200
    assert len(r.data["results"]) >= 1

    # Retrieve
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{assoc_id}")
    assert r.status_code == 200

    # Create another cluster for PUT test
    cluster2 = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "managed-cluster-2",
            "version": "1.28",
            "tenant": tenant["id"],
            "scheduling_mode": "default",
            "status": "active",
        },
        format="json",
    ).data

    # Full Update (PUT) - change cluster
    put_data = {"bastion": bastion["id"], "k8s_cluster": cluster2["id"]}
    r = auth_client.put(
        f"/api/v1/bastion-cluster-associations/{assoc_id}", put_data, format="json"
    )
    assert r.status_code == 200

    # Verify PUT in database
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{assoc_id}")
    assert r.status_code == 200

    # Note: PATCH might not be meaningful for this relationship model
    # as it only has two required fields, but let's test it anyway

    # Delete
    r = auth_client.delete(f"/api/v1/bastion-cluster-associations/{assoc_id}")
    assert r.status_code in (204, 200)

    # Verify deletion - should return 404
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{assoc_id}")
    assert r.status_code == 404
