import pytest

# ============================================================================
# K8S CLUSTER TESTS
# ============================================================================


@pytest.mark.django_db
def test_k8s_cluster_create(auth_client):
    """Test creating a K8s cluster"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "k8s-tenant-create", "status": "active"},
        format="json",
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-1", "description": "", "status": "active"},
        format="json",
    ).data
    # minimal scheduling strategy and user required
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "default-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-owner",
            "password": "Passw0rd!",
            "email": "k8s-owner@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-create",
        "version": "1.28",
        "tenant": tenant["id"],
        "region": region["id"],
        "scheduling_strategy": strategy["id"],
        "description": "",
        "user": user["id"],
        "status": "active",
    }
    r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "cluster-create"
    assert r.data["version"] == "1.28"


@pytest.mark.django_db
def test_k8s_cluster_list(auth_client):
    """Test listing K8s clusters"""
    r = auth_client.get("/api/v1/k8s-clusters")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_k8s_cluster_retrieve(auth_client):
    """Test retrieving a specific K8s cluster"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "k8s-tenant-retrieve", "status": "active"},
        format="json",
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-2", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "retrieve-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-retrieve",
            "password": "Passw0rd!",
            "email": "k8s-retrieve@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-retrieve",
        "version": "1.27",
        "tenant": tenant["id"],
        "region": region["id"],
        "scheduling_strategy": strategy["id"],
        "description": "",
        "user": user["id"],
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    cluster_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["name"] == "cluster-retrieve"
    assert r.data["version"] == "1.27"


