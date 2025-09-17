import pytest

# ============================================================================
# FABRICATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_fabrication_create(auth_client):
    """Test creating a fabrication"""
    payload = {"name": "fab-create", "external_system_id": "legacy-create"}
    r = auth_client.post("/api/v1/fabrications", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "fab-create"
    assert r.data["external_system_id"] == "legacy-create"


@pytest.mark.django_db
def test_fabrication_list(auth_client):
    """Test listing fabrications"""
    r = auth_client.get("/api/v1/fabrications")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_fabrication_retrieve(auth_client):
    """Test retrieving a specific fabrication"""
    payload = {"name": "fab-retrieve", "external_system_id": "legacy-retrieve"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["name"] == "fab-retrieve"
    assert r.data["external_system_id"] == "legacy-retrieve"


@pytest.mark.django_db
def test_fabrication_update_put(auth_client):
    """Test updating a fabrication with PUT"""
    payload = {"name": "fab-put", "external_system_id": "legacy-put"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    put_payload = {"name": "fab-put-updated", "external_system_id": "legacy-put-updated"}
    r = auth_client.put(f"/api/v1/fabrications/{fab_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "fab-put-updated"
    assert r.data["external_system_id"] == "legacy-put-updated"

    # Verify in database
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["name"] == "fab-put-updated"
    assert r.data["external_system_id"] == "legacy-put-updated"


@pytest.mark.django_db
def test_fabrication_update_patch(auth_client):
    """Test updating a fabrication with PATCH"""
    payload = {"name": "fab-patch", "external_system_id": "legacy-patch"}
    create_r = auth_client.post("/api/v1/fabrications", payload, format="json")
    fab_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/fabrications/{fab_id}",
        {"external_system_id": "legacy-patch-updated"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["external_system_id"] == "legacy-patch-updated"
    assert r.data["name"] == "fab-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["external_system_id"] == "legacy-patch-updated"
    assert r.data["name"] == "fab-patch"


@pytest.mark.django_db
def test_fabrication_delete(auth_client):
    """Test deleting a fabrication"""
    payload = {"name": "fab-delete", "external_system_id": "legacy-delete"}
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

    r = auth_client.patch(f"/api/v1/racks/{rack_id}", {"status": "maintenance"}, format="json")
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


# ============================================================================
# UNIT TESTS
# ============================================================================


@pytest.mark.django_db
def test_unit_create(auth_client):
    """Test creating a unit"""
    # First create a rack to associate the unit with
    rack_payload = {
        "name": "rack-for-unit",
        "bgp_number": "65010",
        "as_number": 65010,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    assert rack_r.status_code == 201
    rack_id = rack_r.data["id"]

    # Now create a unit
    unit_payload = {"rack": rack_id, "name": "U1"}
    r = auth_client.post("/api/v1/units", unit_payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "U1"
    assert str(r.data["rack"]) == str(rack_id)
    assert "id" in r.data


@pytest.mark.django_db
def test_unit_list(auth_client):
    """Test listing units"""
    r = auth_client.get("/api/v1/units")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_unit_retrieve(auth_client):
    """Test retrieving a specific unit"""
    # First create a rack
    rack_payload = {
        "name": "rack-for-retrieve",
        "bgp_number": "65011",
        "as_number": 65011,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create a unit
    unit_payload = {"rack": rack_id, "name": "U2"}
    create_r = auth_client.post("/api/v1/units", unit_payload, format="json")
    unit_id = create_r.data["id"]

    # Retrieve the unit
    r = auth_client.get(f"/api/v1/units/{unit_id}")
    assert r.status_code == 200
    assert r.data["name"] == "U2"
    assert str(r.data["rack"]) == str(rack_id)


@pytest.mark.django_db
def test_unit_update_put(auth_client):
    """Test updating a unit with PUT"""
    # First create a rack
    rack_payload = {
        "name": "rack-for-put",
        "bgp_number": "65012",
        "as_number": 65012,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create another rack for updating
    rack2_payload = {
        "name": "rack-for-put-2",
        "bgp_number": "65013",
        "as_number": 65013,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack2_r = auth_client.post("/api/v1/racks", rack2_payload, format="json")
    rack2_id = rack2_r.data["id"]

    # Create a unit
    unit_payload = {"rack": rack_id, "name": "U3"}
    create_r = auth_client.post("/api/v1/units", unit_payload, format="json")
    unit_id = create_r.data["id"]

    # Update with PUT
    put_payload = {"rack": rack2_id, "name": "U3-updated"}
    r = auth_client.put(f"/api/v1/units/{unit_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "U3-updated"
    assert str(r.data["rack"]) == str(rack2_id)

    # Verify in database
    r = auth_client.get(f"/api/v1/units/{unit_id}")
    assert r.status_code == 200
    assert r.data["name"] == "U3-updated"
    assert str(r.data["rack"]) == str(rack2_id)


@pytest.mark.django_db
def test_unit_update_patch(auth_client):
    """Test updating a unit with PATCH"""
    # First create a rack
    rack_payload = {
        "name": "rack-for-patch",
        "bgp_number": "65014",
        "as_number": 65014,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create a unit
    unit_payload = {"rack": rack_id, "name": "U4"}
    create_r = auth_client.post("/api/v1/units", unit_payload, format="json")
    unit_id = create_r.data["id"]

    # Update with PATCH (only name)
    r = auth_client.patch(f"/api/v1/units/{unit_id}", {"name": "U4-patched"}, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "U4-patched"
    assert str(r.data["rack"]) == str(rack_id)  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/units/{unit_id}")
    assert r.status_code == 200
    assert r.data["name"] == "U4-patched"
    assert str(r.data["rack"]) == str(rack_id)


@pytest.mark.django_db
def test_unit_delete(auth_client):
    """Test deleting a unit"""
    # First create a rack
    rack_payload = {
        "name": "rack-for-delete",
        "bgp_number": "65015",
        "as_number": 65015,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create a unit
    unit_payload = {"rack": rack_id, "name": "U5"}
    create_r = auth_client.post("/api/v1/units", unit_payload, format="json")
    unit_id = create_r.data["id"]

    # Delete the unit
    r = auth_client.delete(f"/api/v1/units/{unit_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/units/{unit_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_unit_unique_constraint(auth_client):
    """Test that rack + name combination must be unique"""
    # First create a rack
    rack_payload = {
        "name": "rack-for-unique",
        "bgp_number": "65016",
        "as_number": 65016,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create first unit
    unit_payload = {"rack": rack_id, "name": "U10"}
    r1 = auth_client.post("/api/v1/units", unit_payload, format="json")
    assert r1.status_code == 201

    # Try to create another unit with same rack + name (should fail)
    r2 = auth_client.post("/api/v1/units", unit_payload, format="json")
    assert r2.status_code == 400  # Should fail due to unique constraint


@pytest.mark.django_db
def test_unit_same_name_different_racks(auth_client):
    """Test that same unit name can exist in different racks"""
    # Create first rack
    rack1_payload = {
        "name": "rack-1-for-same-name",
        "bgp_number": "65017",
        "as_number": 65017,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack1_r = auth_client.post("/api/v1/racks", rack1_payload, format="json")
    rack1_id = rack1_r.data["id"]

    # Create second rack
    rack2_payload = {
        "name": "rack-2-for-same-name",
        "bgp_number": "65018",
        "as_number": 65018,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack2_r = auth_client.post("/api/v1/racks", rack2_payload, format="json")
    rack2_id = rack2_r.data["id"]

    # Create unit in first rack
    unit1_payload = {"rack": rack1_id, "name": "U1"}
    r1 = auth_client.post("/api/v1/units", unit1_payload, format="json")
    assert r1.status_code == 201

    # Create unit with same name in second rack (should succeed)
    unit2_payload = {"rack": rack2_id, "name": "U1"}
    r2 = auth_client.post("/api/v1/units", unit2_payload, format="json")
    assert r2.status_code == 201
    assert r2.data["name"] == "U1"
    assert str(r2.data["rack"]) == str(rack2_id)


@pytest.mark.django_db
def test_unit_invalid_rack(auth_client):
    """Test creating a unit with invalid rack ID"""
    import uuid

    fake_rack_id = str(uuid.uuid4())
    unit_payload = {"rack": fake_rack_id, "name": "U99"}
    r = auth_client.post("/api/v1/units", unit_payload, format="json")
    assert r.status_code == 400  # Should fail due to invalid foreign key


@pytest.mark.django_db
def test_unit_missing_required_fields(auth_client):
    """Test creating a unit with missing required fields"""
    # Test missing rack
    r1 = auth_client.post("/api/v1/units", {"name": "U100"}, format="json")
    assert r1.status_code == 400

    # Test missing name
    rack_payload = {
        "name": "rack-for-missing-fields",
        "bgp_number": "65019",
        "as_number": 65019,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    r2 = auth_client.post("/api/v1/units", {"rack": rack_id}, format="json")
    assert r2.status_code == 400


@pytest.mark.django_db
def test_unit_cascade_delete_with_rack(auth_client):
    """Test that units are deleted when their parent rack is deleted"""
    # Create a rack
    rack_payload = {
        "name": "rack-for-cascade",
        "bgp_number": "65020",
        "as_number": 65020,
        "height_units": 42,
        "power_capacity": "4.00",
        "status": "active",
    }
    rack_r = auth_client.post("/api/v1/racks", rack_payload, format="json")
    rack_id = rack_r.data["id"]

    # Create units in the rack
    unit1_payload = {"rack": rack_id, "name": "U1"}
    unit1_r = auth_client.post("/api/v1/units", unit1_payload, format="json")
    unit1_id = unit1_r.data["id"]

    unit2_payload = {"rack": rack_id, "name": "U2"}
    unit2_r = auth_client.post("/api/v1/units", unit2_payload, format="json")
    unit2_id = unit2_r.data["id"]

    # Verify units exist
    r1 = auth_client.get(f"/api/v1/units/{unit1_id}")
    assert r1.status_code == 200
    r2 = auth_client.get(f"/api/v1/units/{unit2_id}")
    assert r2.status_code == 200

    # Delete the rack
    rack_delete_r = auth_client.delete(f"/api/v1/racks/{rack_id}")
    assert rack_delete_r.status_code in (204, 200)

    # Verify units are also deleted (cascade delete)
    r1 = auth_client.get(f"/api/v1/units/{unit1_id}")
    assert r1.status_code == 404
    r2 = auth_client.get(f"/api/v1/units/{unit2_id}")
    assert r2.status_code == 404
