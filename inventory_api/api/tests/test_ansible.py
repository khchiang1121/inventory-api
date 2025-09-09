import pytest
from django.contrib.contenttypes.models import ContentType

# ============================================================================
# ANSIBLE GROUP TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_group_create(auth_client):
    """Test creating an Ansible group"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-group-create",
            "description": "Test inventory for group creation",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "webservers-create",
        "description": "Web server group",
        "is_special": False,
        "status": "active",
    }
    r = auth_client.post("/api/v1/ansible-groups", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "webservers-create"
    assert r.data["is_special"] is False


@pytest.mark.django_db
def test_ansible_group_list(auth_client):
    """Test listing Ansible groups"""
    r = auth_client.get("/api/v1/ansible-groups")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_group_retrieve(auth_client):
    """Test retrieving a specific Ansible group"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-group-retrieve",
            "description": "Test inventory for group retrieval",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "dbservers-retrieve",
        "description": "Database server group",
        "is_special": False,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-groups", payload, format="json")
    group_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-groups/{group_id}")
    assert r.status_code == 200
    assert r.data["name"] == "dbservers-retrieve"
    assert r.data["description"] == "Database server group"


@pytest.mark.django_db
def test_ansible_group_update_put(auth_client):
    """Test updating an Ansible group with PUT"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-group-put",
            "description": "Test inventory for group PUT update",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "appservers-put",
        "description": "Application server group",
        "is_special": False,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-groups", payload, format="json")
    group_id = create_r.data["id"]

    put_payload = {
        "inventory": inventory["id"],
        "name": "appservers-put-updated",
        "description": "Updated application server group",
        "is_special": True,
        "status": "inactive",
    }
    r = auth_client.put(f"/api/v1/ansible-groups/{group_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "appservers-put-updated"
    assert r.data["description"] == "Updated application server group"
    assert r.data["is_special"] is True

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-groups/{group_id}")
    assert r.status_code == 200
    assert r.data["name"] == "appservers-put-updated"
    assert r.data["is_special"] is True


@pytest.mark.django_db
def test_ansible_group_update_patch(auth_client):
    """Test updating an Ansible group with PATCH"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-group-patch",
            "description": "Test inventory for group PATCH update",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "loadbalancers-patch",
        "description": "Load balancer group",
        "is_special": False,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-groups", payload, format="json")
    group_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-groups/{group_id}", {"status": "inactive"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "loadbalancers-patch"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-groups/{group_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "loadbalancers-patch"


@pytest.mark.django_db
def test_ansible_group_delete(auth_client):
    """Test deleting an Ansible group"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-group-delete",
            "description": "Test inventory for group deletion",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "tempgroup-delete",
        "description": "Temporary group",
        "is_special": False,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-groups", payload, format="json")
    group_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-groups/{group_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-groups/{group_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE GROUP VARIABLES TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_group_variables_create(auth_client):
    """Test creating Ansible group variables"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-vars-create",
            "description": "Test inventory for group variables creation",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-vars-create",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "key": "environment",
        "value": "production",
        "value_type": "string",
    }
    r = auth_client.post("/api/v1/ansible-group-variables", payload, format="json")
    assert r.status_code == 201
    assert r.data["key"] == "environment"
    assert r.data["value"] == "production"
    assert r.data["value_type"] == "string"


