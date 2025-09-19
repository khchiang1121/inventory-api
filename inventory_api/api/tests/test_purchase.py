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
    r = auth_client.put(f"/api/v1/purchase-requisitions/{pr_id}", put_payload, format="json")
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
    # First create a purchase requisition
    pr_payload = {
        "pr_number": "PR-FOR-PO-001",
        "requested_by": "alice",
        "department": "IT",
        "reason": "Server procurement",
    }
    pr = auth_client.post("/api/v1/purchase-requisitions", pr_payload, format="json").data

    # Create a supplier
    supplier_payload = {
        "name": "Dell Technologies",
        "contact_email": "sales@dell.com",
        "contact_phone": "1-800-DELL",
        "address": "Round Rock, TX",
        "website": "https://dell.com",
    }
    supplier = auth_client.post("/api/v1/suppliers", supplier_payload, format="json").data

    # Create purchase order
    payload = {
        "po_number": "PO-CREATE-001",
        "purchase_requisition": pr["id"],
        "supplier": supplier["id"],
        "payment_terms": "net30",
        "amount": "10000.00",
        "used": "0.00",
        "description": "Server hardware procurement",
    }
    r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    assert r.status_code == 201
    assert r.data["po_number"] == "PO-CREATE-001"
    assert str(r.data["purchase_requisition"]) == str(pr["id"])  # CREATE returns UUID
    assert str(r.data["supplier"]) == str(supplier["id"])  # CREATE returns UUID
    assert r.data["payment_terms"] == "net30"
    assert str(r.data["amount"]) == "10000.00"
    assert str(r.data["used"]) == "0.00"


