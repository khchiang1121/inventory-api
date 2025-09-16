import pytest
from django.contrib.contenttypes.models import ContentType

# ============================================================================
# BAREMETAL TESTS
# ============================================================================


@pytest.mark.django_db
def test_baremetal_create(auth_client):
    """Test creating a baremetal server"""
    # Setup dependencies
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "Dell"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "R740",
            "manufacturer": manufacturer["id"],
            "suppliers": [],
            "total_cpu": 64,
            "total_memory": 256,
            "total_storage": 4096,
            "total_gpu": 4,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab-x"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "p1"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "dc1"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack1",
            "bgp_number": "65001",
            "as_number": 65001,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
        },
        format="json",
    ).data
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {"pr_number": "PR-100", "requested_by": "ops"},
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {"po_number": "PO-100", "vendor_name": "Dell"},
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g1",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    # Create baremetal
    payload = {
        "name": "bm1",
        "serial_number": "SN1",
        "model": model["id"],
        "fabrication": fab["id"],
        "phase": phase["id"],
        "data_center": dc["id"],
        "rack": rack["id"],
        "unit": "U1",
        "status": "active",
        "available_cpu": 64,
        "available_memory": 128,
        "available_storage": 1000,
        "group": group["id"],
        "pr": pr.get("id"),
        "po": po.get("id"),
    }
    r = auth_client.post("/api/v1/baremetals", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "bm1"
    assert r.data["serial_number"] == "SN1"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_baremetal_list(auth_client):
    """Test listing baremetal servers"""
    r = auth_client.get("/api/v1/baremetals")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_baremetal_retrieve(auth_client):
    """Test retrieving a specific baremetal server"""
    # Setup and create baremetal
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "HP"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "DL380",
            "manufacturer": manufacturer["id"],
            "suppliers": [],
            "total_cpu": 32,
            "total_memory": 128,
            "total_storage": 2048,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab1"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "phase1"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "dc1"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack1",
            "bgp_number": "65001",
            "as_number": 65001,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g1",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    # Create PR and PO for baremetal
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {
            "pr_number": "PR-BM-RETRIEVE",
            "requested_by": "admin",
            "department": "IT",
            "reason": "test",
        },
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {
            "po_number": "PO-BM-RETRIEVE",
            "vendor_name": "Dell",
            "payment_terms": "net30",
        },
        format="json",
    ).data

    payload = {
        "name": "bm-retrieve",
        "serial_number": "SN123",
        "model": model["id"],
        "fabrication": fab["id"],
        "phase": phase["id"],
        "data_center": dc["id"],
        "rack": rack["id"],
        "unit": "U2",
        "status": "active",
        "available_cpu": 32,
        "available_memory": 64,
        "available_storage": 500,
        "group": group["id"],
        "pr": pr["id"],
        "po": po["id"],
    }
    create_r = auth_client.post("/api/v1/baremetals", payload, format="json")
    assert create_r.status_code == 201, f"Failed to create baremetal: {create_r.data}"
    bm_id = create_r.data["id"]

    # Retrieve
    r = auth_client.get(f"/api/v1/baremetals/{bm_id}")
    assert r.status_code == 200
    assert r.data["name"] == "bm-retrieve"
    assert r.data["serial_number"] == "SN123"


