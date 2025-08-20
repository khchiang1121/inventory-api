import pytest
from django.contrib.auth import get_user_model

from .base import auth_client


@pytest.mark.django_db
def test_group_permissions_actions(auth_client):
    # Create a simple tenant object to target
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tp2", "status": "active"}, format="json"
    ).data

    # Create a user to grant permissions to
    User = get_user_model()
    user = User.objects.create_user(username="permuser2", password="x")

    # Assign permission to user
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

    # Remove permission
    r = auth_client.post(
        "/api/v1/permissions/remove_user_permission", payload, format="json"
    )
    assert r.status_code in (200, 201)
