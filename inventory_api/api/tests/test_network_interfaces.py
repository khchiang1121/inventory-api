from django.contrib.contenttypes.models import ContentType

import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_network_interface_for_baremetal(auth_client):
    # minimal tree to create a baremetal
    brand = auth_client.post("/api/v1/brands", {"name": "Br"}, format="json").data
    model = auth_client.post(
        "/api/v1/baremetal-models",
        {
            "name": "M1",
            "brand": brand["id"],
            "total_cpu": 1,
            "total_memory": 1,
            "total_storage": 1,
        },
        format="json",
    ).data
    fab = auth_client.post("/api/v1/fabrications", {"name": "f"}, format="json").data
    phase = auth_client.post("/api/v1/phases", {"name": "p"}, format="json").data
    dc = auth_client.post("/api/v1/data-centers", {"name": "d"}, format="json").data
    rack = auth_client.post(
        "/api/v1/racks",
        {
            "name": "r",
            "bgp_number": "65000",
            "as_number": 65000,
            "height_units": 42,
            "power_capacity": "1.00",
            "status": "active",
        },
        format="json",
    ).data
    pr = auth_client.post(
        "/api/v1/purchase-requisitions",
        {"pr_number": "prx", "requested_by": "u"},
        format="json",
    ).data
    po = auth_client.post(
        "/api/v1/purchase-orders",
        {"po_number": "pox", "vendor_name": "v"},
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "g",
            "description": "",
            "total_cpu": 1,
            "total_memory": 1,
            "total_storage": 1,
            "available_cpu": 1,
            "available_memory": 1,
            "available_storage": 1,
            "status": "active",
        },
        format="json",
    ).data
    bm = auth_client.post(
        "/api/v1/baremetals",
        {
            "name": "bm",
            "serial_number": "SNX",
            "model": model["id"],
            "fabrication": fab["id"],
            "phase": phase["id"],
            "data_center": dc["id"],
            "rack": rack["id"],
            "status": "active",
            "available_cpu": 1,
            "available_memory": 1,
            "available_storage": 1,
            "group": group["id"],
            "pr": pr["id"],
            "po": po["id"],
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="baremetal")
    payload = {
        "content_type": ct.id,
        "object_id": bm["id"],
        "name": "eth0",
        "mac_address": "AA:BB:CC",
        "is_primary": True,
    }
    r = auth_client.post("/api/v1/network-interfaces", payload, format="json")
    assert r.status_code == 201
    ni_id = r.data["id"]

    assert auth_client.get(f"/api/v1/network-interfaces/{ni_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/network-interfaces/{ni_id}", {"name": "eth1"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/network-interfaces/{ni_id}").status_code in (
        200,
        204,
    )
