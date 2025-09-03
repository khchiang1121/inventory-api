import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_vlan(auth_client):
    # Create
    r = auth_client.post(
        "/api/v1/vlans", {"vlan_id": 10, "name": "vlan10"}, format="json"
    )
    assert r.status_code == 201
    obj_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/vlans")
    assert r.status_code == 200

    # Retrieve
    assert auth_client.get(f"/api/v1/vlans/{obj_id}").status_code == 200

    # Full Update (PUT)
    put_payload = {"vlan_id": 11, "name": "vlan11-updated"}
    r = auth_client.put(f"/api/v1/vlans/{obj_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "vlan11-updated"
    assert r.data["vlan_id"] == 11

    # Verify PUT in database
    r = auth_client.get(f"/api/v1/vlans/{obj_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vlan11-updated"
    assert r.data["vlan_id"] == 11

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/vlans/{obj_id}", {"name": "vlan10-dev"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "vlan10-dev"
    # VLAN ID should remain unchanged from PUT
    assert r.data["vlan_id"] == 11

    # Verify PATCH in database
    r = auth_client.get(f"/api/v1/vlans/{obj_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vlan10-dev"
    assert r.data["vlan_id"] == 11

    # Delete
    r = auth_client.delete(f"/api/v1/vlans/{obj_id}")
    assert r.status_code in (204, 200)

    # Verify deletion - should return 404
    r = auth_client.get(f"/api/v1/vlans/{obj_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_crud_vrf(auth_client):
    # Create
    r = auth_client.post(
        "/api/v1/vrfs",
        {"name": "vrf-a", "route_distinguisher": "65000:1"},
        format="json",
    )
    assert r.status_code == 201
    obj_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/vrfs")
    assert r.status_code == 200

    # Retrieve
    assert auth_client.get(f"/api/v1/vrfs/{obj_id}").status_code == 200

    # Full Update (PUT)
    put_payload = {"name": "vrf-a-updated", "route_distinguisher": "65001:1"}
    r = auth_client.put(f"/api/v1/vrfs/{obj_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "vrf-a-updated"

    # Partial Update (PATCH)
    assert (
        auth_client.patch(
            f"/api/v1/vrfs/{obj_id}", {"route_distinguisher": "65000:2"}, format="json"
        ).status_code
        == 200
    )

    # Delete
    assert auth_client.delete(f"/api/v1/vrfs/{obj_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_bgp_config(auth_client):
    # Create
    payload = {
        "asn": 65000,
        "peer_ip": "192.168.0.1",
        "local_ip": "192.168.0.2",
        "password": "pw",
    }
    r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/bgp-configs")
    assert r.status_code == 200

    # Retrieve
    assert auth_client.get(f"/api/v1/bgp-configs/{obj_id}").status_code == 200

    # Full Update (PUT)
    put_payload = {
        "asn": 65001,
        "peer_ip": "192.168.1.1",
        "local_ip": "192.168.1.2",
        "password": "newpw",
    }
    r = auth_client.put(f"/api/v1/bgp-configs/{obj_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["asn"] == 65001

    # Partial Update (PATCH)
    assert (
        auth_client.patch(
            f"/api/v1/bgp-configs/{obj_id}", {"password": "pw2"}, format="json"
        ).status_code
        == 200
    )

    # Delete
    assert auth_client.delete(f"/api/v1/bgp-configs/{obj_id}").status_code in (204, 200)
