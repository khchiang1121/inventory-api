import os
import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm
from virtflow.api import models  # Replace with your actual app path
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Generate fake data for the Django Ninja project"

    def handle(self, *args: tuple, **options: dict) -> None:
        fake = Faker()
        User = get_user_model()

        # Create Groups
        group_names = ['admin', 'maintainer', 'viewer', 'operator']
        groups = [Group.objects.get_or_create(name=name)[0] for name in group_names]
        self.stdout.write("✔️ Created groups")

        # Create Users
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123"),
                account=fake.user_name(),
                status=random.choice(['active', 'inactive'])
            )
            user.groups.add(random.choice(groups))
            users.append(user)

        default_user = User.objects.create_user(
            username="user",
            email=fake.email(),
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123"),
            account="user",
            status="active"
        )
        default_user.groups.add(Group.objects.get(name="maintainer"))
        users.append(default_user)

        self.stdout.write("✔️ Created users")

        # Create Fabrications, Phases, Data Centers, Rooms
        fabrications = [models.Fabrication.objects.create(name=f"Fab-{fake.word()}", old_system_id=fake.uuid4()) for _ in range(3)]
        phases = [models.Phase.objects.create(name=f"Phase-{fake.word()}", old_system_id=fake.uuid4()) for _ in range(3)]
        data_centers = [models.DataCenter.objects.create(name=f"DC-{fake.word()}", old_system_id=fake.uuid4()) for _ in range(3)]
        rooms = [models.Room.objects.create(name=f"Room-{fake.word()}", old_system_id=fake.uuid4()) for _ in range(3)]

        # Create Racks
        racks = [
            models.Rack.objects.create(
                name=f"Rack-{fake.word()}",
                bgp_number=str(fake.random_int(min=1000, max=9999)),
                as_number=fake.random_int(min=10000, max=99999),
                old_system_id=fake.uuid4(),
            )
            for _ in range(5)
        ]
        self.stdout.write("✔️ Created racks")

        # Create Baremetal Groups
        host_groups = [
            models.BaremetalGroup.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=100),
                total_cpu=256,
                total_memory=131072,
                total_storage=50000,
                available_cpu=128,
                available_memory=65536,
                available_storage=25000,
                status=random.choice(['active', 'inactive'])
            ) for _ in range(3)
        ]
        self.stdout.write("✔️ Created baremetal groups")

        # Create Purchase Requisitions & Orders
        prs = [models.PurchaseRequisition.objects.create(
            pr_number=f"PR-{fake.unique.random_number(6)}",
            requested_by=fake.name(),
            department=fake.bs(),
            reason=fake.text(),
        ) for _ in range(5)]

        pos = [models.PurchaseOrder.objects.create(
            po_number=f"PO-{fake.unique.random_number(6)}",
            vendor_name=fake.company(),
            payment_terms="NET 30",
            issued_by=fake.name()
        ) for _ in range(5)]

        # Create Brands and Models
        brands = [models.Brand.objects.create(name=fake.company()) for _ in range(3)]
        baremetal_models = [
            models.BaremetalModel.objects.create(
                name=f"Model-{fake.word()}",
                brand=random.choice(brands),
                total_cpu=64,
                total_memory=65536,
                total_storage=10000
            ) for _ in range(5)
        ]

        # Create Baremetal Servers
        baremetals = [
            models.Baremetal.objects.create(
                name=f"BM-{fake.domain_word()}",
                serial_number=fake.uuid4(),
                model=random.choice(baremetal_models),
                fabrication=random.choice(fabrications),
                phase=random.choice(phases),
                data_center=random.choice(data_centers),
                room=random.choice(rooms).name,
                rack=random.choice(racks),
                unit=f"U{random.randint(1, 48)}",
                status=random.choice(['active', 'inactive', 'pending', 'retired']),
                available_cpu=random.randint(8, 64),
                available_memory=random.randint(8192, 65536),
                available_storage=random.randint(500, 5000),
                group=random.choice(host_groups),
                pr=random.choice(prs),
                po=random.choice(pos),
                old_system_id=fake.uuid4(),
            )
            for _ in range(10)
        ]
        self.stdout.write("✔️ Created baremetal servers")

        # Create Network Interfaces for Baremetal Servers
        baremetal_content_type = ContentType.objects.get_for_model(models.Baremetal)
        
        for baremetal in baremetals:
            for i in range(2):
                models.NetworkInterface.objects.create(
                    content_type=baremetal_content_type,
                    object_id=baremetal.id,
                    name=f"eth{i}",
                    mac_address=fake.mac_address(),
                    is_primary=(i == 0),
                    ipv4_address=fake.ipv4(),
                    ipv4_netmask="255.255.255.0",
                    gateway=fake.ipv4(),
                    dns_servers="8.8.8.8,8.8.4.4"
                )
        self.stdout.write("✔️ Created network interfaces")

        # Create Tenants
        tenants = [
            models.Tenant.objects.create(
                name=fake.company(),
                description=fake.text(),
                status=random.choice(['active', 'inactive'])
            ) for _ in range(5)
        ]
        self.stdout.write("✔️ Created tenants")

        # Create Quotas
        for _ in range(10):
            models.BaremetalGroupTenantQuota.objects.create(
                group=random.choice(host_groups),
                tenant=random.choice(tenants),
                cpu_quota_percentage=random.uniform(0.1, 1.0),
                memory_quota=random.randint(4096, 32768),
                storage_quota=random.randint(500, 5000),
            )
        self.stdout.write("✔️ Created tenant quotas")

        # Create VM Specifications
        vm_specs = [
            models.VirtualMachineSpecification.objects.create(
                name=fake.word().capitalize(),
                generation=f"gen-{random.randint(1, 5)}",
                required_cpu=random.randint(1, 16),
                required_memory=random.randint(1024, 8192),
                required_storage=random.randint(50, 500)
            ) for _ in range(5)
        ]
        self.stdout.write("✔️ Created VM specifications")

        # Create K8s Clusters
        clusters = [
            models.K8sCluster.objects.create(
                name=f"K8s-{fake.word()}",
                version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
                tenant=random.choice(tenants),
                scheduling_mode=random.choice(["spread_rack", "balanced", "spread_resource", "default"]),
                description=fake.text(),
                status=random.choice(["active", "inactive"]),
            )
            for _ in range(3)
        ]
        self.stdout.write("✔️ Created Kubernetes clusters")

        # Create VMs
        vms = [
            models.VirtualMachine.objects.create(
                name=f"VM-{fake.word()}",
                tenant=random.choice(tenants),
                baremetal=random.choice(baremetals),
                specification=random.choice(vm_specs),
                k8s_cluster=random.choice(clusters + [None]),
                type=random.choice(['control-plane', 'worker', 'management', 'other']),
                status=random.choice(['active', 'inactive'])
            ) for _ in range(10)
        ]
        self.stdout.write("✔️ Created virtual machines")

        # Create Plugins
        for cluster in clusters:
            for _ in range(2):
                models.K8sClusterPlugin.objects.create(
                    cluster=cluster,
                    name=fake.word().capitalize(),
                    version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
                    status=random.choice(['active', 'inactive', 'error']),
                    additional_info={"notes": fake.sentence()}
                )
        self.stdout.write("✔️ Created cluster plugins")

        # Create Service Meshes
        meshes = [
            models.ServiceMesh.objects.create(
                name=f"SM-{fake.word()}",
                type=random.choice(['cilium', 'istio', 'other']),
                description=fake.text(),
                status=random.choice(['active', 'inactive', 'error']),
            ) for _ in range(3)
        ]
        self.stdout.write("✔️ Created service meshes")

        # Create K8sClusterToServiceMesh
        for cluster in clusters:
            for mesh in meshes:
                models.K8sClusterToServiceMesh.objects.create(
                    cluster=cluster,
                    service_mesh=mesh,
                    role=random.choice(['primary', 'secondary']),
                )
        self.stdout.write("✔️ Linked clusters to service meshes")

        # Create BastionClusterAssociations
        for _ in range(5):
            models.BastionClusterAssociation.objects.create(
                bastion=random.choice(vms),
                k8s_cluster=random.choice(clusters),
            )
        self.stdout.write("✔️ Created Bastion -> K8s associations")

        self.stdout.write(self.style.SUCCESS("🎉 Fake data generation complete!"))
