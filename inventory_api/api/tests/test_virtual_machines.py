from django.urls import reverse

import pytest
from rest_framework import status

from .base import auth_client


@pytest.mark.django_db
def test_crud_virtual_machine_minimal(auth_client):
    # Setup tenant and spec
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "t1", "status": "active"}, format="json"
    ).data
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "s1",
            "generation": "g1",
            "required_cpu": 1,
            "required_memory": 1,
            "required_storage": 1,
        },
        format="json",
    ).data

    payload = {
        "name": "vm1",
        "tenant": tenant["id"],
        "specification": spec["id"],
        "type": "other",
        "status": "running",
    }
    r = auth_client.post("/api/v1/virtual-machines", payload, format="json")
    assert r.status_code == 201
    vm_id = r.data["id"]
    assert auth_client.get(f"/api/v1/virtual-machines/{vm_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/virtual-machines/{vm_id}", {"status": "stopped"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/virtual-machines/{vm_id}").status_code in (
        204,
        200,
    )
