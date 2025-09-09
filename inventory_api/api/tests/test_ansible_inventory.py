import pytest
from django.contrib.contenttypes.models import ContentType

# ============================================================================
# ANSIBLE INVENTORY TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_inventory_create(auth_client):
    """Test creating an Ansible inventory"""
    payload = {
        "name": "production-inventory",
        "description": "Production environment inventory",
        "version": "1.0",
        "source_type": "static",
        "source_config": {},
        "status": "active",
    }
    r = auth_client.post("/api/v1/ansible-inventories", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "production-inventory"
    assert r.data["source_type"] == "static"
    assert r.data["status"] == "active"


@pytest.mark.django_db
def test_ansible_inventory_list(auth_client):
    """Test listing Ansible inventories"""
    r = auth_client.get("/api/v1/ansible-inventories")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_inventory_retrieve(auth_client):
    """Test retrieving a specific Ansible inventory"""
    payload = {
        "name": "staging-inventory",
        "description": "Staging environment inventory",
        "version": "1.0",
        "source_type": "dynamic",
        "source_plugin": "aws_ec2",
        "source_config": {"regions": ["us-west-2"]},
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventories", payload, format="json")
    inventory_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory_id}")
    assert r.status_code == 200
    assert r.data["name"] == "staging-inventory"
    assert r.data["source_type"] == "dynamic"
    assert r.data["source_plugin"] == "aws_ec2"


@pytest.mark.django_db
def test_ansible_inventory_update_put(auth_client):
    """Test updating an Ansible inventory with PUT"""
    payload = {
        "name": "dev-inventory",
        "description": "Development environment inventory",
        "version": "1.0",
        "source_type": "hybrid",
        "source_plugin": "openstack",
        "source_config": {"regions": ["us-east-1"]},
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventories", payload, format="json")
    inventory_id = create_r.data["id"]

    put_payload = {
        "name": "dev-inventory-updated",
        "description": "Updated development environment inventory",
        "version": "2.0",
        "source_type": "static",
        "source_config": {},
        "status": "inactive",
    }
    r = auth_client.put(f"/api/v1/ansible-inventories/{inventory_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "dev-inventory-updated"
    assert r.data["version"] == "2.0"
    assert r.data["status"] == "inactive"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory_id}")
    assert r.status_code == 200
    assert r.data["name"] == "dev-inventory-updated"


@pytest.mark.django_db
def test_ansible_inventory_update_patch(auth_client):
    """Test updating an Ansible inventory with PATCH"""
    payload = {
        "name": "test-inventory",
        "description": "Test environment inventory",
        "version": "1.0",
        "source_type": "static",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventories", payload, format="json")
    inventory_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-inventories/{inventory_id}",
        {"status": "inactive", "version": "1.1"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["status"] == "inactive"
    assert r.data["version"] == "1.1"
    assert r.data["name"] == "test-inventory"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory_id}")
    assert r.status_code == 200
    assert r.data["status"] == "inactive"


@pytest.mark.django_db
def test_ansible_inventory_delete(auth_client):
    """Test deleting an Ansible inventory"""
    payload = {
        "name": "temp-inventory",
        "description": "Temporary inventory",
        "version": "1.0",
        "source_type": "static",
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventories", payload, format="json")
    inventory_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-inventories/{inventory_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_ansible_inventory_merged_variables(auth_client):
    """Test getting merged variables for an inventory"""
    # Create inventory
    inventory_payload = {
        "name": "merged-test-inventory",
        "description": "Test inventory for merged variables",
        "version": "1.0",
        "source_type": "static",
        "status": "active",
    }
    inventory_r = auth_client.post("/api/v1/ansible-inventories", inventory_payload, format="json")
    inventory_id = inventory_r.data["id"]

    # Create inventory variable
    inv_var_payload = {
        "inventory": inventory_id,
        "key": "environment",
        "value": "test",
        "value_type": "string",
    }
    auth_client.post("/api/v1/ansible-inventory-variables", inv_var_payload, format="json")

    # Test merged variables endpoint
    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory_id}/merged_variables")
    assert r.status_code == 200
    assert "environment" in r.data
    assert r.data["environment"] == "test"


# ============================================================================
# ANSIBLE INVENTORY VARIABLE TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_inventory_variable_create(auth_client):
    """Test creating an Ansible inventory variable"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "var-test-inventory",
            "description": "Test inventory for variables",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "key": "app_version",
        "value": "2.1.0",
        "value_type": "string",
    }
    r = auth_client.post("/api/v1/ansible-inventory-variables", payload, format="json")
    assert r.status_code == 201
    assert r.data["key"] == "app_version"
    assert r.data["value"] == "2.1.0"
    assert r.data["value_type"] == "string"


@pytest.mark.django_db
def test_ansible_inventory_variable_list(auth_client):
    """Test listing Ansible inventory variables"""
    r = auth_client.get("/api/v1/ansible-inventory-variables")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_inventory_variable_retrieve(auth_client):
    """Test retrieving a specific Ansible inventory variable"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "var-retrieve-inventory",
            "description": "Test inventory for variable retrieval",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "key": "database_host",
        "value": "db.example.com",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-inventory-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "database_host"
    assert r.data["value"] == "db.example.com"


@pytest.mark.django_db
def test_ansible_inventory_variable_update_put(auth_client):
    """Test updating an Ansible inventory variable with PUT"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "var-put-inventory",
            "description": "Test inventory for variable PUT",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "key": "max_connections",
        "value": "100",
        "value_type": "integer",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-variables", payload, format="json")
    var_id = create_r.data["id"]

    put_payload = {
        "inventory": inventory["id"],
        "key": "max_connections_updated",
        "value": "200",
        "value_type": "integer",
    }
    r = auth_client.put(
        f"/api/v1/ansible-inventory-variables/{var_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert r.data["key"] == "max_connections_updated"
    assert r.data["value"] == "200"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "max_connections_updated"


@pytest.mark.django_db
def test_ansible_inventory_variable_update_patch(auth_client):
    """Test updating an Ansible inventory variable with PATCH"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "var-patch-inventory",
            "description": "Test inventory for variable PATCH",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "key": "timeout",
        "value": "30",
        "value_type": "integer",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-inventory-variables/{var_id}",
        {"value": "60"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["value"] == "60"
    assert r.data["key"] == "timeout"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["value"] == "60"


@pytest.mark.django_db
def test_ansible_inventory_variable_delete(auth_client):
    """Test deleting an Ansible inventory variable"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "var-delete-inventory",
            "description": "Test inventory for variable deletion",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "key": "temp_var",
        "value": "temp_value",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-inventory-variables/{var_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-inventory-variables/{var_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE VARIABLE SET TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_variable_set_create(auth_client):
    """Test creating an Ansible variable set"""
    payload = {
        "name": "common_variables",
        "description": "Common variables for all environments",
        "content": "ansible_user: ubuntu\nansible_ssh_private_key_file: ~/.ssh/id_rsa",
        "content_type": "yaml",
        "tags": ["common", "system"],
        "priority": 10,
        "status": "active",
    }
    r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "common_variables"
    assert r.data["content_type"] == "yaml"
    assert r.data["priority"] == 10
    assert "common" in r.data["tags"]


@pytest.mark.django_db
def test_ansible_variable_set_list(auth_client):
    """Test listing Ansible variable sets"""
    r = auth_client.get("/api/v1/ansible-variable-sets")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_variable_set_retrieve(auth_client):
    """Test retrieving a specific Ansible variable set"""
    payload = {
        "name": "database_variables",
        "description": "Database connection variables",
        "content": '{"database_host": "db.example.com", "database_port": 5432}',
        "content_type": "json",
        "tags": ["database", "production"],
        "priority": 20,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    var_set_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-variable-sets/{var_set_id}")
    assert r.status_code == 200
    assert r.data["name"] == "database_variables"
    assert r.data["content_type"] == "json"
    assert "database" in r.data["tags"]


@pytest.mark.django_db
def test_ansible_variable_set_update_put(auth_client):
    """Test updating an Ansible variable set with PUT"""
    payload = {
        "name": "app_variables",
        "description": "Application variables",
        "content": "app_name: myapp\napp_version: 1.0",
        "content_type": "yaml",
        "tags": ["app"],
        "priority": 15,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    var_set_id = create_r.data["id"]

    put_payload = {
        "name": "app_variables_updated",
        "description": "Updated application variables",
        "content": "app_name: myapp\napp_version: 2.0",
        "content_type": "yaml",
        "tags": ["app", "updated"],
        "priority": 25,
        "status": "inactive",
    }
    r = auth_client.put(f"/api/v1/ansible-variable-sets/{var_set_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["name"] == "app_variables_updated"
    assert r.data["priority"] == 25
    assert r.data["status"] == "inactive"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-variable-sets/{var_set_id}")
    assert r.status_code == 200
    assert r.data["name"] == "app_variables_updated"


@pytest.mark.django_db
def test_ansible_variable_set_update_patch(auth_client):
    """Test updating an Ansible variable set with PATCH"""
    payload = {
        "name": "monitoring_variables",
        "description": "Monitoring variables",
        "content": "monitoring_enabled: true\nlog_level: info",
        "content_type": "yaml",
        "tags": ["monitoring"],
        "priority": 30,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    var_set_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-variable-sets/{var_set_id}",
        {"priority": 35, "status": "inactive"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["priority"] == 35
    assert r.data["status"] == "inactive"
    assert r.data["name"] == "monitoring_variables"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-variable-sets/{var_set_id}")
    assert r.status_code == 200
    assert r.data["priority"] == 35


@pytest.mark.django_db
def test_ansible_variable_set_delete(auth_client):
    """Test deleting an Ansible variable set"""
    payload = {
        "name": "temp_variables",
        "description": "Temporary variables",
        "content": "temp: true",
        "content_type": "yaml",
        "tags": ["temp"],
        "priority": 100,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    var_set_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-variable-sets/{var_set_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-variable-sets/{var_set_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_ansible_variable_set_by_tags(auth_client):
    """Test filtering variable sets by tags"""
    # Create variable sets with different tags
    auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "common-prod-vars",
            "description": "Common production variables",
            "content": "ansible_user: ubuntu\nenvironment: production",
            "content_type": "yaml",
            "tags": ["common", "production"],
            "priority": 10,
            "status": "active",
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "common-staging-vars",
            "description": "Common staging variables",
            "content": "ansible_user: ubuntu\nenvironment: staging",
            "content_type": "yaml",
            "tags": ["common", "staging"],
            "priority": 10,
            "status": "active",
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "database-prod-vars",
            "description": "Database production variables",
            "content": '{"db_host": "prod-db.example.com", "db_port": 5432}',
            "content_type": "json",
            "tags": ["database", "production"],
            "priority": 20,
            "status": "active",
        },
        format="json",
    )

    # Test filtering by single tag
    r = auth_client.get("/api/v1/ansible-variable-sets/by_tags?tags=common")
    assert r.status_code == 200
    assert len(r.data) == 2
    names = [var_set["name"] for var_set in r.data]
    assert "common-prod-vars" in names
    assert "common-staging-vars" in names

    # Test filtering by multiple tags (AND logic - returns items with ALL of the tags)
    r = auth_client.get("/api/v1/ansible-variable-sets/by_tags?tags=common&tags=production")
    assert r.status_code == 200
    assert len(r.data) == 1  # Should return only "common-prod-vars" which has both tags
    assert r.data[0]["name"] == "common-prod-vars"

    # Test filtering by database tag
    r = auth_client.get("/api/v1/ansible-variable-sets/by_tags?tags=database")
    assert r.status_code == 200
    assert len(r.data) == 1
    assert r.data[0]["name"] == "database-prod-vars"


@pytest.mark.django_db
def test_ansible_variable_set_validate_content(auth_client):
    """Test validating variable set content"""
    # Create variable set with valid YAML
    payload = {
        "name": "valid_yaml",
        "description": "Valid YAML content",
        "content": "ansible_user: ubuntu\nansible_port: 22",
        "content_type": "yaml",
        "tags": ["test"],
        "priority": 10,
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-variable-sets", payload, format="json")
    var_set_id = create_r.data["id"]

    r = auth_client.post(f"/api/v1/ansible-variable-sets/{var_set_id}/validate_content")
    assert r.status_code == 200
    assert r.data["valid"] is True


# ============================================================================
# ANSIBLE INVENTORY VARIABLE SET ASSOCIATION TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_create(auth_client):
    """Test creating an Ansible inventory variable set association"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "association-test-inventory",
            "description": "Test inventory for associations",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set
    variable_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "association-test-vars",
            "description": "Test variables for associations",
            "content": "test: true",
            "content_type": "yaml",
            "tags": ["test"],
            "priority": 10,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 10,
        "enabled": True,
        "load_tags": [],
        "load_config": {"merge_strategy": "override"},
    }
    r = auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations", payload, format="json"
    )
    assert r.status_code == 201
    assert r.data["load_priority"] == 10
    assert r.data["enabled"] is True


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_list(auth_client):
    """Test listing Ansible inventory variable set associations"""
    r = auth_client.get("/api/v1/ansible-inventory-variable-set-associations")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_retrieve(auth_client):
    """Test retrieving a specific Ansible inventory variable set association"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "association-retrieve-inventory",
            "description": "Test inventory for association retrieval",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set
    variable_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "association-retrieve-vars",
            "description": "Test variables for association retrieval",
            "content": "retrieve: true",
            "content_type": "yaml",
            "tags": ["retrieve"],
            "priority": 15,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 15,
        "enabled": True,
        "load_tags": ["production"],
        "load_config": {"merge_strategy": "merge"},
    }
    create_r = auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations", payload, format="json"
    )
    assoc_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}")
    assert r.status_code == 200
    assert r.data["load_priority"] == 15
    assert "production" in r.data["load_tags"]


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_update_put(auth_client):
    """Test updating an Ansible inventory variable set association with PUT"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "association-put-inventory",
            "description": "Test inventory for association PUT",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set
    variable_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "association-put-vars",
            "description": "Test variables for association PUT",
            "content": "put: true",
            "content_type": "yaml",
            "tags": ["put"],
            "priority": 20,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 20,
        "enabled": True,
        "load_tags": [],
        "load_config": {},
    }
    create_r = auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations", payload, format="json"
    )
    assoc_id = create_r.data["id"]

    put_payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 25,
        "enabled": False,
        "load_tags": ["staging"],
        "load_config": {"merge_strategy": "override"},
    }
    r = auth_client.put(
        f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}",
        put_payload,
        format="json",
    )
    assert r.status_code == 200
    assert r.data["load_priority"] == 25
    assert r.data["enabled"] is False

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}")
    assert r.status_code == 200
    assert r.data["load_priority"] == 25


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_update_patch(auth_client):
    """Test updating an Ansible inventory variable set association with PATCH"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "association-patch-inventory",
            "description": "Test inventory for association PATCH",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set
    variable_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "association-patch-vars",
            "description": "Test variables for association PATCH",
            "content": "patch: true",
            "content_type": "yaml",
            "tags": ["patch"],
            "priority": 30,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 30,
        "enabled": True,
        "load_tags": [],
        "load_config": {},
    }
    create_r = auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations", payload, format="json"
    )
    assoc_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}",
        {"enabled": False, "load_priority": 35},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["enabled"] is False
    assert r.data["load_priority"] == 35

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}")
    assert r.status_code == 200
    assert r.data["enabled"] is False


@pytest.mark.django_db
def test_ansible_inventory_variable_set_association_delete(auth_client):
    """Test deleting an Ansible inventory variable set association"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "association-delete-inventory",
            "description": "Test inventory for association deletion",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set
    variable_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "association-delete-vars",
            "description": "Test variables for association deletion",
            "content": "delete: true",
            "content_type": "yaml",
            "tags": ["delete"],
            "priority": 40,
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "variable_set": variable_set["id"],
        "load_priority": 40,
        "enabled": True,
        "load_tags": [],
        "load_config": {},
    }
    create_r = auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations", payload, format="json"
    )
    assoc_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-inventory-variable-set-associations/{assoc_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE HOST VARIABLE TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_host_variable_create(auth_client):
    """Test creating an Ansible host variable"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "host-var-test-inventory",
            "description": "Test inventory for host variables",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "host-var-test-group",
            "description": "Test group for host variables",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "host-var-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "host-var-spec",
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
            "name": "host-var-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.50",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    payload = {
        "host": host["id"],
        "key": "app_port",
        "value": "8080",
        "value_type": "integer",
    }
    r = auth_client.post("/api/v1/ansible-host-variables", payload, format="json")
    assert r.status_code == 201
    assert r.data["key"] == "app_port"
    assert r.data["value"] == "8080"
    assert r.data["value_type"] == "integer"


@pytest.mark.django_db
def test_ansible_host_variable_list(auth_client):
    """Test listing Ansible host variables"""
    r = auth_client.get("/api/v1/ansible-host-variables")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_host_variable_retrieve(auth_client):
    """Test retrieving a specific Ansible host variable"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "host-var-retrieve-inventory",
            "description": "Test inventory for host variable retrieval",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "host-var-retrieve-group",
            "description": "Test group for host variable retrieval",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "host-var-retrieve-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "host-var-retrieve-spec",
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
            "name": "host-var-retrieve-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.60",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    payload = {
        "host": host["id"],
        "key": "database_url",
        "value": "postgresql://user:pass@db:5432/mydb",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-host-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-host-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "database_url"
    assert r.data["value"] == "postgresql://user:pass@db:5432/mydb"


@pytest.mark.django_db
def test_ansible_host_variable_update_put(auth_client):
    """Test updating an Ansible host variable with PUT"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "host-var-put-inventory",
            "description": "Test inventory for host variable PUT",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "host-var-put-group",
            "description": "Test group for host variable PUT",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "host-var-put-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "host-var-put-spec",
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
            "name": "host-var-put-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.70",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    payload = {
        "host": host["id"],
        "key": "max_memory",
        "value": "4GB",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-host-variables", payload, format="json")
    var_id = create_r.data["id"]

    put_payload = {
        "host": host["id"],
        "key": "max_memory_updated",
        "value": "8GB",
        "value_type": "string",
    }
    r = auth_client.put(f"/api/v1/ansible-host-variables/{var_id}", put_payload, format="json")
    assert r.status_code == 200
    assert r.data["key"] == "max_memory_updated"
    assert r.data["value"] == "8GB"

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-host-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["key"] == "max_memory_updated"


@pytest.mark.django_db
def test_ansible_host_variable_update_patch(auth_client):
    """Test updating an Ansible host variable with PATCH"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "host-var-patch-inventory",
            "description": "Test inventory for host variable PATCH",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "host-var-patch-group",
            "description": "Test group for host variable PATCH",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "host-var-patch-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "host-var-patch-spec",
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
            "name": "host-var-patch-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.80",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    payload = {
        "host": host["id"],
        "key": "log_level",
        "value": "info",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-host-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-host-variables/{var_id}",
        {"value": "debug"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["value"] == "debug"
    assert r.data["key"] == "log_level"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-host-variables/{var_id}")
    assert r.status_code == 200
    assert r.data["value"] == "debug"


@pytest.mark.django_db
def test_ansible_host_variable_delete(auth_client):
    """Test deleting an Ansible host variable"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "host-var-delete-inventory",
            "description": "Test inventory for host variable deletion",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "host-var-delete-group",
            "description": "Test group for host variable deletion",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "host-var-delete-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "host-var-delete-spec",
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
            "name": "host-var-delete-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.90",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    payload = {
        "host": host["id"],
        "key": "temp_var",
        "value": "temp_value",
        "value_type": "string",
    }
    create_r = auth_client.post("/api/v1/ansible-host-variables", payload, format="json")
    var_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-host-variables/{var_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-host-variables/{var_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE INVENTORY PLUGIN TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_inventory_plugin_create(auth_client):
    """Test creating an Ansible inventory plugin"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "plugin-test-inventory",
            "description": "Test inventory for plugins",
            "version": "1.0",
            "source_type": "dynamic",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "aws_ec2",
        "config": {
            "regions": ["us-west-2", "us-east-1"],
            "filters": {"tag:Environment": "production"},
        },
        "enabled": True,
        "priority": 10,
        "cache_timeout": 3600,
    }
    r = auth_client.post("/api/v1/ansible-inventory-plugins", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "aws_ec2"
    assert r.data["enabled"] is True
    assert r.data["priority"] == 10
    assert "regions" in r.data["config"]


@pytest.mark.django_db
def test_ansible_inventory_plugin_list(auth_client):
    """Test listing Ansible inventory plugins"""
    r = auth_client.get("/api/v1/ansible-inventory-plugins")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_inventory_plugin_retrieve(auth_client):
    """Test retrieving a specific Ansible inventory plugin"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "plugin-retrieve-inventory",
            "description": "Test inventory for plugin retrieval",
            "version": "1.0",
            "source_type": "dynamic",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "openstack",
        "config": {
            "clouds": ["production", "staging"],
            "regions": ["us-west-2"],
        },
        "enabled": True,
        "priority": 20,
        "cache_timeout": 1800,
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-plugins", payload, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-inventory-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["name"] == "openstack"
    assert r.data["enabled"] is True
    assert "clouds" in r.data["config"]


@pytest.mark.django_db
def test_ansible_inventory_plugin_update_put(auth_client):
    """Test updating an Ansible inventory plugin with PUT"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "plugin-put-inventory",
            "description": "Test inventory for plugin PUT",
            "version": "1.0",
            "source_type": "dynamic",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "vmware",
        "config": {
            "hostname": "vcenter.example.com",
            "username": "admin",
        },
        "enabled": True,
        "priority": 30,
        "cache_timeout": 7200,
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-plugins", payload, format="json")
    plugin_id = create_r.data["id"]

    put_payload = {
        "inventory": inventory["id"],
        "name": "vmware_updated",
        "config": {
            "hostname": "vcenter-updated.example.com",
            "username": "admin",
            "port": 443,
        },
        "enabled": False,
        "priority": 40,
        "cache_timeout": 3600,
    }
    r = auth_client.put(
        f"/api/v1/ansible-inventory-plugins/{plugin_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "vmware_updated"
    assert r.data["enabled"] is False
    assert r.data["config"]["port"] == 443

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["name"] == "vmware_updated"


@pytest.mark.django_db
def test_ansible_inventory_plugin_update_patch(auth_client):
    """Test updating an Ansible inventory plugin with PATCH"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "plugin-patch-inventory",
            "description": "Test inventory for plugin PATCH",
            "version": "1.0",
            "source_type": "dynamic",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "azure_rm",
        "config": {
            "subscription_id": "12345",
            "client_id": "67890",
        },
        "enabled": True,
        "priority": 50,
        "cache_timeout": 1800,
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-plugins", payload, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-inventory-plugins/{plugin_id}",
        {"enabled": False, "config": {"subscription_id": "54321"}},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["enabled"] is False
    assert r.data["config"]["subscription_id"] == "54321"
    assert r.data["name"] == "azure_rm"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-plugins/{plugin_id}")
    assert r.status_code == 200
    assert r.data["enabled"] is False


@pytest.mark.django_db
def test_ansible_inventory_plugin_delete(auth_client):
    """Test deleting an Ansible inventory plugin"""
    # Create inventory first
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "plugin-delete-inventory",
            "description": "Test inventory for plugin deletion",
            "version": "1.0",
            "source_type": "dynamic",
            "status": "active",
        },
        format="json",
    ).data

    payload = {
        "inventory": inventory["id"],
        "name": "temp",
        "config": {"temp": "value"},
        "enabled": True,
        "priority": 100,
        "cache_timeout": 3600,
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-plugins", payload, format="json")
    plugin_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-inventory-plugins/{plugin_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-inventory-plugins/{plugin_id}")
    assert r.status_code == 404


# ============================================================================
# ANSIBLE INVENTORY TEMPLATE TESTS
# ============================================================================


@pytest.mark.django_db
def test_ansible_inventory_template_create(auth_client):
    """Test creating an Ansible inventory template"""
    payload = {
        "name": "web_servers_template",
        "description": "Template for web server inventory",
        "template_type": "jinja2",
        "template_content": """
[webservers]
{% for host in hosts %}
{{ host.name }} ansible_host={{ host.ip }} ansible_user={{ host.user }}
{% endfor %}

[webservers:vars]
http_port=80
max_connections=100
""",
        "variables": {
            "hosts": "list",
            "ip": "string",
            "user": "string",
        },
        "status": "active",
    }
    r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    assert r.status_code == 201
    assert r.data["name"] == "web_servers_template"
    assert r.data["template_type"] == "jinja2"
    assert "webservers" in r.data["template_content"]
    assert "hosts" in r.data["variables"]


@pytest.mark.django_db
def test_ansible_inventory_template_list(auth_client):
    """Test listing Ansible inventory templates"""
    r = auth_client.get("/api/v1/ansible-inventory-templates")
    assert r.status_code == 200
    assert "results" in r.data


@pytest.mark.django_db
def test_ansible_inventory_template_retrieve(auth_client):
    """Test retrieving a specific Ansible inventory template"""
    payload = {
        "name": "database_template",
        "description": "Template for database server inventory",
        "template_type": "jinja2",
        "template_content": """
[dbservers]
{% for db in databases %}
{{ db.name }} ansible_host={{ db.ip }} ansible_user={{ db.user }}
{% endfor %}

[dbservers:vars]
db_port=5432
max_connections=200
""",
        "variables": {
            "databases": "list",
            "ip": "string",
            "user": "string",
        },
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    template_id = create_r.data["id"]

    r = auth_client.get(f"/api/v1/ansible-inventory-templates/{template_id}")
    assert r.status_code == 200
    assert r.data["name"] == "database_template"
    assert "dbservers" in r.data["template_content"]
    assert "databases" in r.data["variables"]


@pytest.mark.django_db
def test_ansible_inventory_template_update_put(auth_client):
    """Test updating an Ansible inventory template with PUT"""
    payload = {
        "name": "app_template",
        "description": "Template for application server inventory",
        "template_type": "jinja2",
        "template_content": """
[appservers]
{% for app in apps %}
{{ app.name }} ansible_host={{ app.ip }}
{% endfor %}
""",
        "variables": {
            "apps": "list",
            "ip": "string",
        },
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    template_id = create_r.data["id"]

    put_payload = {
        "name": "app_template_updated",
        "description": "Updated template for application server inventory",
        "template_type": "jinja2",
        "template_content": """
[appservers]
{% for app in apps %}
{{ app.name }} ansible_host={{ app.ip }} ansible_user={{ app.user }}
{% endfor %}

[appservers:vars]
app_port=8080
""",
        "variables": {
            "apps": "list",
            "ip": "string",
            "user": "string",
        },
    }
    r = auth_client.put(
        f"/api/v1/ansible-inventory-templates/{template_id}", put_payload, format="json"
    )
    assert r.status_code == 200
    assert r.data["name"] == "app_template_updated"
    assert r.data["description"] == "Updated template for application server inventory"
    assert "app_port" in r.data["template_content"]

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-templates/{template_id}")
    assert r.status_code == 200
    assert r.data["name"] == "app_template_updated"


@pytest.mark.django_db
def test_ansible_inventory_template_update_patch(auth_client):
    """Test updating an Ansible inventory template with PATCH"""
    payload = {
        "name": "monitoring_template",
        "description": "Template for monitoring server inventory",
        "template_type": "jinja2",
        "template_content": """
[monitoring]
{% for monitor in monitors %}
{{ monitor.name }} ansible_host={{ monitor.ip }}
{% endfor %}
""",
        "variables": {
            "monitors": "list",
            "ip": "string",
        },
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    template_id = create_r.data["id"]

    r = auth_client.patch(
        f"/api/v1/ansible-inventory-templates/{template_id}",
        {"description": "Updated monitoring template", "template_type": "yaml"},
        format="json",
    )
    assert r.status_code == 200
    assert r.data["template_type"] == "yaml"
    assert r.data["description"] == "Updated monitoring template"
    assert r.data["name"] == "monitoring_template"  # Should remain unchanged

    # Verify in database
    r = auth_client.get(f"/api/v1/ansible-inventory-templates/{template_id}")
    assert r.status_code == 200
    assert r.data["template_type"] == "yaml"


@pytest.mark.django_db
def test_ansible_inventory_template_delete(auth_client):
    """Test deleting an Ansible inventory template"""
    payload = {
        "name": "temp_template",
        "description": "Temporary template",
        "template_type": "jinja2",
        "template_content": "temp: {{ temp }}",
        "variables": {"temp": "string"},
        "status": "active",
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    template_id = create_r.data["id"]

    r = auth_client.delete(f"/api/v1/ansible-inventory-templates/{template_id}")
    assert r.status_code in (204, 200)

    # Verify deletion
    r = auth_client.get(f"/api/v1/ansible-inventory-templates/{template_id}")
    assert r.status_code == 404


@pytest.mark.django_db
def test_ansible_inventory_template_render(auth_client):
    """Test rendering an Ansible inventory template"""
    payload = {
        "name": "render_test_template",
        "description": "Template for testing rendering",
        "template_type": "jinja2",
        "template_content": """
[webservers]
{% for host in hosts %}
{{ host.name }} ansible_host={{ host.ip }} ansible_user={{ host.user }}
{% endfor %}

[webservers:vars]
http_port={{ http_port }}
max_connections={{ max_connections }}
""",
        "variables": {
            "hosts": "list",
            "ip": "string",
            "user": "string",
            "http_port": "integer",
            "max_connections": "integer",
        },
    }
    create_r = auth_client.post("/api/v1/ansible-inventory-templates", payload, format="json")
    template_id = create_r.data["id"]

    render_data = {
        "context": {
            "hosts": [
                {"name": "web1", "ip": "192.168.1.10", "user": "ubuntu"},
                {"name": "web2", "ip": "192.168.1.11", "user": "ubuntu"},
            ],
            "http_port": 80,
            "max_connections": 100,
        }
    }

    r = auth_client.post(
        f"/api/v1/ansible-inventory-templates/{template_id}/render_template",
        render_data,
        format="json",
    )
    assert r.status_code == 200
    assert "rendered_content" in r.data
    rendered = r.data["rendered_content"]
    assert "web1" in rendered
    assert "web2" in rendered
    assert "192.168.1.10" in rendered
    assert "192.168.1.11" in rendered
    assert "http_port=80" in rendered
    assert "max_connections=100" in rendered
