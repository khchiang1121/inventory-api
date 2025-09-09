import pytest
from django.contrib.contenttypes.models import ContentType

# ============================================================================
# COMPREHENSIVE ANSIBLE INVENTORY WORKFLOW TESTS
# ============================================================================


@pytest.mark.django_db
def test_complete_ansible_inventory_workflow(auth_client):
    """Test complete workflow: inventory -> variable sets -> groups -> hosts -> variables"""
    # 1. Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "workflow-test-inventory",
            "description": "Complete workflow test inventory",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # 2. Create variable sets
    common_vars = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "workflow-common-vars",
            "description": "Common variables for workflow test",
            "content": "ansible_user: ubuntu\nansible_port: 22\ntimezone: UTC",
            "content_type": "yaml",
            "tags": ["common", "system"],
            "priority": 10,
            "status": "active",
        },
        format="json",
    ).data

    app_vars = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "workflow-app-vars",
            "description": "Application variables for workflow test",
            "content": '{"app_name": "myapp", "app_version": "1.0.0", "debug": false}',
            "content_type": "json",
            "tags": ["app", "production"],
            "priority": 20,
            "status": "active",
        },
        format="json",
    ).data

    # 3. Associate variable sets with inventory
    auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations",
        {
            "inventory": inventory["id"],
            "variable_set": common_vars["id"],
            "load_priority": 10,
            "enabled": True,
            "load_tags": [],
            "load_config": {},
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations",
        {
            "inventory": inventory["id"],
            "variable_set": app_vars["id"],
            "load_priority": 20,
            "enabled": True,
            "load_tags": ["production"],
            "load_config": {"merge_strategy": "override"},
        },
        format="json",
    )

    # 4. Create inventory variables
    auth_client.post(
        "/api/v1/ansible-inventory-variables",
        {
            "inventory": inventory["id"],
            "key": "environment",
            "value": "production",
            "value_type": "string",
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-inventory-variables",
        {
            "inventory": inventory["id"],
            "key": "backup_enabled",
            "value": "true",
            "value_type": "boolean",
        },
        format="json",
    )

    # 5. Create groups
    webservers_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "webservers",
            "description": "Web server group",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    dbservers_group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "dbservers",
            "description": "Database server group",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # 6. Create group variables
    auth_client.post(
        "/api/v1/ansible-group-variables",
        {
            "group": webservers_group["id"],
            "key": "http_port",
            "value": "80",
            "value_type": "integer",
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-group-variables",
        {
            "group": dbservers_group["id"],
            "key": "db_port",
            "value": "5432",
            "value_type": "integer",
        },
        format="json",
    )

    # 7. Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "workflow-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "workflow-spec",
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
            "name": "workflow-vm",
            "type": "worker",
            "status": "running",
            "tenant": tenant["id"],
            "specification": spec["id"],
        },
        format="json",
    ).data

    # 8. Create host
    ct = ContentType.objects.get(app_label="api", model="virtualmachine")
    host = auth_client.post(
        "/api/v1/ansible-hosts",
        {
            "inventory": inventory["id"],
            "group": webservers_group["id"],
            "content_type": ct.id,
            "object_id": vm["id"],
            "ansible_host": "192.168.1.100",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
            "aliases": ["web1", "primary-web"],
            "status": "active",
            "metadata": {"deployment_id": "deploy-123", "region": "us-west-2"},
        },
        format="json",
    ).data

    # 9. Create host variables
    auth_client.post(
        "/api/v1/ansible-host-variables",
        {
            "host": host["id"],
            "key": "app_version",
            "value": "2.1.0",
            "value_type": "string",
        },
        format="json",
    )

    auth_client.post(
        "/api/v1/ansible-host-variables",
        {
            "host": host["id"],
            "key": "max_connections",
            "value": "200",
            "value_type": "integer",
        },
        format="json",
    )

    # 10. Test merged variables endpoint
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables"
    )
    assert r.status_code == 200

    # Should include inventory variables
    assert "environment" in r.data
    assert r.data["environment"] == "production"
    assert "backup_enabled" in r.data
    assert r.data["backup_enabled"] is True

    # Should include variable set variables
    assert "ansible_user" in r.data
    assert r.data["ansible_user"] == "ubuntu"
    assert "ansible_port" in r.data
    assert r.data["ansible_port"] == 22
    assert "timezone" in r.data
    assert r.data["timezone"] == "UTC"
    assert "app_name" in r.data
    assert r.data["app_name"] == "myapp"
    assert "app_version" in r.data
    assert r.data["app_version"] == "1.0.0"

    # 11. Test merged variables with group context
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables?group_id={webservers_group['id']}"
    )
    assert r.status_code == 200

    # Should include group variables
    assert "http_port" in r.data
    assert r.data["http_port"] == 80

    # 12. Test merged variables with host context
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables?host_id={host['id']}"
    )
    assert r.status_code == 200

    # Should include host variables (highest priority)
    assert "app_version" in r.data
    assert r.data["app_version"] == "2.1.0"  # Host variable overrides variable set
    assert "max_connections" in r.data
    assert r.data["max_connections"] == 200

    # 13. Test inventory statistics
    r = auth_client.get(f"/api/v1/ansible-inventories/{inventory['id']}")
    assert r.status_code == 200
    assert r.data["groups_count"] == 2  # webservers, dbservers
    assert r.data["hosts_count"] == 1
    assert r.data["associated_variable_sets_count"] == 2

    # 14. Test variable set statistics
    r = auth_client.get(f"/api/v1/ansible-variable-sets/{common_vars['id']}")
    assert r.status_code == 200
    assert r.data["associated_inventories_count"] == 1
    assert "parsed_content" in r.data
    assert r.data["parsed_content"]["ansible_user"] == "ubuntu"


