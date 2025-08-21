import os
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from faker import Faker
from guardian.shortcuts import assign_perm

from inventory_api.api import models  # Replace with your actual app path


class Command(BaseCommand):
    help = "Generate fake data for the Django Ninja project"

    def add_arguments(self, parser):
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
        groups = []
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups.append(group)
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
                user.groups.add(random.choice(groups))
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
            group = random.choice(host_groups)
            tenant = random.choice(tenants)
            if (
                not models.BaremetalGroupTenantQuota.objects.filter(
                    group=group, tenant=tenant
                ).exists()
                or not skip_existing
            ):
                if models.BaremetalGroupTenantQuota.objects.filter(
                    group=group, tenant=tenant
                ).exists():
                    quota = models.BaremetalGroupTenantQuota.objects.get(
                        group=group, tenant=tenant
                    )
                    quota.cpu_quota_percentage = random.uniform(0.1, 1.0)
                    quota.memory_quota = random.randint(4096, 32768)
                    quota.storage_quota = random.randint(500, 5000)
                    quota.save()
                else:
                    models.BaremetalGroupTenantQuota.objects.create(
                        group=group,
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

        # Create Ansible Groups
        ansible_groups = []

        # Create special groups
        all_group, created = models.AnsibleGroup.objects.get_or_create(
            name="all",
            defaults={
                "description": "All hosts",
                "is_special": True,
                "status": "active",
            },
        )
        if created:
            self.stdout.write("✔️ Created special group: all")
        ansible_groups.append(all_group)

        ungrouped_group, created = models.AnsibleGroup.objects.get_or_create(
            name="ungrouped",
            defaults={
                "description": "Hosts not in any group",
                "is_special": True,
                "status": "active",
            },
        )
        if created:
            self.stdout.write("✔️ Created special group: ungrouped")
        ansible_groups.append(ungrouped_group)

        # Create regular groups
        group_names = [
            "webservers",
            "dbservers",
            "appservers",
            "monitoring",
            "loadbalancers",
            "bastion",
            "k8s_control_plane",
            "k8s_workers",
            "production",
            "staging",
            "development",
            "management",
        ]

        for group_name in group_names:
            group, created = models.AnsibleGroup.objects.get_or_create(
                name=group_name,
                defaults={
                    "description": fake.text(max_nb_chars=100),
                    "is_special": False,
                    "status": random.choice(["active", "inactive"]),
                },
            )
            if created:
                self.stdout.write(f"✔️ Created Ansible group: {group_name}")
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
            "production": {
                "environment": "production",
                "backup_enabled": True,
                "monitoring_level": "high",
            },
            "staging": {
                "environment": "staging",
                "backup_enabled": False,
                "monitoring_level": "medium",
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

        for group_name, vars_dict in common_vars.items():
            try:
                group = models.AnsibleGroup.objects.get(name=group_name)
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
            ("production", "webservers"),
            ("production", "dbservers"),
            ("production", "loadbalancers"),
            ("staging", "webservers"),
            ("staging", "dbservers"),
            ("management", "bastion"),
            ("management", "monitoring"),
            ("k8s_control_plane", "management"),
            ("k8s_workers", "appservers"),
        ]

        for parent_name, child_name in relationships:
            try:
                parent = models.AnsibleGroup.objects.get(name=parent_name)
                child = models.AnsibleGroup.objects.get(name=child_name)
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

            group = random.choice([g for g in ansible_groups if not g.is_special])

            # Get primary network interface for ansible_host
            primary_interface = models.NetworkInterface.objects.filter(
                content_type=ContentType.objects.get_for_model(baremetal),
                object_id=baremetal.id,
                is_primary=True,
            ).first()
            ansible_host = primary_interface.ipv4_address if primary_interface else None

            if (
                not models.AnsibleHost.objects.filter(
                    content_type=baremetal_content_type, object_id=baremetal.id
                ).exists()
                or not skip_existing
            ):
                if models.AnsibleHost.objects.filter(
                    content_type=baremetal_content_type, object_id=baremetal.id
                ).exists():
                    host = models.AnsibleHost.objects.get(
                        content_type=baremetal_content_type, object_id=baremetal.id
                    )
                    host.group = group
                    host.ansible_host = ansible_host
                    host.host_vars = {
                        "server_type": "baremetal",
                        "rack_location": f"{baremetal.rack.name if baremetal.rack else 'Unknown'}-{baremetal.unit}",
                        "serial_number": baremetal.serial_number,
                    }
                    host.save()
                else:
                    models.AnsibleHost.objects.create(
                        group=group,
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                        ansible_host=ansible_host,
                        ansible_port=22,
                        ansible_user="root",
                        host_vars={
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

            # Assign VMs to appropriate groups based on their type
            if vm.type == "control-plane":
                group = models.AnsibleGroup.objects.get(name="k8s_control_plane")
            elif vm.type == "worker":
                group = models.AnsibleGroup.objects.get(name="k8s_workers")
            elif vm.type == "management":
                group = models.AnsibleGroup.objects.get(name="management")
            else:
                group = random.choice([g for g in ansible_groups if not g.is_special])

            # Get primary network interface for ansible_host
            primary_interface = None
            if vm.baremetal:
                primary_interface = models.NetworkInterface.objects.filter(
                    content_type=ContentType.objects.get_for_model(vm.baremetal),
                    object_id=vm.baremetal.id,
                    is_primary=True,
                ).first()
            ansible_host = primary_interface.ipv4_address if primary_interface else None

            if (
                not models.AnsibleHost.objects.filter(
                    content_type=vm_content_type, object_id=vm.id
                ).exists()
                or not skip_existing
            ):
                if models.AnsibleHost.objects.filter(
                    content_type=vm_content_type, object_id=vm.id
                ).exists():
                    host = models.AnsibleHost.objects.get(
                        content_type=vm_content_type, object_id=vm.id
                    )
                    host.group = group
                    host.ansible_host = ansible_host
                    host.host_vars = {
                        "server_type": "virtual_machine",
                        "vm_type": vm.type,
                        "tenant": vm.tenant.name,
                        "k8s_cluster": vm.k8s_cluster.name if vm.k8s_cluster else None,
                    }
                    host.save()
                else:
                    models.AnsibleHost.objects.create(
                        group=group,
                        content_type=vm_content_type,
                        object_id=vm.id,
                        ansible_host=ansible_host,
                        ansible_port=22,
                        ansible_user="ubuntu",
                        host_vars={
                            "server_type": "virtual_machine",
                            "vm_type": vm.type,
                            "tenant": vm.tenant.name,
                            "k8s_cluster": (
                                vm.k8s_cluster.name if vm.k8s_cluster else None
                            ),
                        },
                    )

        self.stdout.write("✔️ Assigned hosts to Ansible groups")

        self.stdout.write(self.style.SUCCESS("🎉 Fake data generation complete!"))

    def _create_or_get_models(
        self, model_class, data_generator, count, skip_existing, model_name
    ):
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

    def _clear_all_data(self):
        """Clear all data from all models"""
        # Clear in reverse dependency order to avoid foreign key constraints
        models.AnsibleHost.objects.all().delete()
        models.AnsibleGroupVariable.objects.all().delete()
        models.AnsibleGroupRelationship.objects.all().delete()
        models.AnsibleGroup.objects.all().delete()
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
