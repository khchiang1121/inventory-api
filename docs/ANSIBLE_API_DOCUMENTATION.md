# Ansible Inventory API Documentation

This document describes the complete API endpoints for the enhanced Ansible inventory system.

## 📋 Table of Contents

- [Inventory Management](#inventory-management)
- [Variable Sets](#variable-sets)
- [Variable Set Associations](#variable-set-associations)
- [Host Variables](#host-variables)
- [Inventory Plugins](#inventory-plugins)
- [Inventory Templates](#inventory-templates)
- [Existing Ansible Endpoints](#existing-ansible-endpoints)

## 🏗️ Inventory Management

### AnsibleInventory

**Base URL:** `/api/v1/ansible-inventories/`

#### List Inventories
```http
GET /api/v1/ansible-inventories/
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "production",
      "description": "Production environment inventory",
      "version": "1.0",
      "source_type": "static",
      "source_plugin": null,
      "source_config": {},
      "status": "active",
      "created_by": {
        "id": 1,
        "username": "admin"
      },
      "groups_count": 3,
      "hosts_count": 10,
      "associated_variable_sets_count": 2,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Inventory
```http
POST /api/v1/ansible-inventories/
Content-Type: application/json

{
  "name": "staging",
  "description": "Staging environment inventory",
  "version": "1.0",
  "source_type": "hybrid",
  "source_plugin": "aws_ec2",
  "source_config": {
    "regions": ["us-west-2"],
    "filters": {"tag:Environment": "staging"}
  },
  "status": "active"
}
```

#### Get Merged Variables
```http
GET /api/v1/ansible-inventories/{id}/merged_variables/
GET /api/v1/ansible-inventories/{id}/merged_variables/?group_id=1&host_id=2
```

**Response:**
```json
{
  "ansible_user": "ubuntu",
  "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
  "database_host": "db.example.com",
  "app_version": "2.1.0"
}
```

### AnsibleInventoryVariable

**Base URL:** `/api/v1/ansible-inventory-variables/`

#### List Inventory Variables
```http
GET /api/v1/ansible-inventory-variables/
```

#### Create Inventory Variable
```http
POST /api/v1/ansible-inventory-variables/
Content-Type: application/json

{
  "inventory": 1,
  "key": "ansible_user",
  "value": "ubuntu",
  "value_type": "string"
}
```

## 📦 Variable Sets

### AnsibleVariableSet

**Base URL:** `/api/v1/ansible-variable-sets/`

#### List Variable Sets
```http
GET /api/v1/ansible-variable-sets/
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "common_variables",
      "description": "Common variables for all environments",
      "content": "ansible_user: ubuntu\nansible_ssh_private_key_file: ~/.ssh/id_rsa",
      "content_type": "yaml",
      "tags": ["common", "system"],
      "priority": 10,
      "status": "active",
      "created_by": {
        "id": 1,
        "username": "admin"
      },
      "associated_inventories_count": 2,
      "parsed_content": {
        "ansible_user": "ubuntu",
        "ansible_ssh_private_key_file": "~/.ssh/id_rsa"
      },
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Variable Set
```http
POST /api/v1/ansible-variable-sets/
Content-Type: application/json

{
  "name": "database_variables",
  "description": "Database connection variables",
  "content": "{\n  \"database_host\": \"db.example.com\",\n  \"database_port\": 5432,\n  \"database_name\": \"myapp\"\n}",
  "content_type": "json",
  "tags": ["database", "production"],
  "priority": 20,
  "status": "active"
}
```

#### Filter by Tags
```http
GET /api/v1/ansible-variable-sets/by_tags/?tags=common&tags=system
```

#### Validate Content
```http
POST /api/v1/ansible-variable-sets/{id}/validate_content/
```

**Response:**
```json
{
  "valid": true
}
```

## 🔗 Variable Set Associations

### AnsibleInventoryVariableSetAssociation

**Base URL:** `/api/v1/ansible-inventory-variable-set-associations/`

#### List Associations
```http
GET /api/v1/ansible-inventory-variable-set-associations/
```

#### Create Association
```http
POST /api/v1/ansible-inventory-variable-set-associations/
Content-Type: application/json

{
  "inventory": 1,
  "variable_set": 1,
  "load_priority": 10,
  "enabled": true,
  "load_tags": ["production"],
  "load_config": {
    "merge_strategy": "override"
  }
}
```

## 🖥️ Host Variables

### AnsibleHostVariable

**Base URL:** `/api/v1/ansible-host-variables/`

#### List Host Variables
```http
GET /api/v1/ansible-host-variables/
```

#### Create Host Variable
```http
POST /api/v1/ansible-host-variables/
Content-Type: application/json

{
  "host": 1,
  "key": "app_version",
  "value": "2.1.0",
  "value_type": "string"
}
```

## 🔌 Inventory Plugins

### AnsibleInventoryPlugin

**Base URL:** `/api/v1/ansible-inventory-plugins/`

#### List Plugins
```http
GET /api/v1/ansible-inventory-plugins/
```

#### Create Plugin
```http
POST /api/v1/ansible-inventory-plugins/
Content-Type: application/json

{
  "inventory": 1,
  "name": "aws_ec2",
  "config": {
    "regions": ["us-west-2", "us-east-1"],
    "filters": {
      "tag:Environment": "production"
    },
    "keyed_groups": [
      {
        "key": "tags.Environment",
        "prefix": "env"
      }
    ]
  },
  "enabled": true,
  "priority": 1,
  "cache_timeout": 300
}
```

## 📄 Inventory Templates

### AnsibleInventoryTemplate

**Base URL:** `/api/v1/ansible-inventory-templates/`

#### List Templates
```http
GET /api/v1/ansible-inventory-templates/
```

#### Create Template
```http
POST /api/v1/ansible-inventory-templates/
Content-Type: application/json

{
  "name": "yaml_template",
  "description": "YAML format inventory template",
  "template_type": "yaml",
  "template_content": "all:\n  children:\n    {% for group in groups %}\n    {{ group.name }}:\n      hosts:\n        {% for host in group.hosts %}\n        {{ host.name }}:\n          ansible_host: {{ host.ip_address }}\n        {% endfor %}\n    {% endfor %}",
  "variables": {
    "groups": [],
    "hosts": []
  }
}
```

#### Render Template
```http
POST /api/v1/ansible-inventory-templates/{id}/render_template/
Content-Type: application/json

{
  "context": {
    "groups": [
      {
        "name": "webservers",
        "hosts": [
          {"name": "web1", "ip_address": "192.168.1.10"},
          {"name": "web2", "ip_address": "192.168.1.11"}
        ]
      }
    ]
  }
}
```

**Response:**
```json
{
  "rendered_content": "all:\n  children:\n    webservers:\n      hosts:\n        web1:\n          ansible_host: 192.168.1.10\n        web2:\n          ansible_host: 192.168.1.11"
}
```

## 🔄 Existing Ansible Endpoints

The following existing endpoints remain unchanged:

### AnsibleGroup
- **Base URL:** `/api/v1/ansible-groups/`
- **Methods:** GET, POST, PUT, PATCH, DELETE
- **Features:** Group management, variable inheritance, parent-child relationships

### AnsibleGroupVariable
- **Base URL:** `/api/v1/ansible-group-variables/`
- **Methods:** GET, POST, PUT, PATCH, DELETE
- **Features:** Group-level variable management

### AnsibleGroupRelationship
- **Base URL:** `/api/v1/ansible-group-relationships/`
- **Methods:** GET, POST, PUT, PATCH, DELETE
- **Features:** Parent-child group relationships

### AnsibleHost
- **Base URL:** `/api/v1/ansible-hosts/`
- **Methods:** GET, POST, PUT, PATCH, DELETE
- **Features:** Host management, VM/Baremetal integration

## 🚀 Usage Examples

### Complete Workflow Example

1. **Create an inventory:**
```bash
curl -X POST /api/v1/ansible-inventories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "production", "description": "Production inventory"}'
```

2. **Create variable sets:**
```bash
curl -X POST /api/v1/ansible-variable-sets/ \
  -H "Content-Type: application/json" \
  -d '{"name": "common", "content": "ansible_user: ubuntu", "content_type": "yaml"}'
```

3. **Associate variable set with inventory:**
```bash
curl -X POST /api/v1/ansible-inventory-variable-set-associations/ \
  -H "Content-Type: application/json" \
  -d '{"inventory": 1, "variable_set": 1, "load_priority": 10}'
```

4. **Create groups:**
```bash
curl -X POST /api/v1/ansible-groups/ \
  -H "Content-Type: application/json" \
  -d '{"inventory": 1, "name": "webservers", "description": "Web server group"}'
```

5. **Create hosts:**
```bash
curl -X POST /api/v1/ansible-hosts/ \
  -H "Content-Type: application/json" \
  -d '{"inventory": 1, "group": 1, "name": "web1", "ansible_host": "192.168.1.10"}'
```

6. **Get merged variables:**
```bash
curl /api/v1/ansible-inventories/1/merged_variables/
```

### Variable Priority Order

Variables are merged in the following priority order (highest to lowest):

1. **Host Variables** (`AnsibleHostVariable`)
2. **Group Variables** (`AnsibleGroupVariable`)
3. **Associated Variable Sets** (`AnsibleVariableSet` via `AnsibleInventoryVariableSetAssociation`)
4. **Inventory Variables** (`AnsibleInventoryVariable`)

Lower priority variables are overridden by higher priority ones.

## 🔧 Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include detailed error messages:

```json
{
  "error": "Validation failed",
  "details": {
    "name": ["This field is required."],
    "content": ["Invalid YAML format."]
  }
}
```

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- Variable content validation is performed automatically
- Template rendering requires Jinja2 to be installed
- Variable sets support multiple content formats (YAML, JSON, INI, ENV)
- Associations support conditional loading based on tags
- All endpoints support filtering, ordering, and pagination
