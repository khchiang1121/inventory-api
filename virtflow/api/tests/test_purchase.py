import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_purchase_requisition(auth_client):
    payload = {
        "pr_number": "PR-1",
        "requested_by": "alice",
        "department": "IT",
        "reason": "servers",
    }
    r = auth_client.post("/api/v1/purchase-requisitions", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/purchase-requisitions/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/purchase-requisitions/{obj_id}",
            {"department": "OPS"},
            format="json",
        ).status_code
        == 200
    )
    assert auth_client.delete(
        f"/api/v1/purchase-requisitions/{obj_id}"
    ).status_code in (204, 200)


@pytest.mark.django_db
def test_crud_purchase_order(auth_client):
    payload = {"po_number": "PO-1", "vendor_name": "dell", "payment_terms": "net30"}
    r = auth_client.post("/api/v1/purchase-orders", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/purchase-orders/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/purchase-orders/{obj_id}",
            {"payment_terms": "net45"},
            format="json",
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/purchase-orders/{obj_id}").status_code in (
        204,
        200,
    )
