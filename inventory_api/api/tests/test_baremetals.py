from django.contrib.contenttypes.models import ContentType

import pytest

from .base import auth_client


@pytest.mark.django_db
def test_baremetal_crud_minimal_tree(auth_client, django_assert_num_queries):
    # Prerequisites: brand, model, fabrication, phase, data_center, rack, PR, PO, group
    brand = auth_client.post("/api/v1/brands", {"name": "Dell"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "R740",
            "brand": brand["id"],
            "total_cpu": 64,
            "total_memory": 256,
            "total_storage": 4096,
        },
        format="json",
    ).data
    fab = auth_client.post(
        "/api/v1/fabrications", {"name": "fab-x"}, format="json"
    ).data
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
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "status": "active",
        },
        format="json",
    ).data

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
    bm_id = r.data["id"]
    assert auth_client.get(f"/api/v1/baremetals/{bm_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/baremetals/{bm_id}", {"status": "inactive"}, format="json"
        ).status_code
        == 200
    )

    # Create a network interface for this baremetal via generic relation
    ct = ContentType.objects.get(app_label="api", model="baremetal")
    ni_payload = {
        "content_type": ct.id,
        "object_id": bm_id,
        "name": "eth0",
        "mac_address": "AA:BB:CC",
        "is_primary": True,
    }
    r = auth_client.post("/api/v1/network-interfaces", ni_payload, format="json")
    assert r.status_code == 201

    assert auth_client.delete(f"/api/v1/baremetals/{bm_id}").status_code in (204, 200)
