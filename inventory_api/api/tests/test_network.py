import pytest

# ============================================================================
# VLAN TESTS
# ============================================================================


@pytest.mark.django_db
def test_vlan_create(auth_client):
    """Test creating a VLAN"""
    payload = {"vlan_id": 100, "name": "vlan-create"}
    r = auth_client.post("/api/v1/vlans", payload, format="json")
    assert r.status_code == 201
    assert r.data["vlan_id"] == 100
    assert r.data["name"] == "vlan-create"


@pytest.mark.django_db
def test_vlan_list(auth_client):
    """Test listing VLANs"""
    r = auth_client.get("/api/v1/vlans")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_vlan_retrieve(auth_client):
    """Test retrieving a specific VLAN"""
    payload = {"vlan_id": 101, "name": "vlan-retrieve"}
    create_r = auth_client.post("/api/v1/vlans", payload, format="json")
    vlan_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/vlans/{vlan_id}")
    assert r.status_code == 200
    assert r.data["vlan_id"] == 101
    assert r.data["name"] == "vlan-retrieve"


@pytest.mark.django_db
def test_vlan_update_put(auth_client):
    """Test updating a VLAN with PUT"""
    payload = {"vlan_id": 102, "name": "vlan-put"}
    create_r = auth_client.post("/api/v1/vlans", payload, format="json")
    vlan_id = create_r.data["id"]

    put_payload = {"vlan_id": 103, "name": "vlan-put-updated"}
    r = auth_client.put(f"/api/v1/vlans/{vlan_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "vlan-put-updated"
    assert r.data["vlan_id"] == 103

    # Verify in database
    r = auth_client.get(f"/api/v1/vlans/{vlan_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vlan-put-updated"
    assert r.data["vlan_id"] == 103


@pytest.mark.django_db
def test_vlan_update_patch(auth_client):
    """Test updating a VLAN with PATCH"""
    payload = {"vlan_id": 104, "name": "vlan-patch"}
    create_r = auth_client.post("/api/v1/vlans", payload, format="json")
    vlan_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/vlans/{vlan_id}", {"name": "vlan-patch-updated"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "vlan-patch-updated"
    assert r.data["vlan_id"] == 104  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/vlans/{vlan_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vlan-patch-updated"
    assert r.data["vlan_id"] == 104


@pytest.mark.django_db
def test_vlan_delete(auth_client):
    """Test deleting a VLAN"""
    payload = {"vlan_id": 105, "name": "vlan-delete"}
    create_r = auth_client.post("/api/v1/vlans", payload, format="json")
    vlan_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/vlans/{vlan_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/vlans/{vlan_id}")
    assert r.status_code == 404


# ============================================================================
# VRF TESTS
# ============================================================================


@pytest.mark.django_db
def test_vrf_create(auth_client):
    """Test creating a VRF"""
    payload = {"name": "vrf-create", "route_distinguisher": "65000:100"}
    r = auth_client.post("/api/v1/vrfs", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "vrf-create"
    assert r.data["route_distinguisher"] == "65000:100"


@pytest.mark.django_db
def test_vrf_list(auth_client):
    """Test listing VRFs"""
    r = auth_client.get("/api/v1/vrfs")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_vrf_retrieve(auth_client):
    """Test retrieving a specific VRF"""
    payload = {"name": "vrf-retrieve", "route_distinguisher": "65000:101"}
    create_r = auth_client.post("/api/v1/vrfs", payload, format="json")
    vrf_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/vrfs/{vrf_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vrf-retrieve"
    assert r.data["route_distinguisher"] == "65000:101"


@pytest.mark.django_db
def test_vrf_update_put(auth_client):
    """Test updating a VRF with PUT"""
    payload = {"name": "vrf-put", "route_distinguisher": "65000:102"}
    create_r = auth_client.post("/api/v1/vrfs", payload, format="json")
    vrf_id = create_r.data["id"]

    put_payload = {"name": "vrf-put-updated", "route_distinguisher": "65000:103"}
    r = auth_client.put(f"/api/v1/vrfs/{vrf_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "vrf-put-updated"
    assert r.data["route_distinguisher"] == "65000:103"

    # Verify in database
    r = auth_client.get(f"/api/v1/vrfs/{vrf_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vrf-put-updated"
    assert r.data["route_distinguisher"] == "65000:103"


@pytest.mark.django_db
def test_vrf_update_patch(auth_client):
    """Test updating a VRF with PATCH"""
    payload = {"name": "vrf-patch", "route_distinguisher": "65000:104"}
    create_r = auth_client.post("/api/v1/vrfs", payload, format="json")
    vrf_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/vrfs/{vrf_id}", {"name": "vrf-patch-updated"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "vrf-patch-updated"
    assert r.data["route_distinguisher"] == "65000:104"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/vrfs/{vrf_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vrf-patch-updated"
    assert r.data["route_distinguisher"] == "65000:104"


@pytest.mark.django_db
def test_vrf_delete(auth_client):
    """Test deleting a VRF"""
    payload = {"name": "vrf-delete", "route_distinguisher": "65000:105"}
    create_r = auth_client.post("/api/v1/vrfs", payload, format="json")
    vrf_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/vrfs/{vrf_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/vrfs/{vrf_id}")
    assert r.status_code == 404


# ============================================================================
# BGP CONFIG TESTS
# ============================================================================


@pytest.mark.django_db
def test_bgp_config_create(auth_client):
    """Test creating a BGP config"""
    payload = {
        "asn": 65001,
        "peer_ip": "192.168.1.1",
        "local_ip": "192.168.1.2",
    }
    r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    assert r.status_code == 201
    assert r.data["asn"] == 65001
    assert r.data["peer_ip"] == "192.168.1.1"
    assert r.data["local_ip"] == "192.168.1.2"


@pytest.mark.django_db
def test_bgp_config_list(auth_client):
    """Test listing BGP configs"""
    r = auth_client.get("/api/v1/bgp-configs")
    assert r.status_code == 200
    assert "results" in r.data or isinstance(r.data, list)


@pytest.mark.django_db
def test_bgp_config_retrieve(auth_client):
    """Test retrieving a specific BGP config"""
    payload = {
        "asn": 65003,
        "peer_ip": "192.168.1.2",
        "local_ip": "192.168.1.3",
    }
    create_r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    bgp_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/bgp-configs/{bgp_id}")
    assert r.status_code == 200
    assert r.data["asn"] == 65003
    assert r.data["peer_ip"] == "192.168.1.2"
    assert r.data["local_ip"] == "192.168.1.3"


@pytest.mark.django_db
def test_bgp_config_update_put(auth_client):
    """Test updating a BGP config with PUT"""
    payload = {
        "asn": 65005,
        "peer_ip": "192.168.1.3",
        "local_ip": "192.168.1.4",
    }
    create_r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    bgp_id = create_r.data["id"]

    put_payload = {
        "asn": 65007,
        "peer_ip": "192.168.1.4",
        "local_ip": "192.168.1.5",
    }
    r = auth_client.put(f"/api/v1/bgp-configs/{bgp_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["asn"] == 65007
    assert r.data["peer_ip"] == "192.168.1.4"
    assert r.data["local_ip"] == "192.168.1.5"

    # Verify in database
    r = auth_client.get(f"/api/v1/bgp-configs/{bgp_id}")
    assert r.status_code == 200
    assert r.data["asn"] == 65007
    assert r.data["local_ip"] == "192.168.1.5"


@pytest.mark.django_db
def test_bgp_config_update_patch(auth_client):
    """Test updating a BGP config with PATCH"""
    payload = {
        "asn": 65009,
        "peer_ip": "192.168.1.5",
        "local_ip": "192.168.1.6",
    }
    create_r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    bgp_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/bgp-configs/{bgp_id}",
        {"peer_ip": "192.168.1.100"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["local_ip"] == "192.168.1.6"
    assert r.data["asn"] == 65009  # Should remain unchanged
    assert r.data["peer_ip"] == "192.168.1.100"  # Should be updated

    # Verify in database
    r = auth_client.get(f"/api/v1/bgp-configs/{bgp_id}")
    assert r.status_code == 200
    assert r.data["local_ip"] == "192.168.1.6"
    assert r.data["asn"] == 65009


@pytest.mark.django_db
def test_bgp_config_delete(auth_client):
    """Test deleting a BGP config"""
    payload = {
        "asn": 65011,
        "peer_ip": "192.168.1.6",
        "local_ip": "192.168.1.7",
    }
    create_r = auth_client.post("/api/v1/bgp-configs", payload, format="json")
    bgp_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/bgp-configs/{bgp_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/bgp-configs/{bgp_id}")
    assert r.status_code == 404