@pytest.mark.django_db
def test_purchase_order_list(auth_client):
    """Test listing purchase orders"""
    r = auth_client.get("/api/v1/purchase-orders")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_purchase_order_retrieve(auth_client):
    """Test retrieving a specific purchase order"""
    # Create purchase requisition
    pr_payload = {
        "pr_number": "PR-FOR-RETRIEVE",
        "requested_by": "bob",
        "department": "IT",
        "reason": "Hardware procurement",
    }
    pr = auth_client.post("/api/v1/purchase-requisitions", pr_payload, format="json").data

    # Create supplier
    supplier_payload = {
        "name": "HP Inc",
        "contact_email": "sales@hp.com",
        "contact_phone": "1-800-HP",
        "address": "Palo Alto, CA",
        "website": "https://hp.com",
    }
    supplier = auth_client.post("/api/v1/suppliers", supplier_payload, format="json").data

    # Create purchase order
    payload = {
        "po_number": "PO-RETRIEVE-001",
        "purchase_requisition": pr["id"],
        "supplier": supplier["id"],
        "payment_terms": "net45",
        "amount": "5000.00",
        "used": "1000.00",
        "description": "HP hardware procurement",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-RETRIEVE-001"
    assert r.data["purchase_requisition"]["id"] == pr["id"]  # GET returns nested object
    assert r.data["supplier"]["name"] == "HP Inc"  # GET returns nested object
    assert r.data["payment_terms"] == "net45"
    assert str(r.data["amount"]) == "5000.00"
    assert str(r.data["used"]) == "1000.00"


@pytest.mark.django_db
def test_purchase_order_update_put(auth_client):
    """Test updating a purchase order with PUT"""
    # Create purchase requisition
    pr_payload = {
        "pr_number": "PR-FOR-PUT",
        "requested_by": "charlie",
        "department": "IT",
        "reason": "Equipment update",
    }
    pr = auth_client.post("/api/v1/purchase-requisitions", pr_payload, format="json").data

    # Create suppliers
    supplier1_payload = {
        "name": "IBM",
        "contact_email": "sales@ibm.com",
        "contact_phone": "1-800-IBM",
        "address": "Armonk, NY",
        "website": "https://ibm.com",
    }
    supplier1 = auth_client.post("/api/v1/suppliers", supplier1_payload, format="json").data

    supplier2_payload = {
        "name": "IBM Corporation",
        "contact_email": "enterprise@ibm.com",
        "contact_phone": "1-800-IBM-ENT",
        "address": "Armonk, NY",
        "website": "https://ibm.com/enterprise",
    }
    supplier2 = auth_client.post("/api/v1/suppliers", supplier2_payload, format="json").data

    # Create purchase order
    payload = {
        "po_number": "PO-PUT-001",
        "purchase_requisition": pr["id"],
        "supplier": supplier1["id"],
        "payment_terms": "net30",
        "amount": "8000.00",
        "used": "2000.00",
        "description": "IBM equipment",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    # Update with PUT
    put_payload = {
        "po_number": "PO-PUT-001-UPDATED",
        "purchase_requisition": pr["id"],
        "supplier": supplier2["id"],
        "payment_terms": "net60",
        "amount": "12000.00",
        "used": "3000.00",
        "description": "Updated IBM equipment order",
    }
    r = auth_client.put(f"/api/v1/purchase-orders/{po_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-PUT-001-UPDATED"
    assert str(r.data["supplier"]) == str(supplier2["id"])  # PUT returns UUID
    assert r.data["payment_terms"] == "net60"
    assert str(r.data["amount"]) == "12000.00"

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["po_number"] == "PO-PUT-001-UPDATED"
    assert r.data["supplier"]["name"] == "IBM Corporation"  # GET returns nested object
    assert str(r.data["amount"]) == "12000.00"


@pytest.mark.django_db
def test_purchase_order_update_patch(auth_client):
    """Test updating a purchase order with PATCH"""
    # Create purchase requisition
    pr_payload = {
        "pr_number": "PR-FOR-PATCH",
        "requested_by": "diana",
        "department": "Procurement",
        "reason": "Network equipment",
    }
    pr = auth_client.post("/api/v1/purchase-requisitions", pr_payload, format="json").data

    # Create supplier
    supplier_payload = {
        "name": "Cisco Systems",
        "contact_email": "sales@cisco.com",
        "contact_phone": "1-800-CISCO",
        "address": "San Jose, CA",
        "website": "https://cisco.com",
    }
    supplier = auth_client.post("/api/v1/suppliers", supplier_payload, format="json").data

    # Create purchase order
    payload = {
        "po_number": "PO-PATCH-001",
        "purchase_requisition": pr["id"],
        "supplier": supplier["id"],
        "payment_terms": "net30",
        "amount": "15000.00",
        "used": "5000.00",
        "description": "Cisco network equipment",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    # Update with PATCH
    r = auth_client.patch(
        f"/api/v1/purchase-orders/{po_id}",
        {"payment_terms": "net45", "used": "7000.00"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["payment_terms"] == "net45"
    assert str(r.data["used"]) == "7000.00"
    assert r.data["po_number"] == "PO-PATCH-001"  # Should remain unchanged
    assert str(r.data["purchase_requisition"]) == str(pr["id"])  # PATCH returns UUID

    # Verify in database
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 200
    assert r.data["payment_terms"] == "net45"
    assert str(r.data["used"]) == "7000.00"
    assert r.data["po_number"] == "PO-PATCH-001"
    assert r.data["supplier"]["name"] == "Cisco Systems"  # GET returns nested object


@pytest.mark.django_db
def test_purchase_order_delete(auth_client):
    """Test deleting a purchase order"""
    # Create purchase requisition
    pr_payload = {
        "pr_number": "PR-FOR-DELETE",
        "requested_by": "eve",
        "department": "Finance",
        "reason": "Equipment disposal",
    }
    pr = auth_client.post("/api/v1/purchase-requisitions", pr_payload, format="json").data

    # Create supplier
    supplier_payload = {
        "name": "Lenovo",
        "contact_email": "sales@lenovo.com",
        "contact_phone": "1-800-LENOVO",
        "address": "Beijing, China",
        "website": "https://lenovo.com",
    }
    supplier = auth_client.post("/api/v1/suppliers", supplier_payload, format="json").data

    # Create purchase order
    payload = {
        "po_number": "PO-DELETE-001",
        "purchase_requisition": pr["id"],
        "supplier": supplier["id"],
        "payment_terms": "net30",
        "amount": "6000.00",
        "used": "0.00",
        "description": "Lenovo equipment order",
    }
    create_r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    po_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/purchase-orders/{po_id}")
    assert r.status_code == 404
