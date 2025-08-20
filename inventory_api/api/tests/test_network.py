import pytest

from .base import auth_client


@pytest.mark.django_db
def test_crud_vlan(auth_client):
    r = auth_client.post(
        "/api/v1/vlans", {"vlan_id": 10, "name": "vlan10"}, format="json"
    )
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/vlans/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/vlans/{obj_id}", {"name": "vlan10-dev"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/vlans/{obj_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_vrf(auth_client):
    r = auth_client.post(
        "/api/v1/vrfs",
        {"name": "vrf-a", "route_distinguisher": "65000:1"},
        format="json",
    )
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/vrfs/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/vrfs/{obj_id}", {"route_distinguisher": "65000:2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/vrfs/{obj_id}").status_code in (204, 200)


@pytest.mark.django_db
def test_crud_bgp_config(auth_client):
    payload = {
        "asn": 65000,
        "peer_ip": "192.168.0.1",
        "local_ip": "192.168.0.2",
        "password": "pw",
    }
    r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    assert r.status_code == 201
    obj_id = r.data["id"]
    assert auth_client.get(f"/api/v1/bgp-configs/{obj_id}").status_code == 200
    assert (
        auth_client.patch(
            f"/api/v1/bgp-configs/{obj_id}", {"password": "pw2"}, format="json"
        ).status_code
        == 200
    )
    assert auth_client.delete(f"/api/v1/bgp-configs/{obj_id}").status_code in (204, 200)
