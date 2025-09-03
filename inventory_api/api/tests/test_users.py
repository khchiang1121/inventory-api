import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_user_complete(auth_client):
    # Create
    r = auth_client.post(
        "/api/v1/users",
        {"username": "api-user", "password": "p@ssw0rd", "status": "active"},
        format="json",
    )
    assert r.status_code == 201
    uid = r.data["id"]

    # List
    r = auth_client.get("/api/v1/users")
    assert r.status_code == 200
    assert len(r.data["results"]) >= 1

    # Retrieve
    assert auth_client.get(f"/api/v1/users/{uid}").status_code == 200

    # Full Update (PUT)
    put_data = {
        "username": "api-user-updated",
        "password": "newp@ssw0rd",
        "email": "updated@example.com",
        "status": "active",
    }
    r = auth_client.put(f"/api/v1/users/{uid}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["username"] == "api-user-updated"
    assert r.data["email"] == "updated@example.com"

    # Verify in database
    r = auth_client.get(f"/api/v1/users/{uid}")
    assert r.status_code == 200
    assert r.data["username"] == "api-user-updated"
    assert r.data["email"] == "updated@example.com"

    # Partial update (PATCH)
    r = auth_client.patch(
        f"/api/v1/users/{uid}", {"email": "api@example.com"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["email"] == "api@example.com"
    # Username should remain unchanged
    assert r.data["username"] == "api-user-updated"

    # Verify PATCH in database
    r = auth_client.get(f"/api/v1/users/{uid}")
    assert r.status_code == 200
    assert r.data["email"] == "api@example.com"
    assert r.data["username"] == "api-user-updated"

    # Delete
    r = auth_client.delete(f"/api/v1/users/{uid}")
    assert r.status_code in (200, 204)

    # Verify deletion - should return 404
    r = auth_client.get(f"/api/v1/users/{uid}")
    assert r.status_code == 404
