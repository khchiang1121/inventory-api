import pytest

from .base import auth_client

# ============================================================================
# TENANT TESTS (moved to test_users.py to avoid duplication)
# ============================================================================
# Note: Tenant tests are already covered in test_users.py with proper individual tests


# ============================================================================
# NETWORK INTERFACE TESTS
# ============================================================================


@pytest.mark.django_db
def test_network_interface_create(auth_client):
    """Test creating a network interface"""
    # Setup baremetal as the host
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "Cisco"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "UCS",
            "manufacturer": manufacturer["id"],
            "suppliers": [],
            "total_cpu": 16,
            "total_memory": 32,
            "total_storage": 512,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab-ni"}, format="json").data
    phase = auth_client.post(
        "/api/v1/phases", {"name": "phase-ni", "fab": fab["id"]}, format="json"
    ).data
    dc = auth_client.post(
        "/api/v1/data-centers", {"name": "dc-ni", "phase": phase["id"]}, format="json"
    ).data
    room = auth_client.post(
        "/api/v1/rooms", {"name": "room-ni", "datacenter": dc["id"]}, format="json"
    ).data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack-ni",
            "bgp_number": "65100",
            "as_number": 65100,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
            "room": room["id"],
        },
        format="json",
    ).data
    unit = auth_client.post(
        "/api/v1/units",
        {
            "rack": rack["id"],
            "name": "U1",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g-ni",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "status": "active",
        },
        format="json",
    ).data

    # Create PR and PO required by Baremetal
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {
            "pr_number": "PR-NI-001",
            "requested_by": "tester",
            "department": "QA",
            "reason": "Test setup",
        },
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {
            "po_number": "PO-NI-001",
            "vendor_name": "Vendor",
            "payment_terms": "NET30",
        },
        format="json",
    ).data

    baremetal = auth_client.post(
        "/api/v1/baremetals",
        {
            "name": "bm-ni",
            "serial_number": "SN-NI",
            "model": model["id"],
            "fabrication": fab["id"],
            "phase": phase["id"],
            "data_center": dc["id"],
            "rack": rack["id"],
            "unit": unit["id"],
            "status": "active",
            "available_cpu": 16,
            "available_memory": 16,
            "available_storage": 200,
            "group": group["id"],
            "pr": pr["id"],
            "po": po["id"],
        },
        format="json",
    ).data

    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="api", model="baremetal")

    payload = {
        "content_type": ct.id,
        "object_id": baremetal["id"],
        "name": "eth0-create",
        "mac_address": "00:11:22:33:44:55",
        "ipv4_address": "192.168.1.100",
        "is_primary": True,
    }
    r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "eth0-create"
    assert r.data["mac_address"] == "00:11:22:33:44:55"
    assert r.data["is_primary"] is True


@pytest.mark.django_db
def test_network_interface_list(auth_client):
    """Test listing network interfaces"""
    r = auth_client.get("/api/v1/network-interfaces")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_network_interface_retrieve(auth_client):
    """Test retrieving a specific network interface"""
    # Setup tenant as the host for simplicity
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "ni-tenant", "status": "active"}, format="json"
    ).data

    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="api", model="tenant")

    payload = {
        "content_type": ct.id,
        "object_id": tenant["id"],
        "name": "eth0-retrieve",
        "mac_address": "00:11:22:33:44:66",
        "ip_address": "192.168.1.101",
        "is_primary": False,
    }
    create_r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    ni_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/network-interfaces/{ni_id}")
    assert r.status_code == 200
    assert r.data["name"] == "eth0-retrieve"
    assert r.data["mac_address"] == "00:11:22:33:44:66"
    assert r.data["is_primary"] is False


@pytest.mark.django_db
def test_network_interface_update_put(auth_client):
    """Test updating a network interface with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "ni-tenant-put", "status": "active"}, format="json"
    ).data

    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="api", model="tenant")

    payload = {
        "content_type": ct.id,
        "object_id": tenant["id"],
        "name": "eth0-put",
        "mac_address": "00:11:22:33:44:77",
        "ip_address": "192.168.1.102",
        "is_primary": False,
    }
    create_r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    ni_id = create_r.data["id"]

    put_payload = {
        "content_type": ct.id,
        "object_id": tenant["id"],
        "name": "eth0-put-updated",
        "mac_address": "00:11:22:33:44:88",
        "ipv4_address": "192.168.1.200",
        "is_primary": True,
    }
    r = auth_client.put(f"/api/v1/network-interfaces/{ni_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "eth0-put-updated"
    assert r.data["mac_address"] == "00:11:22:33:44:88"
    assert r.data["ipv4_address"] == "192.168.1.200"
    assert r.data["is_primary"] is True

    # Verify in database
    r = auth_client.get(f"/api/v1/network-interfaces/{ni_id}")
    assert r.status_code == 200
    assert r.data["name"] == "eth0-put-updated"
    assert r.data["mac_address"] == "00:11:22:33:44:88"


@pytest.mark.django_db
def test_network_interface_update_patch(auth_client):
    """Test updating a network interface with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "ni-tenant-patch", "status": "active"},
        format="json",
    ).data

    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="api", model="tenant")

    payload = {
        "content_type": ct.id,
        "object_id": tenant["id"],
        "name": "eth0-patch",
        "mac_address": "00:11:22:33:44:99",
        "ip_address": "192.168.1.103",
        "is_primary": False,
    }
    create_r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    ni_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/network-interfaces/{ni_id}", {"is_primary": True}, format="json"
    )
    assert r.status_code == 200
    assert r.data["is_primary"] is True
    assert r.data["name"] == "eth0-patch"  # Should remain unchanged
    assert r.data["mac_address"] == "00:11:22:33:44:99"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/network-interfaces/{ni_id}")
    assert r.status_code == 200
    assert r.data["is_primary"] is True
    assert r.data["name"] == "eth0-patch"


@pytest.mark.django_db
def test_network_interface_delete(auth_client):
    """Test deleting a network interface"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "ni-tenant-delete", "status": "active"},
        format="json",
    ).data

    from django.contrib.contenttypes.models import ContentType

    ct = ContentType.objects.get(app_label="api", model="tenant")

    payload = {
        "content_type": ct.id,
        "object_id": tenant["id"],
        "name": "eth0-delete",
        "mac_address": "00:11:22:33:44:AA",
        "ip_address": "192.168.1.104",
        "is_primary": False,
    }
    create_r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    ni_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/network-interfaces/{ni_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/network-interfaces/{ni_id}")
    assert r.status_code == 404