@pytest.mark.django_db
def test_baremetal_update(auth_client):
    """Test updating a baremetal server (PATCH)"""
    # Setup and create baremetal
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "IBM"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "x3650",
            "manufacturer": manufacturer["id"],
            "suppliers": [],
            "total_cpu": 24,
            "total_memory": 64,
            "total_storage": 1024,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab2"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "phase2"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "dc2"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack2",
            "bgp_number": "65002",
            "as_number": 65002,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g2",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    # Create PR and PO for baremetal
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {
            "pr_number": "PR-BM-UPDATE",
            "requested_by": "admin",
            "department": "IT",
            "reason": "test",
        },
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {"po_number": "PO-BM-UPDATE", "vendor_name": "Dell", "payment_terms": "net30"},
        format="json",
    ).data

    payload = {
        "name": "bm-update",
        "serial_number": "SN456",
        "model": model["id"],
        "fabrication": fab["id"],
        "phase": phase["id"],
        "data_center": dc["id"],
        "rack": rack["id"],
        "unit": "U3",
        "status": "active",
        "available_cpu": 24,
        "available_memory": 32,
        "available_storage": 300,
        "group": group["id"],
        "pr": pr["id"],
        "po": po["id"],
    }
    create_r = auth_client.post("/api/v1/baremetals", payload, format="json")
    assert create_r.status_code == 201, f"Failed to create baremetal: {create_r.data}"
    bm_id = create_r.data["id"]

    # Update status
    r = auth_client.patch(f"/api/v1/baremetals/{bm_id}", {"status": "inactive"}, format="json")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "bm-update"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/baremetals/{bm_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"


@pytest.mark.django_db
def test_baremetal_delete(auth_client):
    """Test deleting a baremetal server"""
    # Setup and create baremetal
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
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab3"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "phase3"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "dc3"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack3",
            "bgp_number": "65003",
            "as_number": 65003,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g3",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    # Create PR and PO for baremetal
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {
            "pr_number": "PR-BM-DELETE",
            "requested_by": "admin",
            "department": "IT",
            "reason": "test",
        },
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {"po_number": "PO-BM-DELETE", "vendor_name": "Dell", "payment_terms": "net30"},
        format="json",
    ).data

    payload = {
        "name": "bm-delete",
        "serial_number": "SN789",
        "model": model["id"],
        "fabrication": fab["id"],
        "phase": phase["id"],
        "data_center": dc["id"],
        "rack": rack["id"],
        "unit": "U4",
        "status": "active",
        "available_cpu": 16,
        "available_memory": 16,
        "available_storage": 200,
        "group": group["id"],
        "pr": pr["id"],
        "po": po["id"],
    }
    create_r = auth_client.post("/api/v1/baremetals", payload, format="json")
    assert create_r.status_code == 201, f"Failed to create baremetal: {create_r.data}"
    bm_id = create_r.data["id"]

    # Delete
    r = auth_client.delete(f"/api/v1/baremetals/{bm_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/baremetals/{bm_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_baremetal_with_network_interface(auth_client):
    """Test creating a network interface for a baremetal server"""
    # Setup and create baremetal
    manufacturer = auth_client.post(
        "/api/v1/manufacturers", {"name": "Supermicro"}, format="json"
    ).data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "X11",
            "manufacturer": manufacturer["id"],
            "suppliers": [],
            "total_cpu": 8,
            "total_memory": 16,
            "total_storage": 256,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "fab4"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "phase4"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "dc4"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "rack4",
            "bgp_number": "65004",
            "as_number": 65004,
            "height_units": 42,
            "power_capacity": "4.00",
            "status": "active",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g4",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    # Create PR and PO for baremetal
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {
            "pr_number": "PR-BM-NI",
            "requested_by": "admin",
            "department": "IT",
            "reason": "test",
        },
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {"po_number": "PO-BM-NI", "vendor_name": "Dell", "payment_terms": "net30"},
        format="json",
    ).data

    payload = {
        "name": "bm-network",
        "serial_number": "SN999",
        "model": model["id"],
        "fabrication": fab["id"],
        "phase": phase["id"],
        "data_center": dc["id"],
        "rack": rack["id"],
        "unit": "U5",
        "status": "active",
        "available_cpu": 8,
        "available_memory": 8,
        "available_storage": 100,
        "group": group["id"],
        "pr": pr["id"],
        "po": po["id"],
    }
    create_r = auth_client.post("/api/v1/baremetals", payload, format="json")
    assert create_r.status_code == 201, f"Failed to create baremetal: {create_r.data}"
    bm_id = create_r.data["id"]

    # Create network interface
    ct = ContentType.objects.get(app_label="api", model="baremetal")
    ni_payload = {
        "content_type": ct.id,
        "object_id": bm_id,
        "name": "eth0",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "is_primary": True,
    }
    r = auth_client.post("/api/v1/network-interfaces", ni_payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "eth0"
    assert r.data["is_primary"] is True


# ============================================================================
# MANUFACTURER TESTS
# ============================================================================


@pytest.mark.django_db
def test_manufacturer_create(auth_client):
    """Test creating a manufacturer"""
    r = auth_client.post("/api/v1/manufacturers", {"name": "HP"}, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "HP"


@pytest.mark.django_db
def test_manufacturer_list(auth_client):
    """Test listing manufacturers"""
    r = auth_client.get("/api/v1/manufacturers")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_manufacturer_retrieve(auth_client):
    """Test retrieving a specific manufacturer"""
    create_r = auth_client.post("/api/v1/manufacturers", {"name": "Dell"}, format="json")
    manufacturer_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/manufacturers/{manufacturer_id}")
    assert r.status_code == 200
    assert r.data["name"] == "Dell"


@pytest.mark.django_db
def test_manufacturer_update_put(auth_client):
    """Test updating a manufacturer with PUT"""
    create_r = auth_client.post("/api/v1/manufacturers", {"name": "HP"}, format="json")
    manufacturer_id = create_r.data["id"]

    r = auth_client.put(
        f"/api/v1/manufacturers/{manufacturer_id}", {"name": "HP Enterprise"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "HP Enterprise"

    # Verify in database
    r = auth_client.get(f"/api/v1/manufacturers/{manufacturer_id}")
    assert r.status_code == 200
    assert r.data["name"] == "HP Enterprise"


@pytest.mark.django_db
def test_manufacturer_update_patch(auth_client):
    """Test updating a manufacturer with PATCH"""
    create_r = auth_client.post("/api/v1/manufacturers", {"name": "HP Enterprise"}, format="json")
    manufacturer_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/manufacturers/{manufacturer_id}", {"name": "HPE"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "HPE"

    # Verify in database
    r = auth_client.get(f"/api/v1/manufacturers/{manufacturer_id}")
    assert r.status_code == 200
    assert r.data["name"] == "HPE"


@pytest.mark.django_db
def test_manufacturer_delete(auth_client):
    """Test deleting a manufacturer"""
    create_r = auth_client.post(
        "/api/v1/manufacturers", {"name": "TestManufacturer"}, format="json"
    )
    manufacturer_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/manufacturers/{manufacturer_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/manufacturers/{manufacturer_id}")
    assert r.status_code == 404


# ============================================================================
# BAREMETAL MODEL TESTS
# ============================================================================


@pytest.mark.django_db
def test_baremetal_model_create(auth_client):
    """Test creating a baremetal model"""
    manufacturer = auth_client.post(
        "/api/v1/manufacturers", {"name": "Lenovo"}, format="json"
    ).data
    s1 = auth_client.post("/api/v1/suppliers", {"name": "Supplier-A"}, format="json").data
    s2 = auth_client.post("/api/v1/suppliers", {"name": "Supplier-B"}, format="json").data

    payload = {
        "name": "ThinkSystem SR650",
        "manufacturer": manufacturer["id"],
        "suppliers": [s1["id"], s2["id"]],
        "total_cpu": 48,
        "total_memory": 768,
        "total_storage": 8192,
    }
    r = auth_client.post("/api/v1/baremetal-models", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "ThinkSystem SR650"
    assert r.data["total_cpu"] == 48
    model_id = r.data["id"]
    # Fetch with read serializer to validate nested suppliers
    r_detail = auth_client.get(f"/api/v1/baremetal-models/{model_id}")
    assert r_detail.status_code == 200
    resp_supplier_names = [s["name"] for s in r_detail.data.get("suppliers", [])]
    assert "Supplier-A" in resp_supplier_names and "Supplier-B" in resp_supplier_names


@pytest.mark.django_db
def test_baremetal_model_list(auth_client):
    """Test listing baremetal models"""
    r = auth_client.get("/api/v1/baremetal-models")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_baremetal_model_retrieve(auth_client):
    """Test retrieving a specific baremetal model"""
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "IBM"}, format="json").data
    s = auth_client.post("/api/v1/suppliers", {"name": "Supplier-R"}, format="json").data
    payload = {
        "name": "x3650 M5",
        "manufacturer": manufacturer["id"],
        "suppliers": [s["id"]],
        "total_cpu": 32,
        "total_memory": 512,
        "total_storage": 4096,
    }
    create_r = auth_client.post("/api/v1/baremetal-models", payload, format="json")
    model_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/baremetal-models/{model_id}")
    assert r.status_code == 200
    assert r.data["name"] == "x3650 M5"
    assert r.data["total_cpu"] == 32


@pytest.mark.django_db
def test_baremetal_model_update_put(auth_client):
    """Test updating a baremetal model with PUT"""
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "Dell"}, format="json").data
    s1 = auth_client.post("/api/v1/suppliers", {"name": "S-One"}, format="json").data
    payload = {
        "name": "PowerEdge R740",
        "manufacturer": manufacturer["id"],
        "suppliers": [s1["id"]],
        "total_cpu": 64,
        "total_memory": 1024,
        "total_storage": 10240,
    }
    create_r = auth_client.post("/api/v1/baremetal-models", payload, format="json")
    model_id = create_r.data["id"]

    s2 = auth_client.post("/api/v1/suppliers", {"name": "S-Two"}, format="json").data
    put_payload = {
        "name": "PowerEdge R740xd",
        "manufacturer": manufacturer["id"],
        "suppliers": [s1["id"], s2["id"]],
        "total_cpu": 128,
        "total_memory": 2048,
        "total_storage": 20480,
    }
    r = auth_client.put(f"/api/v1/baremetal-models/{model_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "PowerEdge R740xd"
    assert r.data["total_cpu"] == 128
    # Fetch with read serializer to validate nested suppliers
    r_detail = auth_client.get(f"/api/v1/baremetal-models/{model_id}")
    assert r_detail.status_code == 200
    resp_supplier_names = [s["name"] for s in r_detail.data.get("suppliers", [])]
    assert "S-One" in resp_supplier_names and "S-Two" in resp_supplier_names


@pytest.mark.django_db
def test_baremetal_model_update_patch(auth_client):
    """Test updating a baremetal model with PATCH"""
    manufacturer = auth_client.post("/api/v1/manufacturers", {"name": "HP"}, format="json").data
    s = auth_client.post("/api/v1/suppliers", {"name": "SP-1"}, format="json").data
    payload = {
        "name": "ProLiant DL380",
        "manufacturer": manufacturer["id"],
        "suppliers": [s["id"]],
        "total_cpu": 48,
        "total_memory": 768,
        "total_storage": 8192,
    }
    create_r = auth_client.post("/api/v1/baremetal-models", payload, format="json")
    model_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/baremetal-models/{model_id}", {"total_memory": 1536}, format="json"
    )
    assert r.status_code == 200
    assert r.data["total_memory"] == 1536
    assert r.data["name"] == "ProLiant DL380"  # Should remain unchanged


@pytest.mark.django_db
def test_baremetal_model_delete(auth_client):
    """Test deleting a baremetal model"""
    manufacturer = auth_client.post(
        "/api/v1/manufacturers", {"name": "Supermicro"}, format="json"
    ).data
    s = auth_client.post("/api/v1/suppliers", {"name": "Sup-Del"}, format="json").data
    payload = {
        "name": "SuperServer",
        "manufacturer": manufacturer["id"],
        "suppliers": [s["id"]],
        "total_cpu": 16,
        "total_memory": 256,
        "total_storage": 2048,
    }
    create_r = auth_client.post("/api/v1/baremetal-models", payload, format="json")
    model_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/baremetal-models/{model_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/baremetal-models/{model_id}")
    assert r.status_code == 404


# ============================================================================
# SUPPLIER TESTS
# ============================================================================


@pytest.mark.django_db
def test_supplier_create(auth_client):
    """Test creating a supplier"""
    r = auth_client.post(
        "/api/v1/suppliers",
        {"name": "Acme Supply", "contact_email": "a@ac.me"},
        format="json",
    )
    assert r.status_code == 201
    assert r.data["name"] == "Acme Supply"


@pytest.mark.django_db
def test_supplier_list(auth_client):
    """Test listing suppliers"""
    auth_client.post("/api/v1/suppliers", {"name": "S-1"}, format="json")
    auth_client.post("/api/v1/suppliers", {"name": "S-2"}, format="json")
    r = auth_client.get("/api/v1/suppliers")
    assert r.status_code == 200
    assert "results" in r.data
    names = [row["name"] for row in r.data["results"]]
    assert "S-1" in names and "S-2" in names


@pytest.mark.django_db
def test_supplier_retrieve_update_delete(auth_client):
    """Test retrieve, update, patch and delete of supplier"""
    create_r = auth_client.post("/api/v1/suppliers", {"name": "Orig"}, format="json")
    sid = create_r.data["id"]

    # Retrieve
    r = auth_client.get(f"/api/v1/suppliers/{sid}")
    assert r.status_code == 200
    assert r.data["name"] == "Orig"

    # PUT
    r = auth_client.put(
        f"/api/v1/suppliers/{sid}",
        {"name": "Orig-Updated", "website": "https://ex.com"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["name"] == "Orig-Updated"

    # PATCH
    r = auth_client.patch(f"/api/v1/suppliers/{sid}", {"contact_phone": "+1-555"}, format="json")
    assert r.status_code == 200
    assert r.data["contact_phone"] == "+1-555"

    # DELETE
    r = auth_client.delete(f"/api/v1/suppliers/{sid}")
    assert r.status_code in (204, 200)
    r = auth_client.get(f"/api/v1/suppliers/{sid}")
    assert r.status_code == 404


# ============================================================================
# BAREMETAL GROUP QUOTA TESTS
# ============================================================================


@pytest.mark.django_db
def test_baremetal_group_quota_create(auth_client):
    """Test creating a baremetal group tenant quota"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "test-tenant", "status": "active"}, format="json"
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "test-group",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 50.0,
        "memory_quota": 50,
        "storage_quota": 50,
        "gpu_quota": 2,
    }
    r = auth_client.post("/api/v1/baremetal-group-tenant-quotas", payload, format="json")
    assert r.status_code == 201
    assert r.data["cpu_quota_percentage"] == 50.0
    assert r.data["memory_quota"] == 50


@pytest.mark.django_db
def test_baremetal_group_quota_list(auth_client):
    """Test listing baremetal group tenant quotas"""
    r = auth_client.get("/api/v1/baremetal-group-tenant-quotas")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_baremetal_group_quota_retrieve(auth_client):
    """Test retrieving a specific baremetal group tenant quota"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "retrieve-tenant", "status": "active"},
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "retrieve-group",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 75.0,
        "memory_quota": 75,
        "storage_quota": 75,
        "gpu_quota": 3,
    }
    create_r = auth_client.post("/api/v1/baremetal-group-tenant-quotas", payload, format="json")
    qid = create_r.data["id"]

    r = auth_client.get(f"/api/v1/baremetal-group-tenant-quotas/{qid}")
    assert r.status_code == 200
    assert r.data["cpu_quota_percentage"] == 75.0
    assert r.data["memory_quota"] == 75


@pytest.mark.django_db
def test_baremetal_group_quota_update_put(auth_client):
    """Test updating a baremetal group tenant quota with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "put-tenant", "status": "active"}, format="json"
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "put-group",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 30.0,
        "memory_quota": 30,
        "storage_quota": 30,
        "gpu_quota": 1,
    }
    create_r = auth_client.post("/api/v1/baremetal-group-tenant-quotas", payload, format="json")
    qid = create_r.data["id"]

    put_payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 80.0,
        "memory_quota": 80,
        "storage_quota": 80,
        "gpu_quota": 4,
    }
    r = auth_client.put(f"/api/v1/baremetal-group-tenant-quotas/{qid}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["cpu_quota_percentage"] == 80.0
    assert r.data["memory_quota"] == 80

    # Verify in database
    r = auth_client.get(f"/api/v1/baremetal-group-tenant-quotas/{qid}")
    assert r.status_code == 200
    assert r.data["cpu_quota_percentage"] == 80.0


@pytest.mark.django_db
def test_baremetal_group_quota_update_patch(auth_client):
    """Test updating a baremetal group tenant quota with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "patch-tenant", "status": "active"}, format="json"
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "patch-group",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 40.0,
        "memory_quota": 40,
        "storage_quota": 40,
        "gpu_quota": 2,
    }
    create_r = auth_client.post("/api/v1/baremetal-group-tenant-quotas", payload, format="json")
    qid = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/baremetal-group-tenant-quotas/{qid}",
        {"cpu_quota_percentage": 90.0},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["cpu_quota_percentage"] == 90.0
    assert r.data["memory_quota"] == 40  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/baremetal-group-tenant-quotas/{qid}")
    assert r.status_code == 200
    assert r.data["cpu_quota_percentage"] == 90.0
    assert r.data["memory_quota"] == 40


@pytest.mark.django_db
def test_baremetal_group_quota_delete(auth_client):
    """Test deleting a baremetal group tenant quota"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "delete-tenant", "status": "active"}, format="json"
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "delete-group",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "total_gpu": 8,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "available_gpu": 4,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 25.0,
        "memory_quota": 25,
        "storage_quota": 25,
        "gpu_quota": 1,
    }
    create_r = auth_client.post("/api/v1/baremetal-group-tenant-quotas", payload, format="json")
    qid = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/baremetal-group-tenant-quotas/{qid}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/baremetal-group-tenant-quotas/{qid}")
    assert r.status_code == 404
