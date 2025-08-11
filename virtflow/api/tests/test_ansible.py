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
