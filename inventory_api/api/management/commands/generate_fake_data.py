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

        # Create Infrastructure Hierarchy: Fabs → Phases → DataCenters → Rooms → Racks
        fabs = self._create_or_get_models(
            models.Fab,
            lambda: {"name": f"Fab-{fake.word()}", "external_system_id": fake.uuid4()},
            3,
            skip_existing,
            "Fab",
        )

        # Create Phases (each belongs to a fabrication)
        phases = []
        for i in range(5):  # Create 5 phases across the fabs
            selected_fab = random.choice(fabs)
            phase_data = {
                "name": f"Phase-{fake.word()}",
                "external_system_id": fake.uuid4(),
                "fab": selected_fab,
            }
            if skip_existing:
                phase, created = models.Phase.objects.get_or_create(
                    name=phase_data["name"], defaults=phase_data
                )
                if created:
                    self.stdout.write(f"✔️ Created Phase: {phase.name}")
                else:
                    self.stdout.write(f"⚠️ Phase already exists: {phase.name}")
            else:
                phase = models.Phase.objects.create(**phase_data)
                self.stdout.write(f"✔️ Created Phase: {phase.name}")
            phases.append(phase)

        # Create DataCenters (each belongs to a phase)
        data_centers = []
        for i in range(4):  # Create 4 datacenters across the phases
            phase = random.choice(phases)
            dc_data = {
                "name": f"DC-{fake.word()}",
                "external_system_id": fake.uuid4(),
                "phase": phase,
            }
            if skip_existing:
                dc, created = models.DataCenter.objects.get_or_create(
                    name=dc_data["name"], defaults=dc_data
                )
                if created:
                    self.stdout.write(f"✔️ Created DataCenter: {dc.name}")
                else:
                    self.stdout.write(f"⚠️ DataCenter already exists: {dc.name}")
            else:
                dc = models.DataCenter.objects.create(**dc_data)
                self.stdout.write(f"✔️ Created DataCenter: {dc.name}")
            data_centers.append(dc)

        # Create Rooms (each belongs to a datacenter)
        rooms = []
        for i in range(8):  # Create 8 rooms across the datacenters
            dc = random.choice(data_centers)
            room_data = {
                "name": f"Room-{fake.word()}",
                "external_system_id": fake.uuid4(),
                "datacenter": dc,
            }
            if skip_existing:
                room, created = models.Room.objects.get_or_create(
                    name=room_data["name"], defaults=room_data
                )
                if created:
                    self.stdout.write(f"✔️ Created Room: {room.name}")
                else:
                    self.stdout.write(f"⚠️ Room already exists: {room.name}")
            else:
                room = models.Room.objects.create(**room_data)
                self.stdout.write(f"✔️ Created Room: {room.name}")
            rooms.append(room)

        # Create Racks (each belongs to a room)
        racks = []
        for i in range(12):  # Create 12 racks across the rooms
            room = random.choice(rooms)
            rack_data = {
                "name": f"Rack-{fake.word()}",
                "bgp_number": str(fake.random_int(min=1000, max=9999)),
                "as_number": fake.random_int(min=10000, max=99999),
                "external_system_id": fake.uuid4(),
                "room": room,
            }
            if skip_existing:
                rack, created = models.Rack.objects.get_or_create(
                    name=rack_data["name"], defaults=rack_data
                )
                if created:
                    self.stdout.write(f"✔️ Created Rack: {rack.name}")
                else:
                    self.stdout.write(f"⚠️ Rack already exists: {rack.name}")
            else:
                rack = models.Rack.objects.create(**rack_data)
                self.stdout.write(f"✔️ Created Rack: {rack.name}")
            racks.append(rack)
        self.stdout.write("✔️ Racks ready")

        # Create Baremetal Groups
        host_groups = self._create_or_get_models(
            models.BaremetalGroup,
            lambda: {
                "name": fake.word().capitalize(),
                "description": fake.text(max_nb_chars=100),
                "total_cpu_cores": 256,
                "total_memory_mib": 131072,
                "total_storage_gb": 50000,
                "available_cpu_cores": 128,
                "available_memory_mib": 65536,
                "available_storage_gb": 25000,
                "status": random.choice(["active", "inactive"]),
            },
            3,
            skip_existing,
            "BaremetalGroup",
        )
        self.stdout.write("✔️ Baremetal groups ready")

        # Create Vendors (replaces old Manufacturers and Suppliers)
        vendors = self._create_or_get_models(
            models.Vendor,
            lambda: {
                "name": fake.company(),
                "contact_email": fake.email(),
                "contact_phone": fake.phone_number()[:20],
                "address": fake.address(),
            },
            5,
            skip_existing,
            "Vendor",
        )

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

        pos = []
        for i in range(5):
            selected_pr = random.choice(prs)
            selected_vendor = random.choice(vendors) if vendors else None
            po_data = {
                "name": f"PO-{i+1}",
                "po_number": f"PO-{fake.unique.random_number(6)}",
                "purchase_requisition": selected_pr,
                "supplier": selected_vendor,
                "payment_terms": random.choice(["net30", "net45", "net60"]),
                "amount": fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                "used": fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                "description": fake.text(max_nb_chars=200),
            }
            po_obj, created = models.PurchaseOrder.objects.get_or_create(
                po_number=po_data["po_number"], defaults=po_data
            )
            pos.append(po_obj)
            if created and not skip_existing:
                self.stdout.write(f"  Created PurchaseOrder: {po_obj.po_number}")

        if not skip_existing:
            self.stdout.write(f"✔️ PurchaseOrder ready ({len(pos)} total)")

        # Create BaremetalModels
        baremetal_models = self._create_or_get_models(
            models.BaremetalModel,
            lambda: {
                "name": f"Model-{fake.word()}",
                "manufacturer": random.choice(vendors) if vendors else None,
                "cpu_cores": 64,
                "memory_mib": 65536,
            },
            5,
            skip_existing,
            "BaremetalModel",
        )

        # Create Units per rack
        units_by_rack = {}
        for rack in racks:
            rack_units = []
            for i in range(1, rack.height_units + 1):
                name = f"U{i}"
                unit_obj, _ = models.Unit.objects.get_or_create(
                    rack=rack, name=name, defaults={"unit_number": i}
                )
                rack_units.append(unit_obj)
            units_by_rack[rack.id] = rack_units

        # Create Baremetal Servers
        baremetals = self._create_or_get_models(
            models.Baremetal,
            lambda: {
                "name": f"BM-{fake.domain_word()}",
                "serial_number": fake.uuid4(),
                "model": random.choice(baremetal_models),
                "unit": random.choice(units_by_rack[(selected_rack := random.choice(racks)).id]),
                "status": random.choice(["active", "inactive", "pending", "retired"]),
                "cpu_cores": 64,
                "memory_mib": 65536,
                "storage_gb": 10000,
                "available_cpu_cores": random.randint(8, 64),
                "available_memory_mib": random.randint(8192, 65536),
                "available_storage_gb": random.randint(500, 5000),
                "baremetal_group": random.choice(host_groups),
                "purchase_requisition": random.choice(prs),
                "purchase_order": random.choice(pos),
                "external_system_id": fake.uuid4(),
                "failure_zone": random.choice(["fz1", "fz2", "fz3", "fz4"]),
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
                    baremetal_group=baremetal_group, tenant=tenant
                ).exists()
                or not skip_existing
            ):
                if models.BaremetalGroupTenantQuota.objects.filter(
                    baremetal_group=baremetal_group, tenant=tenant
                ).exists():
                    quota = models.BaremetalGroupTenantQuota.objects.get(
                        baremetal_group=baremetal_group, tenant=tenant
                    )
                    quota.cpu_quota = random.uniform(0.1, 1.0)
                    quota.memory_quota = random.uniform(0.1, 1.0)
                    quota.storage_quota = random.uniform(0.1, 1.0)
                    quota.save()
                else:
                    models.BaremetalGroupTenantQuota.objects.create(
                        baremetal_group=baremetal_group,
                        tenant=tenant,
                        cpu_quota=random.uniform(0.1, 1.0),
                        memory_quota=random.uniform(0.1, 1.0),
                        storage_quota=random.uniform(0.1, 1.0),
                    )
        self.stdout.write("✔️ Tenant quotas ready")

        # Create VM Specifications
        vm_specs = self._create_or_get_models(
            models.VirtualMachineSpecification,
            lambda: {
                "name": fake.word().capitalize(),
                "generation": f"gen-{random.randint(1, 5)}",
                "required_cpu_cores": random.randint(1, 16),
                "required_memory_mib": random.randint(1024, 8192),
                "required_storage_gb": random.randint(50, 500),
            },
            5,
            skip_existing,
            "VirtualMachineSpecification",
        )
        self.stdout.write("✔️ VM specifications ready")

        # Create K8s Clusters
        # Create scheduling strategies first if they don't exist
        scheduling_strategies = list(models.SchedulingStrategy.objects.all())
        if not scheduling_strategies and tenants:
            for strategy_name in ["spread_rack", "balanced", "spread_resource", "default"]:
                strategy = models.SchedulingStrategy.objects.create(
                    name=f"Strategy-{strategy_name}",
                    tenant=random.choice(tenants),
                )
                scheduling_strategies.append(strategy)

        # Create regions first if they don't exist
        regions = list(models.Region.objects.all())
        if not regions:
            for i in range(3):
                region = models.Region.objects.create(name=f"Region-{fake.word()}")
                regions.append(region)

        clusters = self._create_or_get_models(
            models.K8sCluster,
            lambda: {
                "name": f"K8s-{fake.word()}",
                "version": f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
                "tenant": random.choice(tenants),
                "region": random.choice(regions),
                "scheduling_strategy": (
                    random.choice(scheduling_strategies) if scheduling_strategies else None
                ),
                "description": fake.text(),
                "status": random.choice(["active", "inactive"]),
            },
            3,
            skip_existing,
            "K8sCluster",
        )
        self.stdout.write("✔️ Kubernetes clusters ready")

        # Create VirtualMachineRoles first if they don't exist
        vm_roles = list(models.VirtualMachineRole.objects.all())
        if not vm_roles:
            for role_name in ["control-plane", "worker", "management", "other"]:
                role = models.VirtualMachineRole.objects.create(name=role_name)
                vm_roles.append(role)

        # Create VMs
        vms = self._create_or_get_models(
            models.VirtualMachine,
            lambda: {
                "name": f"VM-{fake.word()}",
                "tenant": random.choice(tenants),
                "region": random.choice(regions),
                "baremetal": random.choice(baremetals),
                "specification": random.choice(vm_specs),
                "k8s_cluster": random.choice(clusters + [None]),
                "virtual_machine_role": random.choice(vm_roles),
                "status": random.choice(["active", "inactive"]),
            },
            10,
            skip_existing,
            "VirtualMachine",
        )
        self.stdout.write("✔️ Virtual machines ready")

        # Create Plugins
        plugins = []
        for i in range(5):
            plugin_name = f"Plugin-{fake.word().capitalize()}"
            plugin, created = models.K8sClusterPlugin.objects.get_or_create(
                name=plugin_name,
                defaults={
                    "versions": [f"v{random.randint(1, 3)}.{random.randint(0, 9)}"],
                    "status": random.choice(["active", "inactive", "error"]),
                    "additional_info": {"notes": fake.sentence()},
                },
            )
            plugins.append(plugin)

        # Create Plugin Associations
        for cluster in clusters:
            for _ in range(2):
                plugin = random.choice(plugins)
                if not models.K8sClusterPluginAssociation.objects.filter(
                    k8s_cluster=cluster, k8s_cluster_plugin=plugin
                ).exists():
                    models.K8sClusterPluginAssociation.objects.create(
                        k8s_cluster=cluster,
                        k8s_cluster_plugin=plugin,
                        version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
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
                        k8s_cluster=cluster, service_mesh=mesh
                    ).exists()
                    or not skip_existing
                ):
                    if models.K8sClusterToServiceMesh.objects.filter(
                        k8s_cluster=cluster, service_mesh=mesh
                    ).exists():
                        association = models.K8sClusterToServiceMesh.objects.get(
                            k8s_cluster=cluster, service_mesh=mesh
                        )
                        association.role = random.choice(["primary", "secondary"])
                        association.save()
                    else:
                        models.K8sClusterToServiceMesh.objects.create(
                            k8s_cluster=cluster,
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
                    "source_type": random.choice(["static", "dynamic"]),
                    "status": "active",
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
                        ansible_inventory=inventory,
                        ansible_variable_set=var_set,
                        defaults={
                            "load_priority": var_set.priority,
                            "enabled": True,
                        },
                    )
                )
                if created:
                    self.stdout.write(f"✔️ Associated {var_set.name} with {inventory.name}")

        # Note: AnsibleInventoryVariable model has been removed from the current schema
        # If needed, variables should be stored in the AnsibleVariableSet or in inventory config
        self.stdout.write("✔️ Inventory variables (stored in variable sets)")

        # Create Ansible Groups for each inventory
        ansible_groups = []

        for inventory in inventories:
            # Create special groups
            all_group, created = models.AnsibleGroup.objects.get_or_create(
                ansible_inventory=inventory,
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
                ansible_inventory=inventory,
                name="ungrouped",
                defaults={
                    "description": "Hosts not in any group",
                    "is_special": True,
                    "status": "active",
                },
            )
            if created:
                self.stdout.write(f"✔️ Created special group: ungrouped for {inventory.name}")
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
                    ansible_inventory=inventory,
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
                        ansible_inventory=inventory, name=group_name
                    )
                    for key, value in vars_dict.items():
                        if (
                            not models.AnsibleGroupVariable.objects.filter(
                                ansible_group=group, name=key
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
                                ansible_group=group, name=key
                            ).exists():
                                var = models.AnsibleGroupVariable.objects.get(
                                    ansible_group=group, name=key
                                )
                                var.content = str(value)
                                var.content_type = "yaml"
                                var.save()
                            else:
                                models.AnsibleGroupVariable.objects.create(
                                    ansible_group=group,
                                    name=key,
                                    content=str(value),
                                    content_type="yaml",
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
                        ansible_inventory=inventory, name=parent_name
                    )
                    child = models.AnsibleGroup.objects.get(
                        ansible_inventory=inventory, name=child_name
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
                        if not g.is_special and g.ansible_inventory == inventory
                    ]
                )

                if (
                    not models.AnsibleHost.objects.filter(
                        ansible_inventory=inventory,
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                    ).exists()
                    or not skip_existing
                ):
                    if models.AnsibleHost.objects.filter(
                        ansible_inventory=inventory,
                        content_type=baremetal_content_type,
                        object_id=baremetal.id,
                    ).exists():
                        host = models.AnsibleHost.objects.get(
                            ansible_inventory=inventory,
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                        )
                        host.ansible_host = ansible_host
                        host.aliases = [f"{baremetal.name}-{inventory.name}"]
                        host.status = "active"
                        host.metadata = {
                            "server_type": "baremetal",
                            "rack_location": f"{baremetal.unit.rack.name if baremetal.unit else 'Unknown'}-{baremetal.unit.name if baremetal.unit else 'Unknown'}",
                            "serial_number": baremetal.serial_number,
                        }
                        host.save()
                        host.ansible_groups.set([group])
                    else:
                        host = models.AnsibleHost.objects.create(
                            ansible_inventory=inventory,
                            content_type=baremetal_content_type,
                            object_id=baremetal.id,
                            ansible_host=ansible_host,
                            ansible_port=22,
                            ansible_user="root",
                            aliases=[f"{baremetal.name}-{inventory.name}"],
                            status="active",
                            metadata={
                                "server_type": "baremetal",
                                "rack_location": f"{baremetal.unit.rack.name if baremetal.unit else 'Unknown'}-{baremetal.unit.name if baremetal.unit else 'Unknown'}",
                                "serial_number": baremetal.serial_number,
                            },
                        )
                        host.ansible_groups.set([group])

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
                # Assign VMs to appropriate groups based on their virtual machine role
                if vm.virtual_machine_role.name == "control-plane":
                    group = models.AnsibleGroup.objects.get(
                        ansible_inventory=inventory, name="k8s_control_plane"
                    )
                elif vm.virtual_machine_role.name == "worker":
                    group = models.AnsibleGroup.objects.get(
                        ansible_inventory=inventory, name="k8s_workers"
                    )
                elif vm.virtual_machine_role.name == "management":
                    group = models.AnsibleGroup.objects.get(
                        ansible_inventory=inventory, name="management"
                    )
                else:
                    group = random.choice(
                        [
                            g
                            for g in ansible_groups
                            if not g.is_special and g.ansible_inventory == inventory
                        ]
                    )

                if (
                    not models.AnsibleHost.objects.filter(
                        ansible_inventory=inventory,
                        content_type=vm_content_type,
                        object_id=vm.id,
                    ).exists()
                    or not skip_existing
                ):
                    if models.AnsibleHost.objects.filter(
                        ansible_inventory=inventory,
                        content_type=vm_content_type,
                        object_id=vm.id,
                    ).exists():
                        host = models.AnsibleHost.objects.get(
                            ansible_inventory=inventory,
                            content_type=vm_content_type,
                            object_id=vm.id,
                        )
                        host.ansible_host = ansible_host
                        host.aliases = [f"{vm.name}-{inventory.name}"]
                        host.status = "active"
                        host.metadata = {
                            "server_type": "virtual_machine",
                            "vm_type": vm.virtual_machine_role.name,
                            "tenant": vm.tenant.name,
                            "k8s_cluster": (vm.k8s_cluster.name if vm.k8s_cluster else None),
                        }
                        host.save()
                        host.ansible_groups.set([group])
                    else:
                        host = models.AnsibleHost.objects.create(
                            ansible_inventory=inventory,
                            content_type=vm_content_type,
                            object_id=vm.id,
                            ansible_host=ansible_host,
                            ansible_port=22,
                            ansible_user="ubuntu",
                            aliases=[f"{vm.name}-{inventory.name}"],
                            status="active",
                            metadata={
                                "server_type": "virtual_machine",
                                "vm_type": vm.virtual_machine_role.name,
                                "tenant": vm.tenant.name,
                                "k8s_cluster": (vm.k8s_cluster.name if vm.k8s_cluster else None),
                            },
                        )
                        host.ansible_groups.set([group])

        self.stdout.write("✔️ Assigned hosts to Ansible groups")

        # Create Host Variables
        for inventory in inventories:
            hosts = models.AnsibleHost.objects.filter(ansible_inventory=inventory)
            for host in hosts[:5]:  # Limit to first 5 hosts per inventory
                host_vars = {
                    "app_version": f"1.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    "deployment_id": fake.uuid4(),
                    "last_backup": fake.date_time_this_month().isoformat(),
                }

                for key, value in host_vars.items():
                    host_var, created = models.AnsibleHostVariable.objects.get_or_create(
                        ansible_host=host,
                        name=key,
                        defaults={
                            "content": str(value),
                            "content_type": "yaml",
                        },
                    )
                    if created:
                        self.stdout.write(f"✔️ Created host variable {key} for {host}")

        # Note: AnsibleInventoryPlugin model has been removed from the current schema
        # If needed, plugin configuration should be stored in the inventory's source_config field
        self.stdout.write("✔️ Inventory plugins (configured in inventory source_config)")

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
                existing_model = model_class.objects.filter(pr_number=data["pr_number"]).first()
            elif "po_number" in data:
                existing_model = model_class.objects.filter(po_number=data["po_number"]).first()

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
        models.AnsibleGroupVariable.objects.all().delete()
        models.AnsibleInventoryTemplate.objects.all().delete()
        models.AnsibleInventoryVariableSetAssociation.objects.all().delete()
        models.AnsibleVariableSet.objects.all().delete()
        models.AnsibleHost.objects.all().delete()
        models.AnsibleGroupRelationship.objects.all().delete()
        models.AnsibleGroup.objects.all().delete()
        models.AnsibleInventory.objects.all().delete()

        # Clear existing models
        models.GPUAllocation.objects.all().delete()
        models.BastionClusterAssociation.objects.all().delete()
        models.ClusterTemplateVirtualMachine.objects.all().delete()
        models.K8sClusterPluginAssociation.objects.all().delete()
        models.K8sClusterToServiceMesh.objects.all().delete()
        models.ServiceMesh.objects.all().delete()
        models.K8sClusterPlugin.objects.all().delete()
        models.VirtualMachine.objects.all().delete()
        models.K8sCluster.objects.all().delete()
        models.ClusterTemplate.objects.all().delete()
        models.VirtualMachineSpecification.objects.all().delete()
        models.PhysicalGPU.objects.all().delete()
        models.BaremetalModelGPU.objects.all().delete()
        models.BaremetalGroupTenantQuota.objects.all().delete()
        models.Tenant.objects.all().delete()
        models.NetworkInterface.objects.all().delete()
        models.Baremetal.objects.all().delete()
        models.Unit.objects.all().delete()
        models.BaremetalModel.objects.all().delete()
        models.PhysicalGPUModel.objects.all().delete()
        models.Vendor.objects.all().delete()
        models.PurchaseOrder.objects.all().delete()
        models.PurchaseRequisition.objects.all().delete()
        models.BaremetalGroup.objects.all().delete()
        models.Rack.objects.all().delete()
        models.Room.objects.all().delete()
        models.DataCenter.objects.all().delete()
        models.Phase.objects.all().delete()
        models.Fab.objects.all().delete()

        # Clear users (except superuser)
        User = get_user_model()
        User.objects.filter(is_superuser=False).delete()

        # Clear groups (except built-in Django groups)
        Group.objects.filter(name__in=["admin", "maintainer", "viewer", "operator"]).delete()