@pytest.mark.django_db
def test_variable_priority_override(auth_client):
    """Test that variables are overridden in correct priority order"""
    # Create inventory
    inventory = auth_client.post(
        "/api/v1/ansible-inventories",
        {
            "name": "priority-test-inventory",
            "description": "Test inventory for variable priority",
            "version": "1.0",
            "source_type": "static",
            "status": "active",
        },
        format="json",
    ).data

    # Create variable set with app_version
    var_set = auth_client.post(
        "/api/v1/ansible-variable-sets",
        {
            "name": "priority-test-vars",
            "description": "Variables for priority test",
            "content": '{"app_version": "1.0.0", "debug": true}',
            "content_type": "json",
            "tags": ["test"],
            "priority": 10,
            "status": "active",
        },
        format="json",
    ).data

    # Associate variable set
    auth_client.post(
        "/api/v1/ansible-inventory-variable-set-associations",
        {
            "inventory": inventory["id"],
            "variable_set": var_set["id"],
            "load_priority": 10,
            "enabled": True,
            "load_tags": [],
            "load_config": {},
        },
        format="json",
    )

    # Create inventory variable with same key (lower priority)
    auth_client.post(
        "/api/v1/ansible-inventory-variables",
        {
            "inventory": inventory["id"],
            "key": "app_version",
            "value": "0.9.0",
            "value_type": "string",
        },
        format="json",
    )

    # Create group
    group = auth_client.post(
        "/api/v1/ansible-groups",
        {
            "inventory": inventory["id"],
            "name": "priority-test-group",
            "description": "Test group for priority",
            "is_special": False,
            "status": "active",
        },
        format="json",
    ).data

    # Create group variable with same key (higher priority)
    auth_client.post(
        "/api/v1/ansible-group-variables",
        {
            "group": group["id"],
            "key": "app_version",
            "value": "2.0.0",
            "value_type": "string",
        },
        format="json",
    )

    # Create tenant and VM
    tenant = auth_client.post(
        "/api/v1/tenants",
        {"name": "priority-tenant", "status": "active"},
        format="json",
    ).data

    spec = auth_client.post(
        "/api/v1/vm-specifications",
        {
            "name": "priority-spec",
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
            "name": "priority-vm",
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
            "ansible_host": "192.168.1.200",
            "ansible_port": 22,
            "ansible_user": "ubuntu",
        },
        format="json",
    ).data

    # Create host variable with same key (highest priority)
    auth_client.post(
        "/api/v1/ansible-host-variables",
        {
            "host": host["id"],
            "key": "app_version",
            "value": "3.0.0",
            "value_type": "string",
        },
        format="json",
    )

    # Test merged variables - should show host variable (highest priority)
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables?host_id={host['id']}"
    )
    assert r.status_code == 200
    assert r.data["app_version"] == "3.0.0"  # Host variable wins
    assert r.data["debug"] is True  # From variable set

    # Test merged variables with group context - should show group variable
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables?group_id={group['id']}"
    )
    assert r.status_code == 200
    assert (
        r.data["app_version"] == "2.0.0"
    )  # Group variable wins over inventory and variable set

    # Test merged variables without host/group context - should show variable set variable
    r = auth_client.get(
        f"/api/v1/ansible-inventories/{inventory['id']}/merged_variables"
    )
    assert r.status_code == 200
    assert r.data["app_version"] == "1.0.0"  # Variable set wins over inventory variable