@pytest.mark.django_db
def test_k8s_cluster_update_put(auth_client):
    """Test updating a K8s cluster with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "k8s-tenant-put", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "put-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-put",
            "password": "Passw0rd!",
            "email": "k8s-put@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-put",
        "version": "1.28",
        "tenant": tenant["id"],
        "region": region["id"],
        "scheduling_strategy": strategy["id"],
        "description": "",
        "user": user["id"],
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    cluster_id = create_r.data["id"]

    put_data = {
        "name": "cluster-put-updated",
        "version": "1.29",
        "tenant": tenant["id"],
        "scheduling_mode": "balanced",
        "status": "active",
    }
    r = auth_client.put(f"/api/v1/k8s-clusters/{cluster_id}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "cluster-put-updated"
    assert r.data["version"] == "1.29"
    assert r.data["scheduling_mode"] == "balanced"

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["name"] == "cluster-put-updated"
    assert r.data["version"] == "1.29"


@pytest.mark.django_db
def test_k8s_cluster_update_patch(auth_client):
    """Test updating a K8s cluster with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "k8s-tenant-patch", "status": "active"},
        format="json",
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-4", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "patch-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-patch",
            "password": "Passw0rd!",
            "email": "k8s-patch@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-patch",
        "version": "1.28",
        "tenant": tenant["id"],
        "region": region["id"],
        "scheduling_strategy": strategy["id"],
        "description": "",
        "user": user["id"],
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    cluster_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/k8s-clusters/{cluster_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "cluster-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "cluster-patch"


@pytest.mark.django_db
def test_k8s_cluster_delete(auth_client):
    """Test deleting a K8s cluster"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "k8s-tenant-delete", "status": "active"},
        format="json",
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-5", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "delete-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-delete",
            "password": "Passw0rd!",
            "email": "k8s-delete@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-delete",
        "version": "1.28",
        "tenant": tenant["id"],
        "region": region["id"],
        "scheduling_strategy": strategy["id"],
        "description": "",
        "user": user["id"],
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json")
    cluster_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/k8s-clusters/{cluster_id}")
    assert r.status_code == 404


# ============================================================================
# K8S CLUSTER PLUGINS TESTS
# ============================================================================


@pytest.mark.django_db
def test_k8s_cluster_plugins_create(auth_client):
    """Test creating K8s cluster plugins"""
    # For plugin tests and service mesh associations below, ensure a cluster exists with required fields
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "plugin-tenant-create", "status": "active"},
        format="json",
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-k8s-plugins", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "plugins-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-plugins",
            "password": "Passw0rd!",
            "email": "k8s-plugins@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-for-plugins",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    plugin_data = {
        "cluster": cluster["id"],
        "name": "ingress-nginx",
        "version": "1.0.0",
        "status": "active",
    }
    r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "ingress-nginx"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_k8s_cluster_plugins_list(auth_client):
    """Test listing K8s cluster plugins"""
    r = auth_client.get("/api/v1/k8s-cluster-plugins")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_k8s_cluster_plugins_retrieve(auth_client):
    """Test retrieving a specific K8s cluster plugin"""
    # Ensure cluster has required fields
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "plugin-tenant-retrieve2", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-plugins-retrieve", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "plugins-retrieve-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-plugins-retrieve",
            "password": "Passw0rd!",
            "email": "k8s-plugins-retrieve@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-for-retrieve",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    plugin_data = {
        "cluster": cluster["id"],
        "name": "cert-manager",
        "version": "1.12.0",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["name"] == "cert-manager"
    assert r.data["version"] == "1.12.0"


@pytest.mark.django_db
def test_k8s_cluster_plugins_update_put(auth_client):
    """Test updating K8s cluster plugins with PUT"""
    # Recreate minimal cluster for put using required fields
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "plugin-tenant-put3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-plugins-put3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "plugins-put3-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-plugins-put3",
            "password": "Passw0rd!",
            "email": "k8s-plugins-put3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-for-put",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    plugin_data = {
        "cluster": cluster["id"],
        "name": "prometheus",
        "version": "2.40.0",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    plugin_id = create_r.data["id"]

    put_data = {
        "cluster": cluster["id"],
        "name": "prometheus-updated",
        "version": "2.45.0",
        "status": "inactive",
    }
    r = auth_client.put(f"/api/v1/k8s-cluster-plugins/{plugin_id}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "prometheus-updated"
    assert r.data["version"] == "2.45.0"
    assert str(r.data["cluster"]) == str(cluster["id"]) or r.data["cluster"] == cluster["id"]

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["name"] == "prometheus-updated"
    assert r.data["version"] == "2.45.0"


@pytest.mark.django_db
def test_k8s_cluster_plugins_update_patch(auth_client):
    """Test updating K8s cluster plugins with PATCH"""
    # Recreate minimal cluster for patch
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "plugin-tenant-patch3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-plugins-patch3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "plugins-patch3-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-plugins-patch3",
            "password": "Passw0rd!",
            "email": "k8s-plugins-patch3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-for-patch",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    plugin_data = {
        "cluster": cluster["id"],
        "name": "grafana",
        "version": "9.0.0",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/k8s-cluster-plugins/{plugin_id}",
        {"status": "inactive"},
        format="json",
    )
    assert r.status_code == 200
    assert str(r.data["cluster"]) == str(cluster["id"]) or r.data["cluster"] == cluster["id"]
    assert r.data["name"] == "grafana"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code == 200
    assert (
        str(r.data.get("cluster")) == str(cluster["id"]) or r.data.get("cluster") == cluster["id"]
    )
    assert r.data["name"] == "grafana"


@pytest.mark.django_db
def test_k8s_cluster_plugins_delete(auth_client):
    """Test deleting K8s cluster plugins"""
    # Recreate minimal cluster for delete
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "plugin-tenant-delete3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-plugins-delete3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "plugins-delete3-strat",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-plugins-delete3",
            "password": "Passw0rd!",
            "email": "k8s-plugins-delete3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-for-delete",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    plugin_data = {
        "cluster": cluster["id"],
        "name": "argocd",
        "version": "2.8.0",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-plugins", plugin_data, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/k8s-cluster-plugins/{plugin_id}")
    assert r.status_code == 404


# ============================================================================
# SERVICE MESH TESTS
# ============================================================================


@pytest.mark.django_db
def test_service_mesh_create(auth_client):
    """Test creating a service mesh"""
    payload = {
        "name": "istio-create",
        "type": "istio",
        "status": "active",
    }
    r = auth_client.post("/api/v1/service-meshes", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "istio-create"
    assert r.data["type"] == "istio"


@pytest.mark.django_db
def test_service_mesh_list(auth_client):
    """Test listing service meshes"""
    r = auth_client.get("/api/v1/service-meshes")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_service_mesh_retrieve(auth_client):
    """Test retrieving a specific service mesh"""
    payload = {
        "name": "mesh-retrieve",
        "type": "cilium",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/service-meshes", payload, format="json")
    mesh_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code == 200
    assert r.data["name"] == "mesh-retrieve"
    assert r.data["type"] == "cilium"


@pytest.mark.django_db
def test_service_mesh_update_put(auth_client):
    """Test updating a service mesh with PUT"""
    payload = {
        "name": "mesh-put",
        "type": "istio",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/service-meshes", payload, format="json")
    mesh_id = create_r.data["id"]

    put_payload = {
        "name": "mesh-put-updated",
        "type": "istio",
        "status": "inactive",
    }
    r = auth_client.put(f"/api/v1/service-meshes/{mesh_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "mesh-put-updated"
    assert r.data["status"] == "inactive"

    # Verify in database
    r = auth_client.get(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code == 200
    assert r.data["name"] == "mesh-put-updated"
    assert r.data["status"] == "inactive"


@pytest.mark.django_db
def test_service_mesh_update_patch(auth_client):
    """Test updating a service mesh with PATCH"""
    payload = {
        "name": "mesh-patch",
        "type": "istio",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/service-meshes", payload, format="json")
    mesh_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/service-meshes/{mesh_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "mesh-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code == 200
    assert r.data["name"] == "mesh-patch"
    assert r.data["status"] == "inactive"


@pytest.mark.django_db
def test_service_mesh_delete(auth_client):
    """Test deleting a service mesh"""
    payload = {
        "name": "mesh-delete",
        "type": "istio",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/service-meshes", payload, format="json")
    mesh_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/service-meshes/{mesh_id}")
    assert r.status_code == 404


# ============================================================================
# K8S CLUSTER SERVICE MESH BINDING TESTS
# ============================================================================


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_create(auth_client):
    """Test creating K8s cluster service mesh binding"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "binding-tenant", "status": "active"}, format="json"
    ).data

    cluster_data = {
        "name": "cluster-binding",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    mesh_data = {
        "name": "istio-binding",
        "version": "1.18.0",
        "type": "istio",
        "status": "active",
    }
    mesh = auth_client.post("/api/v1/service-meshes", mesh_data, format="json").data

    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    r = auth_client.post("/api/v1/k8s-cluster-service-meshes", binding_data, format="json")
    assert r.status_code == 201
    assert r.data["role"] == "primary"


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_list(auth_client):
    """Test listing K8s cluster service mesh bindings"""
    r = auth_client.get("/api/v1/k8s-cluster-service-meshes")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_retrieve(auth_client):
    """Test retrieving a specific K8s cluster service mesh binding"""
    # For mesh binding retrieve minimal cluster
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "binding-tenant-retrieve-3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-binding-retrieve-3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "binding-strat-retrieve-3",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-binding-retrieve-3",
            "password": "Passw0rd!",
            "email": "k8s-binding-retrieve-3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-binding-retrieve",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-service-meshes", binding_data, format="json")
    binding_id = (
        str(create_r.data["id"])
        if not isinstance(create_r.data["id"], str)
        else create_r.data["id"]
    )

    r = auth_client.get(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code == 200
    assert r.data.get("role") in ("primary", "secondary")


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_update_put(auth_client):
    """Test updating K8s cluster service mesh binding with PUT"""
    # For mesh binding put minimal cluster
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "binding-tenant-put-3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-binding-put-3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "binding-strat-put-3",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-binding-put-3",
            "password": "Passw0rd!",
            "email": "k8s-binding-put-3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-binding-put",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-service-meshes", binding_data, format="json")
    binding_id = (
        str(create_r.data["id"])
        if not isinstance(create_r.data["id"], str)
        else create_r.data["id"]
    )

    put_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "secondary",
    }
    r = auth_client.put(
        f"/api/v1/k8s-cluster-service-meshes/{binding_id}",
        put_data,
        format="json",
    )
    assert r.status_code == 200
    assert (
        str(r.data.get("cluster")) == str(cluster["id"]) or r.data.get("cluster") == cluster["id"]
    )

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code == 200
    assert (
        str(r.data.get("cluster")) == str(cluster["id"]) or r.data.get("cluster") == cluster["id"]
    )


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_update_patch(auth_client):
    """Test updating K8s cluster service mesh binding with PATCH"""
    # For mesh binding patch minimal cluster
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "binding-tenant-patch-3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-binding-patch-3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "binding-strat-patch-3",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-binding-patch-3",
            "password": "Passw0rd!",
            "email": "k8s-binding-patch-3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-binding-patch",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-service-meshes", binding_data, format="json")
    binding_id = (
        str(create_r.data["id"])
        if not isinstance(create_r.data["id"], str)
        else create_r.data["id"]
    )

    r = auth_client.patch(
        f"/api/v1/k8s-cluster-service-meshes/{binding_id}",
        {"status": "inactive"},
        format="json",
    )
    assert r.status_code == 200
    assert (
        str(r.data.get("cluster")) == str(cluster["id"]) or r.data.get("cluster") == cluster["id"]
    )

    # Verify in database
    r = auth_client.get(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code == 200
    assert (
        str(r.data.get("cluster")) == str(cluster["id"]) or r.data.get("cluster") == cluster["id"]
    )


@pytest.mark.django_db
def test_k8s_cluster_service_mesh_binding_delete(auth_client):
    """Test deleting K8s cluster service mesh binding"""
    # For mesh binding delete minimal cluster
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "binding-tenant-delete-3", "status": "active"}, format="json"
    ).data
    region = auth_client.post(
        "/api/v1/regions",
        {"name": "us-binding-delete-3", "description": "", "status": "active"},
        format="json",
    ).data
    strategy = auth_client.post(
        "/api/v1/scheduling-strategies",
        {
            "name": "binding-strat-delete-3",
            "description": "",
            "mode": "default",
            "priority": 0,
            "tenant": tenant["id"],
            "status": "active",
            "available_group": [],
        },
        format="json",
    ).data
    user = auth_client.post(
        "/api/v1/users",
        {
            "username": "k8s-binding-delete-3",
            "password": "Passw0rd!",
            "email": "k8s-binding-delete-3@example.com",
            "account": "test",
            "status": "active",
        },
        format="json",
    ).data
    cluster = auth_client.post(
        "/api/v1/k8s-clusters",
        {
            "name": "cluster-binding-delete",
            "version": "1.28",
            "tenant": tenant["id"],
            "region": region["id"],
            "scheduling_strategy": strategy["id"],
            "description": "",
            "user": user["id"],
            "status": "active",
        },
        format="json",
    ).data

    binding_data = {
        "cluster": cluster["id"],
        "service_mesh": mesh["id"],
        "role": "primary",
    }
    create_r = auth_client.post("/api/v1/k8s-cluster-service-meshes", binding_data, format="json")
    binding_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/k8s-cluster-service-meshes/{binding_id}")
    assert r.status_code == 404