@pytest.mark.django_db
def test_ansible_group_variables_list(auth_client):
    """Test listing Ansible group variables"""
    r = auth_client.get("/api/v1/ansible-group-variables")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_group_variables_retrieve(auth_client):
    """Test retrieving specific Ansible group variables"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-vars-retrieve",
            "description": "Test inventory for group variables retrieval",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-vars-retrieve",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "key": "debug_mode",
        "value": "false",
        "value_type": "boolean",
    }
    create_r = auth_client.post("/api/v1/ansible-group-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "debug_mode"
    assert r.data["value"] == "false"
    assert r.data["value_type"] == "boolean"


@pytest.mark.django_db
def test_ansible_group_variables_update_put(auth_client):
    """Test updating Ansible group variables with PUT"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-vars-put",
            "description": "Test inventory for group variables PUT update",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-vars-put",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "key": "max_connections",
        "value": "100",
        "value_type": "integer",
    }
    create_r = auth_client.post("/api/v1/ansible-group-variables", payload, format="json")
    var_id = create_r.data["id"]

    put_payload = {
        "group": group["id"],
        "key": "max_connections_updated",
        "value": "200",
        "value_type": "integer",
    }
    r = auth_client.put(f"/api/v1/ansible-group-variables/{var_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["key"] == "max_connections_updated"
    assert r.data["value"] == "200"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "max_connections_updated"
    assert r.data["value"] == "200"


@pytest.mark.django_db
def test_ansible_group_variables_update_patch(auth_client):
    """Test updating Ansible group variables with PATCH"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-vars-patch",
            "description": "Test inventory for group variables PATCH update",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-vars-patch",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "key": "timeout",
        "value": "30",
        "value_type": "integer",
    }
    create_r = auth_client.post("/api/v1/ansible-group-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-group-variables/{var_id}", {"value": "60"}, format="json"
    )
    assert r.status_code == 200
    assert r.data["value"] == "60"
    assert r.data["key"] == "timeout"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["value"] == "60"
    assert r.data["key"] == "timeout"


@pytest.mark.django_db
def test_ansible_group_variables_delete(auth_client):
    """Test deleting Ansible group variables"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-vars-delete",
            "description": "Test inventory for group variables deletion",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-vars-delete",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "group": group["id"],
        "key": "temp_var",
        "value": "temp_value",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-group-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-group-variables/{var_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE GROUP RELATIONSHIPS TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_group_relationships_create(auth_client):
    """Test creating Ansible group relationships"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-rel-create",
            "description": "Test inventory for group relationships creation",
            "status": "active",
        },
        format="json",
    ).data

    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-rel-create",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    child_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "web-rel-create",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group["id"],
    }
    r = auth_client.post("/api/v1/ansible-group-relationships", payload, format="json")
    assert r.status_code == 201
    assert str(r.data["parent_group"]) == str(parent_group["id"])
    assert str(r.data["child_group"]) == str(child_group["id"])


@pytest.mark.django_db
def test_ansible_group_relationships_list(auth_client):
    """Test listing Ansible group relationships"""
    r = auth_client.get("/api/v1/ansible-group-relationships")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_group_relationships_retrieve(auth_client):
    """Test retrieving specific Ansible group relationships"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-rel-retrieve",
            "description": "Test inventory for group relationships retrieval",
            "status": "active",
        },
        format="json",
    ).data

    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-rel-retrieve",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    child_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "db-rel-retrieve",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group["id"],
    }
    create_r = auth_client.post("/api/v1/ansible-group-relationships", payload, format="json")
    rel_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code == 200
    assert str(r.data["parent_group"]) == str(parent_group["id"])
    assert str(r.data["child_group"]) == str(child_group["id"])


@pytest.mark.django_db
def test_ansible_group_relationships_update_put(auth_client):
    """Test updating Ansible group relationships with PUT"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-rel-put",
            "description": "Test inventory for group relationships PUT update",
            "status": "active",
        },
        format="json",
    ).data

    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-rel-put",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    child_group1 = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "app-rel-put-1",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    child_group2 = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "app-rel-put-2",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group1["id"],
    }
    create_r = auth_client.post("/api/v1/ansible-group-relationships", payload, format="json")
    rel_id = create_r.data["id"]

    put_payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group2["id"],
    }
    r = auth_client.put(
        f"/api/v1/ansible-group-relationships/{rel_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert str(r.data["child_group"]) == str(child_group2["id"])

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code == 200
    assert str(r.data["child_group"]) == str(child_group2["id"])


@pytest.mark.django_db
def test_ansible_group_relationships_update_patch(auth_client):
    """Test updating Ansible group relationships with PATCH"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-rel-patch",
            "description": "Test inventory for group relationships PATCH update",
            "status": "active",
        },
        format="json",
    ).data

    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-rel-patch",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    child_group1 = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "lb-rel-patch-1",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    child_group2 = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "lb-rel-patch-2",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group1["id"],
    }
    create_r = auth_client.post("/api/v1/ansible-group-relationships", payload, format="json")
    rel_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-group-relationships/{rel_id}",
        {"child_group": child_group2["id"]},
        format="json",
    )
    assert r.status_code == 200
    assert str(r.data["child_group"]) == str(child_group2["id"])
    assert str(r.data["parent_group"]) == str(parent_group["id"])  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code == 200
    assert str(r.data["child_group"]) == str(child_group2["id"])
    assert str(r.data["parent_group"]) == str(parent_group["id"])


