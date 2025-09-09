import os
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from faker import Faker

from inventory_api.api import models  # Replace with your actual app path


class Command(BaseCommand):
    help = "Generate fake data for the Django Ninja project"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force recreation of data even if it already exists",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip creation if data already exists (default behavior)",
        )
        parser.add_argument(
            "--clear-first",
            action="store_true",
            help="Clear all existing data before creating new data",
        )

    def handle(self, *args: tuple, **options: dict) -> None:
        fake = Faker()
        User = get_user_model()

        # Determine behavior based on options
        force = options.get("force", False)
        skip_existing = options.get("skip_existing", False)
        clear_first = options.get("clear_first", False)

        # Default behavior: skip existing data
        if not force and not clear_first:
            skip_existing = True

        if clear_first:
            self.stdout.write("🗑️ Clearing existing data...")
            self._clear_all_data()
            self.stdout.write("✔️ Existing data cleared")

        # Create Groups
        group_names = ["admin", "maintainer", "viewer", "operator"]
        django_groups = []
        for name in group_names:
            django_group, created = Group.objects.get_or_create(name=name)
            django_groups.append(django_group)
            if created:
                self.stdout.write(f"✔️ Created group: {name}")
            elif not skip_existing:
                self.stdout.write(f"⚠️ Group already exists: {name}")
        self.stdout.write("✔️ Groups ready")

        # Create Users
        users = []
        for _ in range(5):
            username = fake.user_name()
            if User.objects.filter(username=username).exists() and skip_existing:
                user = User.objects.get(username=username)
                self.stdout.write(f"⚠️ User already exists: {username}")
            else:
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    # Update existing user
                    user.email = fake.email()
                    user.account = fake.user_name()
                    user.status = random.choice(["active", "inactive"])
                    user.save()
                    self.stdout.write(f"🔄 Updated user: {username}")
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=fake.email(),
                        password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123"),
                        account=fake.user_name(),
                        status=random.choice(["active", "inactive"]),
                    )
                    self.stdout.write(f"✔️ Created user: {username}")

                user.groups.clear()
                user.groups.add(random.choice(django_groups))
            users.append(user)

        # Handle default user
        default_username = "user"
        if User.objects.filter(username=default_username).exists() and skip_existing:
            default_user = User.objects.get(username=default_username)
            self.stdout.write(f"⚠️ Default user already exists: {default_username}")
        else:
            if User.objects.filter(username=default_username).exists():
                default_user = User.objects.get(username=default_username)
                default_user.email = fake.email()
                default_user.save()
                self.stdout.write(f"🔄 Updated default user: {default_username}")
            else:
                default_user = User.objects.create_user(
                    username=default_username,
                    email=fake.email(),
                    password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123"),
                    account="user",
                    status="active",
                )
                self.stdout.write(f"✔️ Created default user: {default_username}")

            default_user.groups.clear()
            default_user.groups.add(Group.objects.get(name="maintainer"))
        users.append(default_user)

        self.stdout.write("✔️ Users ready")

        # Create Fabrications, Phases, Data Centers, Rooms
        fabrications = self._create_or_get_models(
            models.Fabrication,
            lambda: {"name": f"Fab-{fake.word()}", "old_system_id": fake.uuid4()},
            3,
            skip_existing,
            "Fabrication",
        )
        phases = self._create_or_get_models(
            models.Phase,
            lambda: {"name": f"Phase-{fake.word()}", "old_system_id": fake.uuid4()},
            3,
            skip_existing,
            "Phase",
        )
        data_centers = self._create_or_get_models(
            models.DataCenter,
            lambda: {"name": f"DC-{fake.word()}", "old_system_id": fake.uuid4()},
            3,
            skip_existing,
            "DataCenter",
        )
        rooms = self._create_or_get_models(
            models.Room,
            lambda: {"name": f"Room-{fake.word()}", "old_system_id": fake.uuid4()},
            3,
            skip_existing,
            "Room",
        )

        # Create Racks
        racks = self._create_or_get_models(
            models.Rack,
            lambda: {
                "name": f"Rack-{fake.word()}",
                "bgp_number": str(fake.random_int(min=1000, max=9999)),
                "as_number": fake.random_int(min=10000, max=99999),
                "old_system_id": fake.uuid4(),
            },
            5,
            skip_existing,
            "Rack",
        )
        self.stdout.write("✔️ Racks ready")

        # Create Baremetal Groups
        host_groups = self._create_or_get_models(
            models.BaremetalGroup,
            lambda: {
                "name": fake.word().capitalize(),
                "description": fake.text(max_nb_chars=100),
                "total_cpu": 256,
                "total_memory": 131072,
                "total_storage": 50000,
                "available_cpu": 128,
                "available_memory": 65536,
                "available_storage": 25000,
                "status": random.choice(["active", "inactive"]),
            },
            3,
            skip_existing,
            "BaremetalGroup",
        )
        self.stdout.write("✔️ Baremetal groups ready")

        # Create Purchase Requisitions & Orders
        prs = self._create_or_get_models(
            models.PurchaseRequisition,
            lambda: {
                "pr_number": f"PR-{fake.unique.random_number(6)}",
                "requested_by": fake.name(),
                "department": fake.bs(),
                "reason": fake.text(),
            },
            5,
            skip_existing,
            "PurchaseRequisition",
        )

        pos = self._create_or_get_models(
            models.PurchaseOrder,
            lambda: {
                "po_number": f"PO-{fake.unique.random_number(6)}",
                "vendor_name": fake.company(),
                "payment_terms": "NET 30",
                "issued_by": fake.name(),
            },
            5,
            skip_existing,
            "PurchaseOrder",
        )

        # Create Brands and Models
        brands = self._create_or_get_models(
            models.Brand, lambda: {"name": fake.company()}, 3, skip_existing, "Brand"
        )

        baremetal_models = self._create_or_get_models(
            models.BaremetalModel,
            lambda: {
                "name": f"Model-{fake.word()}",
                "brand": random.choice(brands),
                "total_cpu": 64,
                "total_memory": 65536,
                "total_storage": 10000,
            },
            5,
            skip_existing,
            "BaremetalModel",
        )

        # Create Baremetal Servers
        baremetals = self._create_or_get_models(
            models.Baremetal,
            lambda: {
                "name": f"BM-{fake.domain_word()}",
                "serial_number": fake.uuid4(),
                "model": random.choice(baremetal_models),
                "fabrication": random.choice(fabrications),
                "phase": random.choice(phases),
                "data_center": random.choice(data_centers),
                "room": random.choice(rooms).name,
                "rack": random.choice(racks),
                "unit": f"U{random.randint(1, 48)}",
                "status": random.choice(["active", "inactive", "pending", "retired"]),
                "available_cpu": random.randint(8, 64),
                "available_memory": random.randint(8192, 65536),
                "available_storage": random.randint(500, 5000),
                "group": random.choice(host_groups),
                "pr": random.choice(prs),
                "po": random.choice(pos),
                "old_system_id": fake.uuid4(),
            },
            10,
            skip_existing,
            "Baremetal",
        )
        self.stdout.write("✔️ Baremetal servers ready")

        # Create Network Interfaces for Baremetal Servers
        baremetal_content_type = ContentType.objects.get_for_model(models.Baremetal)

        for baremetal in baremetals:
            for i in range(2):
                interface_name = f"eth{i}"
                if (
                    not models.NetworkInterface.objects.filter(
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                        name=interface_name,
                    ).exists()
                    or not skip_existing
                ):
                    if models.NetworkInterface.objects.filter(
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                        name=interface_name,
                    ).exists():
                        # Update existing interface
                        interface = models.NetworkInterface.objects.get(
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                            name=interface_name,
                        )
                        interface.mac_address = fake.mac_address()
                        interface.ipv4_address = fake.ipv4()
                        interface.gateway = fake.ipv4()
                        interface.save()
                    else:
                        # Create new interface
                        models.NetworkInterface.objects.create(
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                            name=interface_name,
                            mac_address=fake.mac_address(),
                            is_primary=(i == 0),
                            ipv4_address=fake.ipv4(),
                            ipv4_netmask="255.255.255.0",
                            gateway=fake.ipv4(),
                            dns_servers="8.8.8.8,8.8.4.4",
                        )
        self.stdout.write("✔️ Network interfaces ready")

        # Create Tenants
        tenants = self._create_or_get_models(
            models.Tenant,
            lambda: {
                "name": fake.company(),
                "description": fake.text(),
                "status": random.choice(["active", "inactive"]),
            },
            5,
            skip_existing,
            "Tenant",
        )
        self.stdout.write("✔️ Tenants ready")

        # Create Quotas
        for _ in range(10):
            baremetal_group = random.choice(host_groups)
            tenant = random.choice(tenants)
            if (
                not models.BaremetalGroupTenantQuota.objects.filter(
                    group=baremetal_group, tenant=tenant
                ).exists()
                or not skip_existing
            ):
                if models.BaremetalGroupTenantQuota.objects.filter(
                    group=baremetal_group, tenant=tenant
                ).exists():
                    quota = models.BaremetalGroupTenantQuota.objects.get(
                        group=baremetal_group, tenant=tenant
                    )
                    quota.cpu_quota_percentage = random.uniform(0.1, 1.0)
                    quota.memory_quota = random.randint(4096, 32768)
                    quota.storage_quota = random.randint(500, 5000)
                    quota.save()
                else:
                    models.BaremetalGroupTenantQuota.objects.create(
                        group=baremetal_group,
                        tenant=tenant,
                        cpu_quota_percentage=random.uniform(0.1, 1.0),
                        memory_quota=random.randint(4096, 32768),
                        storage_quota=random.randint(500, 5000),
                    )
        self.stdout.write("✔️ Tenant quotas ready")

        # Create VM Specifications
        vm_specs = self._create_or_get_models(
            models.VirtualMachineSpecification,
            lambda: {
                "name": fake.word().capitalize(),
                "generation": f"gen-{random.randint(1, 5)}",
                "required_cpu": random.randint(1, 16),
                "required_memory": random.randint(1024, 8192),
                "required_storage": random.randint(50, 500),
            },
            5,
            skip_existing,
            "VirtualMachineSpecification",
        )
        self.stdout.write("✔️ VM specifications ready")

        # Create K8s Clusters
        clusters = self._create_or_get_models(
            models.K8sCluster,
            lambda: {
                "name": f"K8s-{fake.word()}",
                "version": f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
                "tenant": random.choice(tenants),
                "scheduling_mode": random.choice(
                    ["spread_rack", "balanced", "spread_resource", "default"]
                ),
                "description": fake.text(),
                "status": random.choice(["active", "inactive"]),
            },
            3,
            skip_existing,
            "K8sCluster",
        )
        self.stdout.write("✔️ Kubernetes clusters ready")

        # Create VMs
        vms = self._create_or_get_models(
            models.VirtualMachine,
            lambda: {
                "name": f"VM-{fake.word()}",
                "tenant": random.choice(tenants),
                "baremetal": random.choice(baremetals),
                "specification": random.choice(vm_specs),
                "k8s_cluster": random.choice(clusters + [None]),
                "type": random.choice(
                    ["control-plane", "worker", "management", "other"]
                ),
                "status": random.choice(["active", "inactive"]),
            },
            10,
            skip_existing,
            "VirtualMachine",
        )
        self.stdout.write("✔️ Virtual machines ready")

        # Create Plugins
        for cluster in clusters:
            for _ in range(2):
                plugin_name = fake.word().capitalize()
                if (
                    not models.K8sClusterPlugin.objects.filter(
                        cluster=cluster, name=plugin_name
                    ).exists()
                    or not skip_existing
                ):
                    if models.K8sClusterPlugin.objects.filter(
                        cluster=cluster, name=plugin_name
                    ).exists():
                        plugin = models.K8sClusterPlugin.objects.get(
                            cluster=cluster, name=plugin_name
                        )
                        plugin.version = (
                            f"v{random.randint(1, 3)}.{random.randint(0, 9)}"
                        )
                        plugin.status = random.choice(["active", "inactive", "error"])
                        plugin.additional_info = {"notes": fake.sentence()}
                        plugin.save()
                    else:
                        models.K8sClusterPlugin.objects.create(
                            cluster=cluster,
                            name=plugin_name,
                            version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
                            status=random.choice(["active", "inactive", "error"]),
                            additional_info={"notes": fake.sentence()},
                        )
        self.stdout.write("✔️ Cluster plugins ready")

        # Create Service Meshes
        meshes = self._create_or_get_models(
            models.ServiceMesh,
            lambda: {
                "name": f"SM-{fake.word()}",
                "type": random.choice(["cilium", "istio", "other"]),
                "description": fake.text(),
                "status": random.choice(["active", "inactive", "error"]),
            },
            3,
            skip_existing,
            "ServiceMesh",
        )
        self.stdout.write("✔️ Service meshes ready")

        # Create K8sClusterToServiceMesh
        for cluster in clusters:
            for mesh in meshes:
                if (
                    not models.K8sClusterToServiceMesh.objects.filter(
                        cluster=cluster, service_mesh=mesh
                    ).exists()
                    or not skip_existing
                ):
                    if models.K8sClusterToServiceMesh.objects.filter(
                        cluster=cluster, service_mesh=mesh
                    ).exists():
                        association = models.K8sClusterToServiceMesh.objects.get(
                            cluster=cluster, service_mesh=mesh
                        )
                        association.role = random.choice(["primary", "secondary"])
                        association.save()
                    else:
                        models.K8sClusterToServiceMesh.objects.create(
                            cluster=cluster,
                            service_mesh=mesh,
                            role=random.choice(["primary", "secondary"]),
                        )
        self.stdout.write("✔️ Linked clusters to service meshes")

        # Create BastionClusterAssociations
        for _ in range(5):
            bastion = random.choice(vms)
            k8s_cluster = random.choice(clusters)
            if (
                not models.BastionClusterAssociation.objects.filter(
                    bastion=bastion, k8s_cluster=k8s_cluster
                ).exists()
                or not skip_existing
            ):
                if models.BastionClusterAssociation.objects.filter(
                    bastion=bastion, k8s_cluster=k8s_cluster
                ).exists():
                    # Update existing association
                    pass  # No fields to update
                else:
                    models.BastionClusterAssociation.objects.create(
                        bastion=bastion,
                        k8s_cluster=k8s_cluster,
                    )
        self.stdout.write("✔️ Created Bastion -> K8s associations")

        # Create Ansible Inventories
        inventories = []
        inventory_names = ["production", "staging", "development"]

        for inv_name in inventory_names:
            inventory, created = models.AnsibleInventory.objects.get_or_create(
                name=inv_name,
                defaults={
                    "description": f"{inv_name.capitalize()} environment inventory",
                    "version": "1.0",
                    "source_type": random.choice(["static", "dynamic", "hybrid"]),
                    "source_plugin": random.choice(
                        ["aws_ec2", "openstack", "vmware", None]
                    ),
                    "source_config": {
                        "regions": (
                            ["us-west-2", "us-east-1"]
                            if inv_name == "production"
                            else ["us-west-2"]
                        ),
                        "filters": {"tag:Environment": inv_name},
                    },
                    "status": "active",
                    "created_by": random.choice(users),
                },
            )
            if created:
                self.stdout.write(f"✔️ Created inventory: {inv_name}")
            inventories.append(inventory)

        # Create Variable Sets
        variable_sets = []

        # Common variables
        common_vars_content = """ansible_user: ubuntu
ansible_ssh_private_key_file: ~/.ssh/id_rsa
ansible_python_interpreter: /usr/bin/python3
timezone: UTC
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org"""

        common_var_set, created = models.AnsibleVariableSet.objects.get_or_create(
            name="common_variables",
            defaults={
                "description": "Common variables for all environments",
                "content": common_vars_content,
                "content_type": "yaml",
                "tags": ["common", "system"],
                "priority": 10,
                "status": "active",
                "created_by": random.choice(users),
            },
        )
        if created:
            self.stdout.write("✔️ Created common variable set")
        variable_sets.append(common_var_set)

        # Database variables
        db_vars_content = """{
  "database_host": "db.example.com",
  "database_port": 5432,
  "database_name": "myapp",
  "database_user": "app_user",
  "database_pool_size": 20
}"""

        db_var_set, created = models.AnsibleVariableSet.objects.get_or_create(
            name="database_variables",
            defaults={
                "description": "Database connection variables",
                "content": db_vars_content,
                "content_type": "json",
                "tags": ["database", "production"],
                "priority": 20,
                "status": "active",
                "created_by": random.choice(users),
            },
        )
        if created:
            self.stdout.write("✔️ Created database variable set")
        variable_sets.append(db_var_set)

        # Associate variable sets with inventories
        for inventory in inventories:
            for var_set in variable_sets:
                association, created = (
                    models.AnsibleInventoryVariableSetAssociation.objects.get_or_create(
                        inventory=inventory,
                        variable_set=var_set,
                        defaults={
                            "load_priority": var_set.priority,
                            "enabled": True,
                            "load_tags": [],
                            "load_config": {"merge_strategy": "override"},
                        },
                    )
                )
                if created:
                    self.stdout.write(
                        f"✔️ Associated {var_set.name} with {inventory.name}"
                    )

        # Create Inventory Variables
        for inventory in inventories:
            env_vars = {
                "environment": inventory.name,
                "backup_enabled": inventory.name == "production",
                "monitoring_level": (
                    "high" if inventory.name == "production" else "medium"
                ),
                "log_level": "info" if inventory.name == "production" else "debug",
            }

            for key, value in env_vars.items():
                inv_var, created = (
                    models.AnsibleInventoryVariable.objects.get_or_create(
                        inventory=inventory,
                        key=key,
                        defaults={
                            "value": str(value),
                            "value_type": (
                                "string" if isinstance(value, str) else "boolean"
                            ),
                        },
                    )
                )
                if created:
                    self.stdout.write(
                        f"✔️ Created inventory variable {key} for {inventory.name}"
                    )

        # Create Ansible Groups for each inventory
        ansible_groups = []

        for inventory in inventories:
            # Create special groups
            all_group, created = models.AnsibleGroup.objects.get_or_create(
                inventory=inventory,
                name="all",
                defaults={
                    "description": "All hosts",
                    "is_special": True,
                    "status": "active",
                },
            )
            if created:
                self.stdout.write(f"✔️ Created special group: all for {inventory.name}")
            ansible_groups.append(all_group)

            ungrouped_group, created = models.AnsibleGroup.objects.get_or_create(
                inventory=inventory,
                name="ungrouped",
                defaults={
                    "description": "Hosts not in any group",
                    "is_special": True,
                    "status": "active",
                },
            )
            if created:
                self.stdout.write(
                    f"✔️ Created special group: ungrouped for {inventory.name}"
                )
            ansible_groups.append(ungrouped_group)

        # Create regular groups for each inventory
        group_names = [
            "webservers",
            "dbservers",
            "appservers",
            "monitoring",
            "loadbalancers",
            "bastion",
            "k8s_control_plane",
            "k8s_workers",
            "management",
        ]

        for inventory in inventories:
            for group_name in group_names:
                group, created = models.AnsibleGroup.objects.get_or_create(
                    inventory=inventory,
                    name=group_name,
                    defaults={
                        "description": fake.text(max_nb_chars=100),
                        "is_special": False,
                        "status": random.choice(["active", "inactive"]),
                    },
                )
                if created:
                    self.stdout.write(
                        f"✔️ Created Ansible group: {group_name} for {inventory.name}"
                    )
                ansible_groups.append(group)

        self.stdout.write("✔️ Ansible groups ready")

        # Create group variables
        common_vars = {
            "webservers": {
                "http_port": 80,
                "max_clients": 200,
                "nginx_version": "1.18.0",
            },
            "dbservers": {
                "db_port": 5432,
                "max_connections": 100,
                "postgres_version": "13.4",
            },
            "k8s_control_plane": {
                "kubernetes_version": "1.24.0",
                "control_plane_endpoint": "10.0.0.10:6443",
                "pod_network_cidr": "10.244.0.0/16",
            },
            "k8s_workers": {
                "kubernetes_version": "1.24.0",
                "container_runtime": "containerd",
                "node_labels": ["worker", "compute"],
            },
        }

        for inventory in inventories:
            for group_name, vars_dict in common_vars.items():
                try:
                    group = models.AnsibleGroup.objects.get(
                        inventory=inventory, name=group_name
                    )
                    for key, value in vars_dict.items():
                        if (
                            not models.AnsibleGroupVariable.objects.filter(
                                group=group, key=key
                            ).exists()
                            or not skip_existing
                        ):
                            value_type = "string"
                            if isinstance(value, bool):
                                value_type = "boolean"
                            elif isinstance(value, int):
                                value_type = "integer"
                            elif isinstance(value, (list, dict)):
                                value_type = "json"
                                value = str(value)

                            if models.AnsibleGroupVariable.objects.filter(
                                group=group, key=key
                            ).exists():
                                var = models.AnsibleGroupVariable.objects.get(
                                    group=group, key=key
                                )
                                var.value = str(value)
                                var.value_type = value_type
                                var.save()
                            else:
                                models.AnsibleGroupVariable.objects.create(
                                    group=group,
                                    key=key,
                                    value=str(value),
                                    value_type=value_type,
                                )
                except models.AnsibleGroup.DoesNotExist:
                    continue

        self.stdout.write("✔️ Group variables ready")

        # Create group relationships (parent-child)
        relationships = [
            ("webservers", "loadbalancers"),
            ("dbservers", "monitoring"),
            ("k8s_control_plane", "management"),
            ("k8s_workers", "appservers"),
        ]

        for inventory in inventories:
            for parent_name, child_name in relationships:
                try:
                    parent = models.AnsibleGroup.objects.get(
                        inventory=inventory, name=parent_name
                    )
                    child = models.AnsibleGroup.objects.get(
                        inventory=inventory, name=child_name
                    )
                    if (
                        not models.AnsibleGroupRelationship.objects.filter(
                            parent_group=parent, child_group=child
                        ).exists()
                        or not skip_existing
                    ):
                        if not models.AnsibleGroupRelationship.objects.filter(
                            parent_group=parent, child_group=child
                        ).exists():
                            models.AnsibleGroupRelationship.objects.create(
                                parent_group=parent, child_group=child
                            )
                except models.AnsibleGroup.DoesNotExist:
                    continue

        self.stdout.write("✔️ Group relationships ready")

        # Assign hosts to groups
        baremetal_content_type = ContentType.objects.get_for_model(models.Baremetal)
        vm_content_type = ContentType.objects.get_for_model(models.VirtualMachine)

        # Assign baremetal servers to groups
        for baremetal in baremetals:
            # Skip some baremetal servers to simulate ungrouped hosts
            if random.random() < 0.1:  # 10% chance to be ungrouped
                continue

            # Get primary network interface for ansible_host
            primary_interface = models.NetworkInterface.objects.filter(
                content_type=ContentType.objects.get_for_model(baremetal),
                object_id=baremetal.id,
                is_primary=True,
            ).first()
            ansible_host = primary_interface.ipv4_address if primary_interface else None

            # Assign to each inventory
            for inventory in inventories:
                group = random.choice(
                    [
                        g
                        for g in ansible_groups
                        if not g.is_special and g.inventory == inventory
                    ]
                )

                if (
                    not models.AnsibleHost.objects.filter(
                        inventory=inventory,
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                    ).exists()
                    or not skip_existing
                ):
                    if models.AnsibleHost.objects.filter(
                        inventory=inventory,
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                    ).exists():
                        host = models.AnsibleHost.objects.get(
                            inventory=inventory,
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                        )
                        host.group = group
                        host.ansible_host = ansible_host
                        host.aliases = [f"{baremetal.name}-{inventory.name}"]
                        host.status = "active"
                        host.metadata = {
                            "server_type": "baremetal",
                            "rack_location": f"{baremetal.rack.name if baremetal.rack else 'Unknown'}-{baremetal.unit}",
                            "serial_number": baremetal.serial_number,
                        }
                        host.save()
                    else:
                        models.AnsibleHost.objects.create(
                            inventory=inventory,
                            group=group,
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                            ansible_host=ansible_host,
                            ansible_port=22,
                            ansible_user="root",
                            aliases=[f"{baremetal.name}-{inventory.name}"],
                            status="active",
                            metadata={
                                "server_type": "baremetal",
                                "rack_location": f"{baremetal.rack.name if baremetal.rack else 'Unknown'}-{baremetal.unit}",
                                "serial_number": baremetal.serial_number,
                            },
                        )

        # Assign VMs to groups
        for vm in vms:
            # Skip some VMs to simulate ungrouped hosts
            if random.random() < 0.1:  # 10% chance to be ungrouped
                continue

            # Get primary network interface for ansible_host
            primary_interface = None
            if vm.baremetal:
                primary_interface = models.NetworkInterface.objects.filter(
                    content_type=ContentType.objects.get_for_model(vm.baremetal),
                    object_id=vm.baremetal.id,
                    is_primary=True,
                ).first()
            ansible_host = primary_interface.ipv4_address if primary_interface else None

            # Assign to each inventory
            for inventory in inventories:
                # Assign VMs to appropriate groups based on their type
                if vm.type == "control-plane":
                    group = models.AnsibleGroup.objects.get(
                        inventory=inventory, name="k8s_control_plane"
                    )
                elif vm.type == "worker":
                    group = models.AnsibleGroup.objects.get(
                        inventory=inventory, name="k8s_workers"
                    )
                elif vm.type == "management":
                    group = models.AnsibleGroup.objects.get(
                        inventory=inventory, name="management"
                    )
                else:
                    group = random.choice(
                        [
                            g
                            for g in ansible_groups
                            if not g.is_special and g.inventory == inventory
                        ]
                    )

                if (
                    not models.AnsibleHost.objects.filter(
                        inventory=inventory,
                        content_type=vm_content_type,
                        object_id=vm.id,
                    ).exists()
                    or not skip_existing
                ):
                    if models.AnsibleHost.objects.filter(
                        inventory=inventory,
                        content_type=vm_content_type,
                        object_id=vm.id,
                    ).exists():
                        host = models.AnsibleHost.objects.get(
                            inventory=inventory,
                            content_type=vm_content_type,
                            object_id=vm.id,
                        )
                        host.group = group
                        host.ansible_host = ansible_host
                        host.aliases = [f"{vm.name}-{inventory.name}"]
                        host.status = "active"
                        host.metadata = {
                            "server_type": "virtual_machine",
                            "vm_type": vm.type,
                            "tenant": vm.tenant.name,
                            "k8s_cluster": (
                                vm.k8s_cluster.name if vm.k8s_cluster else None
                            ),
                        }
                        host.save()
                    else:
                        models.AnsibleHost.objects.create(
                            inventory=inventory,
                            group=group,
                            content_type=vm_content_type,
                            object_id=vm.id,
                            ansible_host=ansible_host,
                            ansible_port=22,
                            ansible_user="ubuntu",
                            aliases=[f"{vm.name}-{inventory.name}"],
                            status="active",
                            metadata={
                                "server_type": "virtual_machine",
                                "vm_type": vm.type,
                                "tenant": vm.tenant.name,
                                "k8s_cluster": (
                                    vm.k8s_cluster.name if vm.k8s_cluster else None
                                ),
                            },
                        )

        self.stdout.write("✔️ Assigned hosts to Ansible groups")

        # Create Host Variables
        for inventory in inventories:
            hosts = models.AnsibleHost.objects.filter(inventory=inventory)
            for host in hosts[:5]:  # Limit to first 5 hosts per inventory
                host_vars = {
                    "app_version": f"1.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    "deployment_id": fake.uuid4(),
                    "last_backup": fake.date_time_this_month().isoformat(),
                }

                for key, value in host_vars.items():
                    host_var, created = (
                        models.AnsibleHostVariable.objects.get_or_create(
                            host=host,
                            key=key,
                            defaults={
                                "value": str(value),
                                "value_type": "string",
                            },
                        )
                    )
                    if created:
                        self.stdout.write(f"✔️ Created host variable {key} for {host}")

        # Create Inventory Plugins
        for inventory in inventories:
            if inventory.source_type in ["dynamic", "hybrid"]:
                plugin_config = {
                    "regions": inventory.source_config.get("regions", ["us-west-2"]),
                    "filters": inventory.source_config.get("filters", {}),
                    "keyed_groups": [
                        {"key": "tags.Environment", "prefix": "env"},
                        {"key": "instance_type", "prefix": "type"},
                    ],
                }

                plugin, created = models.AnsibleInventoryPlugin.objects.get_or_create(
                    inventory=inventory,
                    name=inventory.source_plugin or "aws_ec2",
                    defaults={
                        "config": plugin_config,
                        "enabled": True,
                        "priority": 1,
                        "cache_timeout": 300,
                    },
                )
                if created:
                    self.stdout.write(
                        f"✔️ Created plugin {plugin.name} for {inventory.name}"
                    )

        # Create Inventory Templates
        template_content = """all:
  children:
    {% for group in groups %}
    {{ group.name }}:
      hosts:
        {% for host in group.hosts %}
        {{ host.name }}:
          ansible_host: {{ host.ansible_host }}
          ansible_user: {{ host.ansible_user }}
        {% endfor %}
      vars:
        {% for key, value in group.variables.items() %}
        {{ key }}: {{ value }}
        {% endfor %}
    {% endfor %}"""

        template, created = models.AnsibleInventoryTemplate.objects.get_or_create(
            name="yaml_inventory_template",
            defaults={
                "description": "YAML format inventory template",
                "template_type": "yaml",
                "template_content": template_content,
                "variables": {"groups": [], "hosts": []},
            },
        )
        if created:
            self.stdout.write("✔️ Created inventory template")

        self.stdout.write(self.style.SUCCESS("🎉 Fake data generation complete!"))

    def _create_or_get_models(
        self, model_class, data_generator, count, skip_existing, model_name
    ) -> list:
        """Helper method to create or get models with proper handling of existing data"""
        models_list = []
        for _ in range(count):
            data = data_generator()

            # Try to find existing model by name or unique identifier
            existing_model = None
            if "name" in data:
                existing_model = model_class.objects.filter(name=data["name"]).first()
            elif "serial_number" in data:
                existing_model = model_class.objects.filter(
                    serial_number=data["serial_number"]
                ).first()
            elif "pr_number" in data:
                existing_model = model_class.objects.filter(
                    pr_number=data["pr_number"]
                ).first()
            elif "po_number" in data:
                existing_model = model_class.objects.filter(
                    po_number=data["po_number"]
                ).first()

            if existing_model and skip_existing:
                models_list.append(existing_model)
                self.stdout.write(
                    f"⚠️ {model_name} already exists: {existing_model.name if hasattr(existing_model, 'name') else existing_model}"
                )
            else:
                if existing_model:
                    # Update existing model
                    for key, value in data.items():
                        setattr(existing_model, key, value)
                    existing_model.save()
                    models_list.append(existing_model)
                    self.stdout.write(
                        f"🔄 Updated {model_name}: {existing_model.name if hasattr(existing_model, 'name') else existing_model}"
                    )
                else:
                    # Create new model
                    new_model = model_class.objects.create(**data)
                    models_list.append(new_model)
                    self.stdout.write(
                        f"✔️ Created {model_name}: {new_model.name if hasattr(new_model, 'name') else new_model}"
                    )

        return models_list

    def _clear_all_data(self) -> None:
        """Clear all data from all models"""
        # Clear in reverse dependency order to avoid foreign key constraints
        # Clear new Ansible models first
        models.AnsibleHostVariable.objects.all().delete()
        models.AnsibleInventoryPlugin.objects.all().delete()
        models.AnsibleInventoryTemplate.objects.all().delete()
        models.AnsibleInventoryVariableSetAssociation.objects.all().delete()
        models.AnsibleVariableSet.objects.all().delete()
        models.AnsibleInventoryVariable.objects.all().delete()
        models.AnsibleHost.objects.all().delete()
        models.AnsibleGroupVariable.objects.all().delete()
        models.AnsibleGroupRelationship.objects.all().delete()
        models.AnsibleGroup.objects.all().delete()
        models.AnsibleInventory.objects.all().delete()

        # Clear existing models
        models.BastionClusterAssociation.objects.all().delete()
        models.K8sClusterToServiceMesh.objects.all().delete()
        models.ServiceMesh.objects.all().delete()
        models.K8sClusterPlugin.objects.all().delete()
        models.VirtualMachine.objects.all().delete()
        models.K8sCluster.objects.all().delete()
        models.VirtualMachineSpecification.objects.all().delete()
        models.BaremetalGroupTenantQuota.objects.all().delete()
        models.Tenant.objects.all().delete()
        models.NetworkInterface.objects.all().delete()
        models.Baremetal.objects.all().delete()
        models.BaremetalModel.objects.all().delete()
        models.Brand.objects.all().delete()
        models.PurchaseOrder.objects.all().delete()
        models.PurchaseRequisition.objects.all().delete()
        models.BaremetalGroup.objects.all().delete()
        models.Rack.objects.all().delete()
        models.Room.objects.all().delete()
        models.DataCenter.objects.all().delete()
        models.Phase.objects.all().delete()
        models.Fabrication.objects.all().delete()

        # Clear users (except superuser)
        User = get_user_model()
        User.objects.filter(is_superuser=False).delete()

        # Clear groups (except built-in Django groups)
        Group.objects.filter(
            name__in=["admin", "maintainer", "viewer", "operator"]
        ).delete()
