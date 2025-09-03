import pytest

# ============================================================================
# USER TESTS
# ============================================================================


@pytest.mark.django_db
def test_user_create(auth_client):
    """Test creating a user"""
    payload = {"username": "user-create", "password": "p@ssw0rd", "status": "active"}
    r = auth_client.post("/api/v1/users", payload, format="json")
    assert r.status_code == 201
    assert r.data["username"] == "user-create"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_user_list(auth_client):
    """Test listing users"""
    r = auth_client.get("/api/v1/users")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_user_retrieve(auth_client):
    """Test retrieving a specific user"""
    payload = {"username": "user-retrieve", "password": "p@ssw0rd", "status": "active"}
    create_r = auth_client.post("/api/v1/users", payload, format="json")
    user_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 200
    assert r.data["username"] == "user-retrieve"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_user_update_put(auth_client):
    """Test updating a user with PUT"""
    payload = {"username": "user-put", "password": "p@ssw0rd", "status": "active"}
    create_r = auth_client.post("/api/v1/users", payload, format="json")
    user_id = create_r.data["id"]

    put_data = {
        "username": "user-put-updated",
        "password": "newp@ssw0rd",
        "email": "put@example.com",
        "status": "active",
    }
    r = auth_client.put(f"/api/v1/users/{user_id}", put_data, format="json")
    assert r.status_code == 200
    assert r.data["username"] == "user-put-updated"
    assert r.data["email"] == "put@example.com"

    # Verify in database
    r = auth_client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 200
    assert r.data["username"] == "user-put-updated"
    assert r.data["email"] == "put@example.com"


@pytest.mark.django_db
def test_user_update_patch(auth_client):
    """Test updating a user with PATCH"""
    payload = {
        "username": "user-patch",
        "password": "p@ssw0rd",
        "status": "active",
        "email": "patch@example.com",
    }
    create_r = auth_client.post("/api/v1/users", payload, format="json")
    user_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/users/{user_id}",
        {"email": "patch-updated@example.com"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["email"] == "patch-updated@example.com"
    assert r.data["username"] == "user-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 200
    assert r.data["email"] == "patch-updated@example.com"
    assert r.data["username"] == "user-patch"


@pytest.mark.django_db
def test_user_delete(auth_client):
    """Test deleting a user"""
    payload = {"username": "user-delete", "password": "p@ssw0rd", "status": "active"}
    create_r = auth_client.post("/api/v1/users", payload, format="json")
    user_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/users/{user_id}")
    assert r.status_code in (200, 204)

    # Verify deletion
    r = auth_client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 404


# ============================================================================
# TENANT TESTS
# ============================================================================


@pytest.mark.django_db
def test_tenant_create(auth_client):
    """Test creating a tenant"""
    payload = {"name": "tenant-create", "status": "active"}
    r = auth_client.post("/api/v1/tenants", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "tenant-create"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_tenant_list(auth_client):
    """Test listing tenants"""
    r = auth_client.get("/api/v1/tenants")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_tenant_retrieve(auth_client):
    """Test retrieving a specific tenant"""
    payload = {"name": "tenant-retrieve", "status": "active"}
    create_r = auth_client.post("/api/v1/tenants", payload, format="json")
    tenant_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/tenants/{tenant_id}")
    assert r.status_code == 200
    assert r.data["name"] == "tenant-retrieve"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_tenant_update_put(auth_client):
    """Test updating a tenant with PUT"""
    payload = {
        "name": "tenant-put",
        "status": "active",
        "description": "Original description",
    }
    create_r = auth_client.post("/api/v1/tenants", payload, format="json")
    tenant_id = create_r.data["id"]

    put_payload = {
        "name": "tenant-put-updated",
        "status": "inactive",
        "description": "Updated description",
    }
    r = auth_client.put(f"/api/v1/tenants/{tenant_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "tenant-put-updated"
    assert r.data["status"] == "inactive"
    assert r.data["description"] == "Updated description"

    # Verify in database
    r = auth_client.get(f"/api/v1/tenants/{tenant_id}")
    assert r.status_code == 200
    assert r.data["name"] == "tenant-put-updated"
    assert r.data["status"] == "inactive"


@pytest.mark.django_db
def test_tenant_update_patch(auth_client):
    """Test updating a tenant with PATCH"""
    payload = {
        "name": "tenant-patch",
        "status": "active",
        "description": "Original description",
    }
    create_r = auth_client.post("/api/v1/tenants", payload, format="json")
    tenant_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/tenants/{tenant_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "tenant-patch"  # Should remain unchanged
    assert r.data["description"] == "Original description"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/tenants/{tenant_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "tenant-patch"


@pytest.mark.django_db
def test_tenant_delete(auth_client):
    """Test deleting a tenant"""
    payload = {"name": "tenant-delete", "status": "active"}
    create_r = auth_client.post("/api/v1/tenants", payload, format="json")
    tenant_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/tenants/{tenant_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/tenants/{tenant_id}")
    assert r.status_code == 404