# ============================================================================
# BASTION CLUSTER ASSOCIATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_bastion_cluster_association_create(auth_client):
    """Test creating bastion cluster association"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "bastion-tenant", "status": "active"}, format="json"
    ).data

    cluster_data = {
        "name": "cluster-bastion",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    # Create VM spec first
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm_data = {
        "name": "bastion-vm",
        "type": "management",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm = auth_client.post("/api/v1/virtual-machines", vm_data, format="json").data

    association_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    r = auth_client.post("/api/v1/bastion-cluster-associations", association_data, format="json")
    assert r.status_code == 201
    assert str(r.data["k8s_cluster"]) == str(cluster["id"])
    assert str(r.data["bastion"]) == str(vm["id"])


@pytest.mark.django_db
def test_bastion_cluster_association_list(auth_client):
    """Test listing bastion cluster associations"""
    r = auth_client.get("/api/v1/bastion-cluster-associations")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_bastion_cluster_association_retrieve(auth_client):
    """Test retrieving a specific bastion cluster association"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "bastion-tenant-retrieve", "status": "active"},
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-bastion-retrieve",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    # Create VM spec first
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec-retrieve",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm_data = {
        "name": "bastion-vm-retrieve",
        "type": "management",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm = auth_client.post("/api/v1/virtual-machines", vm_data, format="json").data

    association_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    create_r = auth_client.post(
        "/api/v1/bastion-cluster-associations", association_data, format="json"
    )
    association_id = (
        str(create_r.data["id"])
        if not isinstance(create_r.data["id"], str)
        else create_r.data["id"]
    )

    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{association_id}")
    assert r.status_code == 200
    assert str(r.data["k8s_cluster"]) == str(cluster["id"])
    assert str(r.data["bastion"]) == str(vm["id"])


