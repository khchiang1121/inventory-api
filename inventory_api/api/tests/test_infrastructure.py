import pytest

# ============================================================================
# FABRICATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_fabrication_create(auth_client):
    """Test creating a fabrication"""
    payload = {"name": "fab-create", "old_system_id": "legacy-create"}
    r = auth_client.post("/api/v1/fabrications", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "fab-create"
    assert r.data["old_system_id"] == "legacy-create"


@pytest.mark.django_db
def test_fabrication_list(auth_client):
    """Test listing fabrications"""
    r = auth_client.get("/api/v1/fabrications")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_fabrication_retrieve(auth_client):
    """Test retrieving a specific fabrication"""
    payload = {"name": "fab-retrieve", "old_system_id": "legacy-retrieve"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["name"] == "fab-retrieve"
    assert r.data["old_system_id"] == "legacy-retrieve"


@pytest.mark.django_db
def test_fabrication_update_put(auth_client):
    """Test updating a fabrication with PUT"""
    payload = {"name": "fab-put", "old_system_id": "legacy-put"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    put_payload = {"name": "fab-put-updated", "old_system_id": "legacy-put-updated"}
    r = auth_client.put(f"/api/v1/fabrications/{fab_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "fab-put-updated"
    assert r.data["old_system_id"] == "legacy-put-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["name"] == "fab-put-updated"
    assert r.data["old_system_id"] == "legacy-put-updated"


@pytest.mark.django_db
def test_fabrication_update_patch(auth_client):
    """Test updating a fabrication with PATCH"""
    payload = {"name": "fab-patch", "old_system_id": "legacy-patch"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/fabrications/{fab_id}",
        {"old_system_id": "legacy-patch-updated"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["old_system_id"] == "legacy-patch-updated"
    assert r.data["name"] == "fab-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["old_system_id"] == "legacy-patch-updated"
    assert r.data["name"] == "fab-patch"


@pytest.mark.django_db
def test_fabrication_delete(auth_client):
    """Test deleting a fabrication"""
    payload = {"name": "fab-delete", "old_system_id": "legacy-delete"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 404


# ============================================================================
# PHASE TESTS
# ============================================================================


@pytest.mark.django_db
def test_phase_create(auth_client):
    """Test creating a phase"""
    payload = {"name": "phase-create"}
    r = auth_client.post("/api/v1/phases", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "phase-create"


@pytest.mark.django_db
def test_phase_list(auth_client):
    """Test listing phases"""
    r = auth_client.get("/api/v1/phases")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_phase_retrieve(auth_client):
    """Test retrieving a specific phase"""
    payload = {"name": "phase-retrieve"}
    create_r = auth_client.post("/api/v1/phases", payload, format="json")
    phase_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/phases/{phase_id}")
    assert r.status_code == 200
    assert r.data["name"] == "phase-retrieve"


@pytest.mark.django_db
def test_phase_update_put(auth_client):
    """Test updating a phase with PUT"""
    payload = {"name": "phase-put"}
    create_r = auth_client.post("/api/v1/phases", payload, format="json")
    phase_id = create_r.data["id"]

    put_payload = {"name": "phase-put-updated"}
    r = auth_client.put(f"/api/v1/phases/{phase_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "phase-put-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/phases/{phase_id}")
    assert r.status_code == 200
    assert r.data["name"] == "phase-put-updated"


@pytest.mark.django_db
def test_phase_update_patch(auth_client):
    """Test updating a phase with PATCH"""
    payload = {"name": "phase-patch"}
    create_r = auth_client.post("/api/v1/phases", payload, format="json")
    phase_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/phases/{phase_id}", {"name": "phase-patch-updated"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "phase-patch-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/phases/{phase_id}")
    assert r.status_code == 200
    assert r.data["name"] == "phase-patch-updated"


@pytest.mark.django_db
def test_phase_delete(auth_client):
    """Test deleting a phase"""
    payload = {"name": "phase-delete"}
    create_r = auth_client.post("/api/v1/phases", payload, format="json")
    phase_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/phases/{phase_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/phases/{phase_id}")
    assert r.status_code == 404


# ============================================================================
# DATA CENTER TESTS
# ============================================================================


@pytest.mark.django_db
def test_data_center_create(auth_client):
    """Test creating a data center"""
    payload = {"name": "dc-create"}
    r = auth_client.post("/api/v1/data-centers", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "dc-create"


@pytest.mark.django_db
def test_data_center_list(auth_client):
    """Test listing data centers"""
    r = auth_client.get("/api/v1/data-centers")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_data_center_retrieve(auth_client):
    """Test retrieving a specific data center"""
    payload = {"name": "dc-retrieve"}
    create_r = auth_client.post("/api/v1/data-centers", payload, format="json")
    dc_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/data-centers/{dc_id}")
    assert r.status_code == 200
    assert r.data["name"] == "dc-retrieve"


@pytest.mark.django_db
def test_data_center_update_put(auth_client):
    """Test updating a data center with PUT"""
    payload = {"name": "dc-put"}
    create_r = auth_client.post("/api/v1/data-centers", payload, format="json")
    dc_id = create_r.data["id"]

    put_payload = {"name": "dc-put-updated"}
    r = auth_client.put(f"/api/v1/data-centers/{dc_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "dc-put-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/data-centers/{dc_id}")
    assert r.status_code == 200
    assert r.data["name"] == "dc-put-updated"


@pytest.mark.django_db
def test_data_center_update_patch(auth_client):
    """Test updating a data center with PATCH"""
    payload = {"name": "dc-patch"}
    create_r = auth_client.post("/api/v1/data-centers", payload, format="json")
    dc_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/data-centers/{dc_id}", {"name": "dc-patch-updated"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "dc-patch-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/data-centers/{dc_id}")
    assert r.status_code == 200
    assert r.data["name"] == "dc-patch-updated"


@pytest.mark.django_db
def test_data_center_delete(auth_client):
    """Test deleting a data center"""
    payload = {"name": "dc-delete"}
    create_r = auth_client.post("/api/v1/data-centers", payload, format="json")
    dc_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/data-centers/{dc_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/data-centers/{dc_id}")
    assert r.status_code == 404


# ============================================================================
# ROOM TESTS
# ============================================================================


@pytest.mark.django_db
def test_room_create(auth_client):
    """Test creating a room"""
    payload = {"name": "room-create"}
    r = auth_client.post("/api/v1/rooms", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "room-create"


@pytest.mark.django_db
def test_room_list(auth_client):
    """Test listing rooms"""
    r = auth_client.get("/api/v1/rooms")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_room_retrieve(auth_client):
    """Test retrieving a specific room"""
    payload = {"name": "room-retrieve"}
    create_r = auth_client.post("/api/v1/rooms", payload, format="json")
    room_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/rooms/{room_id}")
    assert r.status_code == 200
    assert r.data["name"] == "room-retrieve"


@pytest.mark.django_db
def test_room_update_put(auth_client):
    """Test updating a room with PUT"""
    payload = {"name": "room-put"}
    create_r = auth_client.post("/api/v1/rooms", payload, format="json")
    room_id = create_r.data["id"]

    put_payload = {"name": "room-put-updated"}
    r = auth_client.put(f"/api/v1/rooms/{room_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "room-put-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/rooms/{room_id}")
    assert r.status_code == 200
    assert r.data["name"] == "room-put-updated"


@pytest.mark.django_db
def test_room_update_patch(auth_client):
    """Test updating a room with PATCH"""
    payload = {"name": "room-patch"}
    create_r = auth_client.post("/api/v1/rooms", payload, format="json")
    room_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/rooms/{room_id}", {"name": "room-patch-updated"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "room-patch-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/rooms/{room_id}")
    assert r.status_code == 200
    assert r.data["name"] == "room-patch-updated"


@pytest.mark.django_db
def test_room_delete(auth_client):
    """Test deleting a room"""
    payload = {"name": "room-delete"}
    create_r = auth_client.post("/api/v1/rooms", payload, format="json")
    room_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/rooms/{room_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/rooms/{room_id}")
    assert r.status_code == 404


# ============================================================================
# RACK TESTS
# ============================================================================


@pytest.mark.django_db
def test_rack_create(auth_client):
    """Test creating a rack"""
    payload = {
        "name": "rack-create",
        "bgp_number": "65001",
        "as_number": 65001,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    r = auth_client.post("/api/v1/racks", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "rack-create"
    assert r.data["as_number"] == 65001


@pytest.mark.django_db
def test_rack_list(auth_client):
    """Test listing racks"""
    r = auth_client.get("/api/v1/racks")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_rack_retrieve(auth_client):
    """Test retrieving a specific rack"""
    payload = {
        "name": "rack-retrieve",
        "bgp_number": "65002",
        "as_number": 65002,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/racks", payload, format="json")
    rack_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/racks/{rack_id}")
    assert r.status_code == 200
    assert r.data["name"] == "rack-retrieve"
    assert r.data["as_number"] == 65002


@pytest.mark.django_db
def test_rack_update_put(auth_client):
    """Test updating a rack with PUT"""
    payload = {
        "name": "rack-put",
        "bgp_number": "65003",
        "as_number": 65003,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/racks", payload, format="json")
    rack_id = create_r.data["id"]

    put_payload = {
        "name": "rack-put-updated",
        "bgp_number": "65004",
        "as_number": 65004,
        "height_units": 48,
        "power_capacity": "6.00",
        "status": "maintenance",
    }
    r = auth_client.put(f"/api/v1/racks/{rack_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "rack-put-updated"
    assert r.data["as_number"] == 65004
    assert r.data["height_units"] == 48

    # Verify in database
    r = auth_client.get(f"/api/v1/racks/{rack_id}")
    assert r.status_code == 200
    assert r.data["name"] == "rack-put-updated"
    assert r.data["as_number"] == 65004


@pytest.mark.django_db
def test_rack_update_patch(auth_client):
    """Test updating a rack with PATCH"""
    payload = {
        "name": "rack-patch",
        "bgp_number": "65005",
        "as_number": 65005,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/racks", payload, format="json")
    rack_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/racks/{rack_id}", {"status": "maintenance"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "maintenance"
    assert r.data["name"] == "rack-patch"  # Should remain unchanged
    assert r.data["as_number"] == 65005  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/racks/{rack_id}")
    assert r.status_code == 200
    assert r.data["status"] == "maintenance"
    assert r.data["name"] == "rack-patch"


@pytest.mark.django_db
def test_rack_delete(auth_client):
    """Test deleting a rack"""
    payload = {
        "name": "rack-delete",
        "bgp_number": "65006",
        "as_number": 65006,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/racks", payload, format="json")
    rack_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/racks/{rack_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/racks/{rack_id}")
    assert r.status_code == 404