@pytest.mark.django_db
def test_ansible_group_relationships_delete(auth_client):
    """Test deleting Ansible group relationships"""
    # First create an inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-rel-delete",
            "description": "Test inventory for group relationships deletion",
            "status": "active",
        },
        format="json",
    ).data

    parent_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "all-rel-delete",
            "description": "",
            "is_special": True,
            "status": "active",
        },
        format="json",
    ).data

    child_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "temp-rel-delete",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "parent_group": parent_group["id"],
        "child_group": child_group["id"],
    }
    create_r = auth_client.post("/api/v1/ansible-group-relationships", payload, format="json")
    rel_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-group-relationships/{rel_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE HOST TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_host_create_for_vm(auth_client):
    """Test creating an Ansible host for a VM"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "t-ansible-host", "status": "active"}, format="json"
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "small",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible-host",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create inventory and group required by AnsibleHost
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-host-create",
            "description": "Test inventory for host creation",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "web",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.100",
        "ansible_port": 22,
        "ansible_user": "ubuntu",
    }
    r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    assert r.status_code == 201
    assert r.data["ansible_host"] == "192.168.1.100"
    assert r.data["ansible_port"] == 22
    assert r.data["ansible_user"] == "ubuntu"


@pytest.mark.django_db
def test_ansible_host_list(auth_client):
    """Test listing Ansible hosts"""
    r = auth_client.get("/api/v1/ansible-hosts")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_host_retrieve(auth_client):
    """Test retrieving a specific Ansible host"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "t-ansible-retrieve", "status": "active"},
        format="json",
    ).data

    # Create spec and VM correctly
    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "medium",
            "generation": "gen1",
            "required_cpu": 4,
            "required_memory": 8,
            "required_storage": 100,
        },
        format="json",
    ).data

    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible-retrieve",
            "type": "control-plane",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create inventory and group required by AnsibleHost
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-host-retrieve",
            "description": "Test inventory for host retrieval",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "db",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.101",
        "ansible_port": 22,
        "ansible_user": "admin",
    }
    create_r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    host_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-hosts/{host_id}")
    assert r.status_code == 200
    assert r.data["ansible_host"] == "192.168.1.101"
    assert r.data["ansible_user"] == "admin"


@pytest.mark.django_db
def test_ansible_host_update_put(auth_client):
    """Test updating an Ansible host with PUT"""
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "t-ansible-put", "status": "active"}, format="json"
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "small-put",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible-put",
            "type": "management",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create inventory and group required by AnsibleHost
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-host-put",
            "description": "Test inventory for host PUT update",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "ops",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.102",
        "ansible_port": 22,
        "ansible_user": "root",
    }
    create_r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    host_id = create_r.data["id"]

    put_payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.200",
        "ansible_port": 2222,
        "ansible_user": "ubuntu",
    }
    r = auth_client.put(f"/api/v1/ansible-hosts/{host_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["ansible_host"] == "192.168.1.200"
    assert r.data["ansible_port"] == 2222
    assert r.data["ansible_user"] == "ubuntu"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-hosts/{host_id}")
    assert r.status_code == 200
    assert r.data["ansible_host"] == "192.168.1.200"


@pytest.mark.django_db
def test_ansible_host_update_patch(auth_client):
    """Test updating an Ansible host with PATCH"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "t-ansible-patch", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "tiny-patch",
            "generation": "gen1",
            "required_cpu": 1,
            "required_memory": 2,
            "required_storage": 25,
        },
        format="json",
    ).data

    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible-patch",
            "type": "other",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create inventory and group required by AnsibleHost
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-host-patch",
            "description": "Test inventory for host PATCH update",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "ops-patch",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.103",
        "ansible_port": 22,
        "ansible_user": "centos",
    }
    create_r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    host_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-hosts/{host_id}",
        {"ansible_user": "centos-updated"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["ansible_user"] == "centos-updated"
    assert r.data["ansible_host"] == "192.168.1.103"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-hosts/{host_id}")
    assert r.status_code == 200
    assert r.data["ansible_user"] == "centos-updated"


@pytest.mark.django_db
def test_ansible_host_delete(auth_client):
    """Test deleting an Ansible host"""
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "t-ansible-delete", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "bastion-spec-del",
            "generation": "gen1",
            "required_cpu": 2,
            "required_memory": 4,
            "required_storage": 50,
        },
        format="json",
    ).data

    vm = auth_client.post(
        "/api/v1/virtual-machines",
        {
            "name": "vm-ansible-delete",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create inventory and group required by AnsibleHost
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "test-inventory-host-delete",
            "description": "Test inventory for host deletion",
            "status": "active",
        },
        format="json",
    ).data

    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "ops-del",
            "description": "",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    payload = {
        "inventory": inventory["id"],
        "group": group["id"],
        "content_type": ct.id,
        "object_id": vm["id"],
        "ansible_host": "192.168.1.104",
        "ansible_port": 22,
        "ansible_user": "debian",
    }
    create_r = auth_client.post("/api/v1/ansible-hosts", payload, format="json")
    host_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-hosts/{host_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-hosts/{host_id}")
    assert r.status_code == 404