@pytest.mark.django_db
def test_bastion_cluster_association_update_put(auth_client):
    """Test updating bastion cluster association with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "bastion-tenant-put", "status": "active"},
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-bastion-put",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    # Create VM spec first
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec-put",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm_data = {
        "name": "bastion-vm-put",
        "type": "management",
        "status": "active",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm = auth_client.post("/api/v1/virtual-machines", vm_data, format="json").data

    association_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    create_r = auth_client.post(
        "/api/v1/bastion-cluster-associations", association_data, format="json"
    )
    association_id = (
        str(create_r.data["id"])
        if not isinstance(create_r.data["id"], str)
        else create_r.data["id"]
    )

    put_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    r = auth_client.put(
        f"/api/v1/bastion-cluster-associations/{association_id}",
        put_data,
        format="json",
    )
    assert r.status_code == 200
    assert (
        str(r.data.get("k8s_cluster")) == str(cluster["id"])
        or r.data.get("k8s_cluster") == cluster["id"]
    )
    assert str(r.data.get("bastion")) == str(vm["id"]) or r.data.get("bastion") == vm["id"]

    # Verify in database
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{association_id}")
    assert r.status_code == 200
    assert str(r.data["k8s_cluster"]) == str(cluster["id"])
    assert str(r.data["bastion"]) == str(vm["id"])


@pytest.mark.django_db
def test_bastion_cluster_association_update_patch(auth_client):
    """Test updating bastion cluster association with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "bastion-tenant-patch", "status": "active"},
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-bastion-patch",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    # Create VM spec first
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec-patch",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm_data = {
        "name": "bastion-vm-patch",
        "type": "management",
        "status": "active",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm = auth_client.post("/api/v1/virtual-machines", vm_data, format="json").data

    association_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    create_r = auth_client.post(
        "/api/v1/bastion-cluster-associations", association_data, format="json"
    )
    association_id = create_r.data["id"]

    # Create a second VM to switch to
    vm2_data = {
        "name": "bastion-vm2-patch",
        "type": "management",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm2 = auth_client.post("/api/v1/virtual-machines", vm2_data, format="json").data

    r = auth_client.patch(
        f"/api/v1/bastion-cluster-associations/{association_id}",
        {"bastion": vm2["id"]},
        format="json",
    )
    assert r.status_code == 200
    assert str(r.data["k8s_cluster"]) == str(cluster["id"])
    assert str(r.data["bastion"]) == str(vm2["id"])  # Should be updated

    # Verify in database
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{association_id}")
    assert r.status_code == 200
    assert str(r.data["k8s_cluster"]) == str(cluster["id"])
    assert str(r.data["bastion"]) == str(vm2["id"])


@pytest.mark.django_db
def test_bastion_cluster_association_delete(auth_client):
    """Test deleting bastion cluster association"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "bastion-tenant-delete", "status": "active"},
        format="json",
    ).data

    cluster_data = {
        "name": "cluster-bastion-delete",
        "version": "1.28",
        "tenant": tenant["id"],
        "scheduling_mode": "default",
        "status": "active",
    }
    cluster = auth_client.post("/api/v1/k8s-clusters", cluster_data, format="json").data

    # Create VM spec first
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec-delete",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm_data = {
        "name": "bastion-vm-delete",
        "type": "management",
        "status": "active",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    vm = auth_client.post("/api/v1/virtual-machines", vm_data, format="json").data

    association_data = {
        "k8s_cluster": cluster["id"],
        "bastion": vm["id"],
    }
    create_r = auth_client.post(
        "/api/v1/bastion-cluster-associations", association_data, format="json"
    )
    association_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/bastion-cluster-associations/{association_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/bastion-cluster-associations/{association_id}")
    assert r.status_code == 404
