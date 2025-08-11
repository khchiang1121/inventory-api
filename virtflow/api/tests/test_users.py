import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_user_minimal(auth_client):
    # Create
    r = auth_client.post(
        "/api/v1/users",
        {"username": "api-user", "password": "p@ssw0rd", "status": "active"},
        format="json",
    )
    assert r.status_code == 201
    uid = r.data["id"]

    # Retrieve
    assert auth_client.get(f"/api/v1/users/{uid}").status_code == 200

    # Partial update
    r = auth_client.patch(
        f"/api/v1/users/{uid}", {"email": "api@example.com"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["email"] == "api@example.com"

    # Delete
    assert auth_client.delete(f"/api/v1/users/{uid}").status_code in (200, 204)
