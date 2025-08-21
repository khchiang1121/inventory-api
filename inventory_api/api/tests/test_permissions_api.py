from django.contrib.auth import get_user_model

import pytest

from .base import auth_client


@pytest.mark.django_db
def test_object_permissions_assign_list(auth_client):
    # Create a tenant and a user
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tp", "status": "active"}, format="json"
    ).data
    User = get_user_model()
    user = User.objects.create_user(username="permuser", password="x")

    # Assign permission
    payload = {
        "model_name": "api.tenant",
        "object_id": tenant["id"],
        "user_id": str(user.id),
        "permission": "view_tenant",
    }
    r = auth_client.post(
        "/api/v1/permissions/assign_user_permission", payload, format="json"
    )
    assert r.status_code in (200, 201)

    # List objects for user
    r = auth_client.get(
        "/api/v1/permissions/get_user_objects",
        {
            "model_name": "api.tenant",
            "user_id": str(user.id),
            "permission": "view_tenant",
        },
    )
    assert r.status_code == 200
    assert tenant["id"] in r.data.get("objects", [])
