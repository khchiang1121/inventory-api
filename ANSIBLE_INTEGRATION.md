# Ansible Integration with VirtFlow

This document describes the Ansible inventory integration with the VirtFlow database models.

## Overview

The Ansible integration allows you to:

- Store Ansible groups, variables, and relationships in the database
- Link VMs and Baremetal servers to Ansible groups
- Generate Ansible inventory files from the database
- Manage group hierarchies and variable inheritance

## Database Models

### AnsibleGroup

Represents an Ansible group with the following fields:

- `name`: Unique group name
- `description`: Group description
- `is_special`: Whether this is a special group (all, ungrouped)
- `status`: Active or inactive

### AnsibleGroupVariable

Stores variables for groups:

- `group`: Foreign key to AnsibleGroup
- `key`: Variable name
- `value`: Variable value (stored as text)
- `value_type`: Type of the variable (string, integer, float, boolean, json, list, dict)

### AnsibleGroupRelationship

Manages parent-child relationships between groups:

- `parent_group`: Parent group
- `child_group`: Child group

### AnsibleHost

Links VMs and Baremetal servers to Ansible groups:

- `group`: The Ansible group this host belongs to
- `host`: Generic foreign key to either VM or Baremetal
- `ansible_host`: IP address for Ansible connection
- `ansible_port`: SSH port (default: 22)
- `ansible_user`: SSH username (default: root)
- `ansible_ssh_private_key_file`: Path to SSH private key
- `host_vars`: JSON field for host-specific variables

## Usage Examples

### Creating Groups and Variables

```python
from virtflow.api.models import AnsibleGroup, AnsibleGroupVariable

# Create a group
webservers = AnsibleGroup.objects.create(
    name="webservers",
    description="Web servers",
    status="active"
)

# Add variables to the group
webservers.set_variable("http_port", 80, "integer")
webservers.set_variable("max_clients", 200, "integer")
webservers.set_variable("nginx_version", "1.18.0", "string")
```

### Creating Group Relationships

```python
from virtflow.api.models import AnsibleGroup, AnsibleGroupRelationship

# Create parent and child groups
production = AnsibleGroup.objects.create(name="production")
webservers = AnsibleGroup.objects.create(name="webservers")

# Create relationship
AnsibleGroupRelationship.objects.create(
    parent_group=production,
    child_group=webservers
)
```

### Assigning Hosts to Groups

```python
from virtflow.api.models import AnsibleHost
from django.contrib.contenttypes.models import ContentType

# Get a VM or Baremetal server
vm = VirtualMachine.objects.get(name="web-server-01")

# Assign to group
content_type = ContentType.objects.get_for_model(vm)
AnsibleHost.objects.create(
    group=webservers,
    content_type=content_type,
    object_id=vm.id,
    ansible_host="192.168.1.100",
    ansible_user="ubuntu",
    host_vars={"environment": "production"}
)
```

### Generating Ansible Inventory

```python
from ansible_utils import AnsibleInventoryGenerator

# Generate inventory
generator = AnsibleInventoryGenerator()
inventory = generator.generate_inventory()

# Save to file
generator.save_inventory("inventory.json")
```

## Generated Inventory Structure

The generated inventory follows the Ansible JSON inventory format:

```json
{
  "all": {
    "children": {
      "production": {
        "children": {
          "webservers": {
            "hosts": {
              "web-server-01": {
                "ansible_host": "192.168.1.100",
                "ansible_port": 22,
                "ansible_user": "ubuntu",
                "http_port": 80,
                "max_clients": 200,
                "host_type": "virtualmachine"
              }
            },
            "vars": {
              "http_port": 80,
              "max_clients": 200,
              "nginx_version": "1.18.0"
            }
          }
        },
        "vars": {
          "environment": "production",
          "backup_enabled": true
        }
      }
    },
    "vars": {
      "global_setting": "value"
    }
  }
}
```

## Variable Inheritance

Variables are inherited from parent groups, with child group variables taking precedence:

1. Variables from parent groups are inherited
2. Child group variables override parent variables
3. Host variables override group variables

## Utility Classes

### AnsibleGroupManager

Provides convenient methods for managing groups:

```python
from ansible_utils import AnsibleGroupManager

manager = AnsibleGroupManager()

# Create groups
production = manager.create_group("production", "Production environment")
webservers = manager.create_group("webservers", "Web servers")

# Add variables
manager.add_group_variable(production, "environment", "production")
manager.add_group_variable(webservers, "http_port", 80, "integer")

# Create relationships
manager.create_parent_child_relationship(production, webservers)

# Assign hosts
manager.assign_host_to_group(vm, webservers, ansible_host="192.168.1.100")
```

### AnsibleInventoryGenerator

Generates Ansible inventory from the database:

```python
from ansible_utils import AnsibleInventoryGenerator

generator = AnsibleInventoryGenerator()
inventory = generator.generate_inventory()
generator.save_inventory("ansible_inventory.json")
```

## Integration with Existing Models

The Ansible integration works seamlessly with existing VirtFlow models:

- **Baremetal servers** can be assigned to Ansible groups
- **Virtual machines** can be assigned to Ansible groups
- **Network interfaces** provide IP addresses for Ansible connections
- **Tenants** can be used for group organization

## Migration

To apply the database changes:

```bash
python manage.py migrate
```

To generate fake data including Ansible groups:

```bash
python manage.py generate_fake_data
```

## Best Practices

1. **Group Naming**: Use descriptive names like `production-webservers`, `staging-dbservers`
2. **Variable Organization**: Use hierarchical groups to organize variables
3. **Host Assignment**: Assign hosts based on their role and environment
4. **Security**: Store sensitive information like SSH keys securely
5. **Documentation**: Keep group descriptions up to date

## API Endpoints

The models can be exposed through Django REST Framework API endpoints for:

- CRUD operations on groups
- Managing group variables
- Assigning hosts to groups
- Generating inventory files

## Example Workflow

1. Create environment groups (production, staging, development)
2. Create role groups (webservers, dbservers, monitoring)
3. Set up parent-child relationships
4. Add variables to groups
5. Assign VMs and Baremetal servers to appropriate groups
6. Generate Ansible inventory
7. Use the inventory with Ansible playbooks

This integration provides a powerful way to manage Ansible inventory as code, with full database persistence and integration with your existing infrastructure management system.
