import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_fabrication(auth_client):
    # Create
    payload = {"name": "fab-a", "old_system_id": "legacy-1"}
    r = auth_client.post("/api/v1/fabrications", payload, format="json")
    assert r.status_code == 201
    fab_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/fabrications")
    assert r.status_code == 200
    assert (
        any(item["id"] == fab_id for item in r.data.get("results", []))
        if isinstance(r.data, dict)
        else True
    )

    # Retrieve
    r = auth_client.get(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code == 200
    assert r.data["name"] == "fab-a"

    # Update
    r = auth_client.patch(
        f"/api/v1/fabrications/{fab_id}", {"old_system_id": "legacy-2"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["old_system_id"] == "legacy-2"

    # Delete
    r = auth_client.delete(f"/api/v1/fabrications/{fab_id}")
    assert r.status_code in (204, 200)


@pytest.mark.django_db
def test_crud_phase(auth_client):
    payload = {"name": "phase-1", "old_system_id": "p-1"}
    r = auth_client.post("/api/v1/phases", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/phases/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/phases/{obj_id}", {"old_system_id": "p-2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/phases/{obj_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_data_center(auth_client):
    payload = {"name": "DC1", "old_system_id": "d-1"}
    r = auth_client.post("/api/v1/data-centers", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/data-centers/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/data-centers/{obj_id}", {"old_system_id": "d-2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/data-centers/{obj_id}").status_code in (
        204,
        200,
    )


@pytest.mark.django_db
def test_crud_room(auth_client):
    payload = {"name": "R1", "old_system_id": "r-1"}
    r = auth_client.post("/api/v1/rooms", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/rooms/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/rooms/{obj_id}", {"old_system_id": "r-2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/rooms/{obj_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_rack(auth_client):
    payload = {
        "name": "RACK-A",
        "bgp_number": "65000",
        "as_number": 65000,
        "old_system_id": "rack-1",
        "height_units": 42,
        "power_capacity": "5.50",
        "status": "active",
    }
    r = auth_client.post("/api/v1/racks", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/racks/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/racks/{obj_id}", {"status": "maintenance"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/racks/{obj_id}").status_code in (204, 200)
