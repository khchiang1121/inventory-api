#!/usr/bin/env python3
"""
Utility functions for working with Ansible inventory models.
This script demonstrates how to use the Ansible models to generate
Ansible inventory files and manage groups.
"""

import json
import os
from typing import Any, Dict, List

from django.contrib.contenttypes.models import ContentType

from inventory_api.api.models import (
    AnsibleGroup,
    AnsibleGroupRelationship,
    AnsibleGroupVariable,
    AnsibleHost,
    Baremetal,
    VirtualMachine,
)


class AnsibleInventoryGenerator:
    """Generate Ansible inventory from database models"""

    def __init__(self):
        self.inventory = {"all": {"children": {}, "vars": {}}}

    def generate_inventory(self) -> Dict[str, Any]:
        """Generate complete Ansible inventory"""
        # Get all groups
        groups = AnsibleGroup.objects.filter(status="active")

        for group in groups:
            if group.is_special and group.name == "all":
                # Handle 'all' group specially
                self.inventory["all"]["vars"] = group.all_variables
                continue

            # Add group to inventory
            self._add_group_to_inventory(group)

        return self.inventory

    def _add_group_to_inventory(self, group: AnsibleGroup):
        """Add a group and its hosts to the inventory"""
        group_data = {"hosts": {}, "vars": group.all_variables}

        # Add child groups
        if group.child_groups:
            group_data["children"] = {}
            for child in group.child_groups:
                group_data["children"][child.name] = {}

        # Add hosts to this group
        for host in group.hosts.all():
            host_data = self._get_host_data(host)
            group_data["hosts"][host.host_name] = host_data

        # Add to inventory
        if group.name not in self.inventory["all"]["children"]:
            self.inventory["all"]["children"][group.name] = group_data

    def _get_host_data(self, host: AnsibleHost) -> Dict[str, Any]:
        """Get host data for inventory"""
        host_data = {
            "ansible_host": host.ansible_host,
            "ansible_port": host.ansible_port,
            "ansible_user": host.ansible_user,
        }

        # Add SSH key if specified
        if host.ansible_ssh_private_key_file:
            host_data["ansible_ssh_private_key_file"] = (
                host.ansible_ssh_private_key_file
            )

        # Add host variables
        if host.host_vars:
            host_data.update(host.host_vars)

        # Add host type information
        host_data["host_type"] = host.host_type

        return host_data

    def save_inventory(self, filepath: str):
        """Save inventory to file"""
        inventory = self.generate_inventory()

        with open(filepath, "w") as f:
            json.dump(inventory, f, indent=2)

        print(f"Inventory saved to {filepath}")


class AnsibleGroupManager:
    """Manage Ansible groups and relationships"""

    @staticmethod
    def create_group(
        name: str, description: str = "", is_special: bool = False
    ) -> AnsibleGroup:
        """Create a new Ansible group"""
        group, created = AnsibleGroup.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "is_special": is_special,
                "status": "active",
            },
        )

        if created:
            print(f"Created group: {name}")
        else:
            print(f"Group already exists: {name}")

        return group

    @staticmethod
    def add_group_variable(
        group: AnsibleGroup, key: str, value, value_type: str = "string"
    ):
        """Add a variable to a group"""
        var = group.set_variable(key, value, value_type)
        print(f"Added variable {key}={value} to group {group.name}")
        return var

    @staticmethod
    def create_parent_child_relationship(parent: AnsibleGroup, child: AnsibleGroup):
        """Create a parent-child relationship between groups"""
        rel, created = AnsibleGroupRelationship.objects.get_or_create(
            parent_group=parent, child_group=child
        )

        if created:
            print(f"Created relationship: {parent.name} -> {child.name}")
        else:
            print(f"Relationship already exists: {parent.name} -> {child.name}")

        return rel

    @staticmethod
    def assign_host_to_group(host_obj, group: AnsibleGroup, **kwargs):
        """Assign a host (VM or Baremetal) to an Ansible group"""
        content_type = ContentType.objects.get_for_model(host_obj)

        host, created = AnsibleHost.objects.get_or_create(
            group=group,
            content_type=content_type,
            object_id=host_obj.id,
            defaults=kwargs,
        )

        if created:
            print(f"Assigned {host_obj.name} to group {group.name}")
        else:
            print(f"Host {host_obj.name} already in group {group.name}")

        return host


def example_usage():
    """Example of how to use the Ansible models"""

    # Create groups
    manager = AnsibleGroupManager()

    # Create environment groups
    production = manager.create_group("production", "Production environment")
    staging = manager.create_group("staging", "Staging environment")

    # Create role groups
    webservers = manager.create_group("webservers", "Web servers")
    dbservers = manager.create_group("dbservers", "Database servers")
    monitoring = manager.create_group("monitoring", "Monitoring servers")

    # Create relationships
    manager.create_parent_child_relationship(production, webservers)
    manager.create_parent_child_relationship(production, dbservers)
    manager.create_parent_child_relationship(production, monitoring)
    manager.create_parent_child_relationship(staging, webservers)
    manager.create_parent_child_relationship(staging, dbservers)

    # Add variables to groups
    manager.add_group_variable(production, "environment", "production")
    manager.add_group_variable(production, "backup_enabled", True, "boolean")
    manager.add_group_variable(production, "monitoring_level", "high")

    manager.add_group_variable(staging, "environment", "staging")
    manager.add_group_variable(staging, "backup_enabled", False, "boolean")
    manager.add_group_variable(staging, "monitoring_level", "medium")

    manager.add_group_variable(webservers, "http_port", 80, "integer")
    manager.add_group_variable(webservers, "max_clients", 200, "integer")

    manager.add_group_variable(dbservers, "db_port", 5432, "integer")
    manager.add_group_variable(dbservers, "max_connections", 100, "integer")

    # Assign hosts to groups (example with existing hosts)
    baremetals = Baremetal.objects.all()[:5]
    vms = VirtualMachine.objects.all()[:5]

    for i, baremetal in enumerate(baremetals):
        if i < 2:
            group = webservers
        else:
            group = dbservers
        manager.assign_host_to_group(baremetal, group)

    for i, vm in enumerate(vms):
        if i < 2:
            group = webservers
        else:
            group = monitoring
        manager.assign_host_to_group(vm, group)

    # Generate inventory
    generator = AnsibleInventoryGenerator()
    inventory = generator.generate_inventory()

    # Save to file
    generator.save_inventory("ansible_inventory.json")

    print("\nGenerated inventory structure:")
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    # This would need to be run in a Django environment
    # python manage.py shell < ansible_utils.py
    print("This script should be run in a Django shell environment")
    print("Use: python manage.py shell")
    print(
        "Then import and run: from ansible_utils import example_usage; example_usage()"
    )
