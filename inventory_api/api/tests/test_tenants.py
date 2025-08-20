import pytest
from django.urls import reverse
from rest_framework import status

from ..models import Tenant
from .base import auth_client


@pytest.mark.django_db
def test_crud_tenant(auth_client):
    payload = {"name": "team-a", "description": "", "status": "active"}
    r = auth_client.post("/api/v1/tenants", payload, format="json")
    assert r.status_code == 201
    t_id = r.data["id"]
    assert auth_client.get(f"/api/v1/tenants/{t_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/tenants/{t_id}", {"status": "inactive"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/tenants/{t_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_vm_spec(auth_client):
    payload = {
        "name": "s-1",
        "generation": "g1",
        "required_cpu": 2,
        "required_memory": 4,
        "required_storage": 10,
    }
    r = auth_client.post("/api/v1/vm-specifications", payload, format="json")
    assert r.status_code == 201
    spec_id = r.data["id"]
    assert auth_client.get(f"/api/v1/vm-specifications/{spec_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/vm-specifications/{spec_id}", {"generation": "g2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/vm-specifications/{spec_id}").status_code in (
        204,
        200,
    )
