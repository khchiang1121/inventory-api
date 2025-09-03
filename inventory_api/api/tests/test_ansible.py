import pytest
from django.contrib.contenttypes.models import ContentType

from .base import auth_client


@pytest.mark.django_db
def test_ansible_group_and_variables(auth_client):
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {"name": "all", "description": "", "is_special": True, "status": "active"},
        format="json",
    ).data
    assert group["id"]

    # create variable
    var = auth_client.post(
        "/api/v1/ansible-group-variables",
        {"group": group["id"], "key": "env", "value": "prod", "value_type": "string"},
        format="json",
    ).data
    assert var["id"]

    # nested group
    child = auth_client.post(
        "/api/v1/ansible-groups",
        {"name": "web", "description": "", "is_special": False, "status": "active"},
        format="json",
    ).data
    rel = auth_client.post(
        "/api/v1/ansible-group-relationships",
        {"parent_group": group["id"], "child_group": child["id"]},
        format="json",
    ).data
    assert rel["id"]

    # list derived fields
    g = auth_client.get(f"/api/v1/ansible-groups/{group['id']}")
    assert g.status_code == 200
    assert "all_variables" in g.data
    assert "child_groups" in g.data


@pytest.mark.django_db
def test_ansible_host_for_vm(auth_client):
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "t-ansible", "status": "active"}, format="json"
    ).data
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "s2",
            "generation": "g1",
            "required_cpu": 1,
            "required_memory": 1,
            "required_storage": 1,
        },
        format="json",
    ).data
    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible",
            "tenant": tenant["id"],
            "specification": spec["id"],
            "type": "other",
            "status": "running",
        },
        format="json",
    ).data
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {"name": "vmgrp", "description": "", "is_special": False, "status": "active"},
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "host_vars": {"env": "dev"},
    }
    r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_ansible_group_variables_crud_complete(auth_client):
    """Test complete CRUD operations for ansible group variables"""
    # Setup group dependency
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "name": "webservers",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create
    var_data = {
        "group": group["id"],
        "key": "http_port",
        "value": "80",
        "value_type": "integer",
    }
    r = auth_client.post("/api/v1/ansible-group-variables", var_data, format="json")
    assert r.status_code == 201
    var_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/ansible-group-variables")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "http_port"

    # Full Update (PUT)
    put_data = {
        "group": group["id"],
        "key": "https_port",
        "value": "443",
        "value_type": "integer",
    }
    r = auth_client.put(
        f"/api/v1/ansible-group-variables/{var_id}", put_data, format="json"
    )
    assert r.status_code == 200
    assert r.data["key"] == "https_port"

    # Partial Update (PATCH)
    r = auth_client.patch(
        f"/api/v1/ansible-group-variables/{var_id}", {"value": "8443"}, format="json"
    )
    assert r.status_code == 200

    # Delete
    assert auth_client.delete(
        f"/api/v1/ansible-group-variables/{var_id}"
    ).status_code in (204, 200)


@pytest.mark.django_db
def test_ansible_group_relationships_crud_complete(auth_client):
    """Test complete CRUD operations for ansible group relationships"""
    # Setup group dependencies
    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "name": "all_servers",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data
    child_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "name": "web_servers",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create
    rel_data = {"parent_group": parent_group["id"], "child_group": child_group["id"]}
    r = auth_client.post("/api/v1/ansible-group-relationships", rel_data, format="json")
    assert r.status_code == 201
    rel_id = r.data["id"]

    # List
    r = auth_client.get("/api/v1/ansible-group-relationships")
    assert r.status_code == 200

    # Retrieve
    r = auth_client.get(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code == 200

    # Full Update (PUT) - change child group
    new_child = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "name": "db_servers",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data
    put_data = {"parent_group": parent_group["id"], "child_group": new_child["id"]}
    r = auth_client.put(
        f"/api/v1/ansible-group-relationships/{rel_id}", put_data, format="json"
    )
    assert r.status_code == 200

    # Delete
    assert auth_client.delete(
        f"/api/v1/ansible-group-relationships/{rel_id}"
    ).status_code in (204, 200)
