import pytest

from .base import auth_client

# ============================================================================
# VIRTUAL MACHINE TESTS
# ============================================================================


@pytest.mark.django_db
def test_virtual_machine_create(auth_client):
    """Test creating a virtual machine"""
    # Setup dependencies
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "vm-tenant-create", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-create",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    payload = {
        "name": "vm-create",
        "type": "worker",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "vm-create"
    assert r.data["type"] == "worker"
    assert r.data["status"] == "running"


@pytest.mark.django_db
def test_virtual_machine_list(auth_client):
    """Test listing virtual machines"""
    r = auth_client.get("/api/v1/virtual-machines")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_virtual_machine_retrieve(auth_client):
    """Test retrieving a specific virtual machine"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "vm-tenant-retrieve", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-retrieve",
            "generation": "gen1",
            "required_cpu": 4,
            "required_memory": 8,
            "required_storage": 100,
        },
        format="json",
    ).data

    payload = {
        "name": "vm-retrieve",
        "type": "control-plane",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    create_r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    vm_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/virtual-machines/{vm_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vm-retrieve"
    assert r.data["type"] == "control-plane"


@pytest.mark.django_db
def test_virtual_machine_update_put(auth_client):
    """Test updating a virtual machine with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "vm-tenant-put", "status": "active"}, format="json"
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-put",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    spec2 = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-put-2",
            "generation": "gen2",
            "required_cpu": 4,
            "required_memory": 8,
            "required_storage": 100,
        },
        format="json",
    ).data

    payload = {
        "name": "vm-put",
        "type": "management",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    create_r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    vm_id = create_r.data["id"]

    put_payload = {
        "name": "vm-put-updated",
        "type": "other",
        "status": "stopped",
        "tenant": tenant["id"],
        "specification": spec2["id"],
    }
    r = auth_client.put(f"/api/v1/virtual-machines/{vm_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "vm-put-updated"
    assert r.data["type"] == "other"
    assert r.data["status"] == "stopped"

    # Verify in database
    r = auth_client.get(f"/api/v1/virtual-machines/{vm_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vm-put-updated"


@pytest.mark.django_db
def test_virtual_machine_update_patch(auth_client):
    """Test updating a virtual machine with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "vm-tenant-patch", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-patch",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    payload = {
        "name": "vm-patch",
        "type": "worker",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    create_r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    vm_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/virtual-machines/{vm_id}", {"status": "stopped"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "stopped"
    assert r.data["name"] == "vm-patch"  # Should remain unchanged
    assert r.data["type"] == "worker"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/virtual-machines/{vm_id}")
    assert r.status_code == 200
    assert r.data["status"] == "stopped"
    assert r.data["name"] == "vm-patch"


@pytest.mark.django_db
def test_virtual_machine_delete(auth_client):
    """Test deleting a virtual machine"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "vm-tenant-delete", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "vm-spec-delete",
            "generation": "gen1",
            "required_cpu": 1,
            "required_memory": 2,
            "required_storage": 25,
        },
        format="json",
    ).data

    payload = {
        "name": "vm-delete",
        "type": "other",
        "status": "running",
        "tenant": tenant["id"],
        "specification": spec["id"],
    }
    create_r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    vm_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/virtual-machines/{vm_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/virtual-machines/{vm_id}")
    assert r.status_code == 404


# ============================================================================
# VM SPECIFICATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_vm_specification_create(auth_client):
    """Test creating a VM specification"""
    payload = {
        "name": "spec-create",
        "generation": "gen1",
        "required_cpu": 2,
        "required_memory": 4,
        "required_storage": 50,
    }
    r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "spec-create"
    assert r.data["generation"] == "gen1"
    assert r.data["required_cpu"] == 2


@pytest.mark.django_db
def test_vm_specification_list(auth_client):
    """Test listing VM specifications"""
    r = auth_client.get("/api/v1/vm-specifications")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_vm_specification_retrieve(auth_client):
    """Test retrieving a specific VM specification"""
    payload = {
        "name": "spec-retrieve",
        "generation": "gen2",
        "required_cpu": 4,
        "required_memory": 8,
        "required_storage": 100,
    }
    create_r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    spec_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/vm-specifications/{spec_id}")
    assert r.status_code == 200
    assert r.data["name"] == "spec-retrieve"
    assert r.data["generation"] == "gen2"
    assert r.data["required_cpu"] == 4


@pytest.mark.django_db
def test_vm_specification_update_put(auth_client):
    """Test updating a VM specification with PUT"""
    payload = {
        "name": "spec-put",
        "generation": "gen1",
        "required_cpu": 2,
        "required_memory": 4,
        "required_storage": 50,
    }
    create_r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    spec_id = create_r.data["id"]

    put_payload = {
        "name": "spec-put-updated",
        "generation": "gen3",
        "required_cpu": 8,
        "required_memory": 16,
        "required_storage": 200,
    }
    r = auth_client.put(
        f"/api/v1/vm-specifications/{spec_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "spec-put-updated"
    assert r.data["generation"] == "gen3"
    assert r.data["required_cpu"] == 8
    assert r.data["required_memory"] == 16

    # Verify in database
    r = auth_client.get(f"/api/v1/vm-specifications/{spec_id}")
    assert r.status_code == 200
    assert r.data["name"] == "spec-put-updated"
    assert r.data["required_cpu"] == 8


@pytest.mark.django_db
def test_vm_specification_update_patch(auth_client):
    """Test updating a VM specification with PATCH"""
    payload = {
        "name": "spec-patch",
        "generation": "gen1",
        "required_cpu": 2,
        "required_memory": 4,
        "required_storage": 50,
    }
    create_r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    spec_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/vm-specifications/{spec_id}", {"generation": "gen2"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["generation"] == "gen2"
    assert r.data["name"] == "spec-patch"  # Should remain unchanged
    assert r.data["required_cpu"] == 2  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/vm-specifications/{spec_id}")
    assert r.status_code == 200
    assert r.data["generation"] == "gen2"
    assert r.data["name"] == "spec-patch"


@pytest.mark.django_db
def test_vm_specification_delete(auth_client):
    """Test deleting a VM specification"""
    payload = {
        "name": "spec-delete",
        "generation": "gen1",
        "required_cpu": 1,
        "required_memory": 2,
        "required_storage": 25,
    }
    create_r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    spec_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/vm-specifications/{spec_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/vm-specifications/{spec_id}")
    assert r.status_code == 404
