import random
from uuid import UUID
from django.core.management.base import BaseCommand
from faker import Faker
from backend import models

class Command(BaseCommand):
    help = "Generate fake data for the Django Ninja project"

    def handle(self, *args, **options):
        fake = Faker()

        # Create Maintainers
        maintainers = []
        for _ in range(10):
            m = models.Maintainer.objects.create(
                name=fake.name(),
                account=fake.user_name(),
                email=fake.email(),
                status=random.choice(['active', 'inactive']),
            )
            maintainers.append(m)
        self.stdout.write("Created maintainers.")

        # Create Maintainer Groups
        maintainer_groups = []
        for _ in range(5):
            group = models.MaintainerGroup.objects.create(
                name=fake.word().capitalize(),
                group_manager=random.choice(maintainers),
                description=fake.text(max_nb_chars=200),
                status=random.choice(['active', 'inactive']),
            )
            maintainer_groups.append(group)
        self.stdout.write("Created maintainer groups.")

        # Create Maintainer Group Members
        for group in maintainer_groups:
            # Add 2 to 5 random members to each group
            members = random.sample(maintainers, k=random.randint(2, min(5, len(maintainers))))
            for member in members:
                models.MaintainerToMaintainerGroup.objects.create(
                    maintainer_group=group,
                    maintainer=member,
                )
        self.stdout.write("Created maintainer group members.")

        # Create Resource Maintainers
        for _ in range(10):
            models.ResourceMaintainer.objects.create(
                resource_type=random.choice(['vm', 'container', 'database']),
                resource_id=fake.uuid4(),
                maintainer_type=random.choice(['maintainer', 'maintainer_group']),
                maintainer_id=random.choice(maintainers).id,
            )
        self.stdout.write("Created resource maintainers.")

        # Create Racks
        racks = [
            models.Rack.objects.create(
                name=fake.word().capitalize(),
                bgp_number=str(fake.random_int(min=1000, max=9999)),
                as_number=str(fake.random_int(min=1000, max=9999)),
                old_system_id=fake.uuid4(),
            ) for _ in range(5)
        ]
        self.stdout.write("Created racks.")
        
        # Create Baremetal Groups
        host_groups = []
        for _ in range(3):
            hg = models.BaremetalGroup.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=150),
                total_cpu=random.randint(100, 1000),
                total_memory=random.randint(8192, 65536),
                total_storage=random.randint(1000, 10000),
                available_cpu=random.randint(50, 500),
                available_memory=random.randint(4096, 32768),
                available_storage=random.randint(500, 5000),
                status=random.choice(['active', 'inactive']),
            )
            host_groups.append(hg)
        self.stdout.write("Created host groups.")

        # Create Baremetals
        hosts = []
        for _ in range(10):
            host = models.Baremetal.objects.create(
                name=fake.domain_word(),
                serial_number=fake.uuid4(),
                status=random.choice(['active', 'inactive']),
                total_cpu=random.randint(4, 32),
                total_memory=random.randint(8192, 65536),
                total_storage=random.randint(100, 1000),
                available_cpu=random.randint(1, 4),
                available_memory=random.randint(1024, 8192),
                available_storage=random.randint(10, 100),
                group=random.choice(host_groups),
                region=fake.city(),
                fab=fake.word(),
                phase=fake.word(),
                dc=fake.city(),
                room=fake.word(),
                rack=random.choice(racks),
                unit=fake.word(),
                old_system_id=fake.uuid4(),
            )
            hosts.append(host)
        self.stdout.write("Created hosts.")

        # Create Tenants
        tenants = []
        for _ in range(5):
            tenant = models.Tenant.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                status=random.choice(['active', 'inactive']),
            )
            tenants.append(tenant)
        self.stdout.write("Created tenants.")

        # Create Virtual Machine Specifications
        specs = []
        for _ in range(5):
            spec = models.VirtualMachineSpecification.objects.create(
                name=fake.word().capitalize(),
                generation=fake.word(),
                required_cpu=random.randint(1, 8),
                required_memory=random.randint(1024, 16384),
                required_storage=random.randint(50, 500),
            )
            specs.append(spec)
        self.stdout.write("Created virtual machine specifications.")

        # Create K8s Clusters
        clusters = []
        for _ in range(3):
            cluster = models.K8sCluster.objects.create(
                name=fake.word().capitalize(),
                version=fake.word(),
                tenant=random.choice(tenants),
                scheduling_mode=random.choice(['spread_rack', 'balanced', 'spread_resource', 'simple']),
                description=fake.text(max_nb_chars=200),
                status=random.choice(['active', 'inactive']),
            )
            clusters.append(cluster)
        self.stdout.write("Created K8s clusters.")

        # Create Virtual Machines
        for _ in range(10):
            models.VirtualMachine.objects.create(
                name=fake.word().capitalize(),
                tenant=random.choice(tenants),
                baremetal=random.choice(hosts),
                specification=random.choice(specs),
                k8s_cluster=random.choice(clusters + [None]),  # Allow some to have no cluster
                type=random.choice(['control-plane', 'worker', 'management', 'other']),
                status=random.choice(['active', 'inactive']),
            )
        self.stdout.write("Created virtual machines.")

        # Create Baremetal Group Tenant Quotas
        for _ in range(5):
            models.BaremetalGroupTenantQuota.objects.create(
                group=random.choice(host_groups),
                tenant=random.choice(tenants),
                cpu_quota_percentage=round(random.uniform(0.1, 1.0), 2),
                memory_quota=random.randint(1024, 8192),
                storage_quota=random.randint(100, 1000),
            )
        self.stdout.write("Created host group tenant quotas.")

        # Create K8s Cluster Plugins
        for cluster in clusters:
            for _ in range(3):
                models.K8sClusterPlugin.objects.create(
                    cluster=cluster,
                    name=fake.word().capitalize(),
                    version=fake.word(),
                    status=random.choice(['active', 'inactive', 'error']),
                    additional_info=fake.json(),
                )
        self.stdout.write("Created K8s cluster plugins.")

        # Create Bastion Cluster Associations
        for _ in range(5):
            models.BastionClusterAssociation.objects.create(
                bastion=random.choice(models.VirtualMachine.objects.all()),
                k8s_cluster=random.choice(clusters),
            )
        self.stdout.write("Created bastion cluster associations.")

        # Create Service Meshes
        service_meshes = []
        for _ in range(3):
            sm = models.ServiceMesh.objects.create(
                name=fake.word().capitalize(),
                type=random.choice(['cilium', 'istio', 'other']),
                description=fake.text(max_nb_chars=200),
                status=random.choice(['active', 'inactive', 'error']),
            )
            service_meshes.append(sm)
        self.stdout.write("Created service meshes.")

        # Create K8s Cluster to Service Mesh Associations
        for cluster in clusters:
            for service_mesh in service_meshes:
                models.K8sClusterToServiceMesh.objects.create(
                    cluster=cluster,
                    service_mesh=service_mesh,
                    role=random.choice(['primary', 'secondary']),
                )
        self.stdout.write("Created K8s cluster to service mesh associations.")

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
