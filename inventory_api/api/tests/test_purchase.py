import pytest

from .base import auth_client

# ============================================================================
# PURCHASE REQUISITION TESTS
# ============================================================================


@pytest.mark.django_db
def test_purchase_requisition_create(auth_client):
    """Test creating a purchase requisition"""
    payload = {
        "pr_number": "PR-CREATE-001",
        "requested_by": "alice",
        "department": "IT",
        "reason": "Server upgrade",
    }
    r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    assert r.status_code == 201
    assert r.data["pr_number"] == "PR-CREATE-001"
    assert r.data["requested_by"] == "alice"
    assert r.data["department"] == "IT"


@pytest.mark.django_db
def test_purchase_requisition_list(auth_client):
    """Test listing purchase requisitions"""
    r = auth_client.get("/api/v1/purchase-requisitions")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_purchase_requisition_retrieve(auth_client):
    """Test retrieving a specific purchase requisition"""
    payload = {
        "pr_number": "PR-RETRIEVE-001",
        "requested_by": "bob",
        "department": "Operations",
        "reason": "Network equipment",
    }
    create_r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    pr_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/purchase-requisitions/{pr_id}")
    assert r.status_code == 200
    assert r.data["pr_number"] == "PR-RETRIEVE-001"
    assert r.data["requested_by"] == "bob"


@pytest.mark.django_db
def test_purchase_requisition_update_put(auth_client):
    """Test updating a purchase requisition with PUT"""
    payload = {
        "pr_number": "PR-PUT-001",
        "requested_by": "charlie",
        "department": "IT",
        "reason": "Storage upgrade",
    }
    create_r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    pr_id = create_r.data["id"]

    put_payload = {
        "pr_number": "PR-PUT-001-UPDATED",
        "requested_by": "charlie-updated",
        "department": "DevOps",
        "reason": "Storage and network upgrade",
    }
    r = auth_client.put(
        f"/api/v1/purchase-requisitions/{pr_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert r.data["pr_number"] == "PR-PUT-001-UPDATED"
    assert r.data["department"] == "DevOps"
    assert r.data["reason"] == "Storage and network upgrade"

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-requisitions/{pr_id}")
    assert r.status_code == 200
    assert r.data["pr_number"] == "PR-PUT-001-UPDATED"
    assert r.data["department"] == "DevOps"


@pytest.mark.django_db
def test_purchase_requisition_update_patch(auth_client):
    """Test updating a purchase requisition with PATCH"""
    payload = {
        "pr_number": "PR-PATCH-001",
        "requested_by": "diana",
        "department": "IT",
        "reason": "Security upgrade",
    }
    create_r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    pr_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/purchase-requisitions/{pr_id}",
        {"department": "Security"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["department"] == "Security"
    assert r.data["pr_number"] == "PR-PATCH-001"  # Should remain unchanged
    assert r.data["requested_by"] == "diana"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-requisitions/{pr_id}")
    assert r.status_code == 200
    assert r.data["department"] == "Security"
    assert r.data["pr_number"] == "PR-PATCH-001"


@pytest.mark.django_db
def test_purchase_requisition_delete(auth_client):
    """Test deleting a purchase requisition"""
    payload = {
        "pr_number": "PR-DELETE-001",
        "requested_by": "eve",
        "department": "Finance",
        "reason": "Budget planning",
    }
    create_r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    pr_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/purchase-requisitions/{pr_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/purchase-requisitions/{pr_id}")
    assert r.status_code == 404


# ============================================================================
# PURCHASE ORDER TESTS
# ============================================================================


@pytest.mark.django_db
def test_purchase_order_create(auth_client):
    """Test creating a purchase order"""
    payload = {
        "po_number": "PO-CREATE-001",
        "vendor_name": "Dell Technologies",
        "payment_terms": "net30",
    }
    r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    assert r.status_code == 201
    assert r.data["po_number"] == "PO-CREATE-001"
    assert r.data["vendor_name"] == "Dell Technologies"
    assert r.data["payment_terms"] == "net30"


@pytest.mark.django_db
def test_purchase_order_list(auth_client):
    """Test listing purchase orders"""
    r = auth_client.get("/api/v1/purchase-orders")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_purchase_order_retrieve(auth_client):
    """Test retrieving a specific purchase order"""
    payload = {
        "po_number": "PO-RETRIEVE-001",
        "vendor_name": "HP Inc",
        "payment_terms": "net45",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-RETRIEVE-001"
    assert r.data["vendor_name"] == "HP Inc"


@pytest.mark.django_db
def test_purchase_order_update_put(auth_client):
    """Test updating a purchase order with PUT"""
    payload = {
        "po_number": "PO-PUT-001",
        "vendor_name": "IBM",
        "payment_terms": "net30",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    put_payload = {
        "po_number": "PO-PUT-001-UPDATED",
        "vendor_name": "IBM Corporation",
        "payment_terms": "net60",
    }
    r = auth_client.put(f"/api/v1/purchase-orders/{po_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-PUT-001-UPDATED"
    assert r.data["vendor_name"] == "IBM Corporation"
    assert r.data["payment_terms"] == "net60"

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-PUT-001-UPDATED"
    assert r.data["vendor_name"] == "IBM Corporation"


@pytest.mark.django_db
def test_purchase_order_update_patch(auth_client):
    """Test updating a purchase order with PATCH"""
    payload = {
        "po_number": "PO-PATCH-001",
        "vendor_name": "Cisco Systems",
        "payment_terms": "net30",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/purchase-orders/{po_id}", {"payment_terms": "net45"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["payment_terms"] == "net45"
    assert r.data["po_number"] == "PO-PATCH-001"  # Should remain unchanged
    assert r.data["vendor_name"] == "Cisco Systems"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["payment_terms"] == "net45"
    assert r.data["po_number"] == "PO-PATCH-001"


@pytest.mark.django_db
def test_purchase_order_delete(auth_client):
    """Test deleting a purchase order"""
    payload = {
        "po_number": "PO-DELETE-001",
        "vendor_name": "Lenovo",
        "payment_terms": "net30",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 404
