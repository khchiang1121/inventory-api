import os
import random
from uuid import UUID
from django.core.management.base import BaseCommand
from faker import Faker
from virtflow.api import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm

class Command(BaseCommand):
    help = "Generate fake data for the Django Ninja project"

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()

        # Create Groups
        groups = []
        group_names = ['admin', 'maintainer', 'viewer', 'operator']
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups.append(group)
        self.stdout.write("Created groups.")

        # Create Users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD'),
                account=fake.user_name(),
                status=random.choice(['active', 'inactive'])
            )
            # Assign random group to each user
            user.groups.add(random.choice(groups))
            users.append(user)
        user = User.objects.create_user(
                username="user",
                email=fake.email(),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD'),
                account="user",
                status="active"
            )
        group, created = Group.objects.get_or_create(name="maintainer")
        user.groups.add(group)
        users.append(user)
        
        self.stdout.write("Created users.")

        # Define permissions for each model
        model_permissions = {
            'rack': ['add_rack', 'change_rack', 'delete_rack', 'view_rack'],
            'baremetalgroup': ['add_baremetalgroup', 'change_baremetalgroup', 'delete_baremetalgroup', 'view_baremetalgroup'],
            'baremetal': ['add_baremetal', 'change_baremetal', 'delete_baremetal', 'view_baremetal'],
            'tenant': ['add_tenant', 'change_tenant', 'delete_tenant', 'view_tenant'],
            'virtualmachinespecification': ['add_virtualmachinespecification', 'change_virtualmachinespecification', 'delete_virtualmachinespecification', 'view_virtualmachinespecification'],
            'k8scluster': ['add_k8scluster', 'change_k8scluster', 'delete_k8scluster', 'view_k8scluster'],
            'virtualmachine': ['add_virtualmachine', 'change_virtualmachine', 'delete_virtualmachine', 'view_virtualmachine'],
            'baremetalgrouptenantquota': ['add_baremetalgrouptenantquota', 'change_baremetalgrouptenantquota', 'delete_baremetalgrouptenantquota', 'view_baremetalgrouptenantquota'],
            'k8sclusterplugin': ['add_k8sclusterplugin', 'change_k8sclusterplugin', 'delete_k8sclusterplugin', 'view_k8sclusterplugin'],
            'bastionclusterassociation': ['add_bastionclusterassociation', 'change_bastionclusterassociation', 'delete_bastionclusterassociation', 'view_bastionclusterassociation'],
            'servicemesh': ['add_servicemesh', 'change_servicemesh', 'delete_servicemesh', 'view_servicemesh'],
            'k8sclustertoservicemesh': ['add_k8sclustertoservicemesh', 'change_k8sclustertoservicemesh', 'delete_k8sclustertoservicemesh', 'view_k8sclustertoservicemesh'],
        }

        # Create Racks
        racks = [
            models.Rack.objects.create(
                name=fake.word().capitalize(),
                bgp_number=str(fake.random_int(min=1000, max=9999)),
                as_number=str(fake.random_int(min=1000, max=9999)),
                old_system_id=fake.uuid4(),
            ) for _ in range(5)
        ]
        # Assign random permissions to groups and users for racks
        for rack in racks:
            for group in groups:
                assign_perm(random.choice(model_permissions['rack']), group, rack)
            for user in users:
                assign_perm(random.choice(model_permissions['rack']), user, rack)
        self.stdout.write("Created racks and assigned permissions.")
        
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
            # Assign random permissions to groups and users for host groups
            for group in groups:
                assign_perm(random.choice(model_permissions['baremetalgroup']), group, hg)
            for user in users:
                assign_perm(random.choice(model_permissions['baremetalgroup']), user, hg)
        self.stdout.write("Created host groups and assigned permissions.")

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
            # Assign random permissions to groups and users for hosts
            for group in groups:
                assign_perm(random.choice(model_permissions['baremetal']), group, host)
            for user in users:
                assign_perm(random.choice(model_permissions['baremetal']), user, host)
        self.stdout.write("Created hosts and assigned permissions.")

        # Create Tenants
        tenants = []
        for _ in range(5):
            tenant = models.Tenant.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                status=random.choice(['active', 'inactive']),
            )
            tenants.append(tenant)
            # Assign random permissions to groups and users for tenants
            for group in groups:
                assign_perm(random.choice(model_permissions['tenant']), group, tenant)
            for user in users:
                assign_perm(random.choice(model_permissions['tenant']), user, tenant)
        self.stdout.write("Created tenants and assigned permissions.")

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
            # Assign random permissions to groups and users for specs
            for group in groups:
                assign_perm(random.choice(model_permissions['virtualmachinespecification']), group, spec)
            for user in users:
                assign_perm(random.choice(model_permissions['virtualmachinespecification']), user, spec)
        self.stdout.write("Created virtual machine specifications and assigned permissions.")

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
            # Assign random permissions to groups and users for clusters
            for group in groups:
                assign_perm(random.choice(model_permissions['k8scluster']), group, cluster)
            for user in users:
                assign_perm(random.choice(model_permissions['k8scluster']), user, cluster)
        self.stdout.write("Created K8s clusters and assigned permissions.")

        # Create Virtual Machines
        vms = []
        for _ in range(10):
            vm = models.VirtualMachine.objects.create(
                name=fake.word().capitalize(),
                tenant=random.choice(tenants),
                baremetal=random.choice(hosts),
                specification=random.choice(specs),
                k8s_cluster=random.choice(clusters + [None]),  # Allow some to have no cluster
                type=random.choice(['control-plane', 'worker', 'management', 'other']),
                status=random.choice(['active', 'inactive']),
            )
            vms.append(vm)
            # Assign random permissions to groups and users for VMs
            for group in groups:
                assign_perm(random.choice(model_permissions['virtualmachine']), group, vm)
            for user in users:
                assign_perm(random.choice(model_permissions['virtualmachine']), user, vm)
        self.stdout.write("Created virtual machines and assigned permissions.")

        # Create Baremetal Group Tenant Quotas
        quotas = []
        for _ in range(5):
            quota = models.BaremetalGroupTenantQuota.objects.create(
                group=random.choice(host_groups),
                tenant=random.choice(tenants),
                cpu_quota_percentage=round(random.uniform(0.1, 1.0), 2),
                memory_quota=random.randint(1024, 8192),
                storage_quota=random.randint(100, 1000),
            )
            quotas.append(quota)
            # Assign random permissions to groups and users for quotas
            for group in groups:
                assign_perm(random.choice(model_permissions['baremetalgrouptenantquota']), group, quota)
            for user in users:
                assign_perm(random.choice(model_permissions['baremetalgrouptenantquota']), user, quota)
        self.stdout.write("Created host group tenant quotas and assigned permissions.")

        # Create K8s Cluster Plugins
        plugins = []
        for cluster in clusters:
            for _ in range(3):
                plugin = models.K8sClusterPlugin.objects.create(
                    cluster=cluster,
                    name=fake.word().capitalize(),
                    version=fake.word(),
                    status=random.choice(['active', 'inactive', 'error']),
                    additional_info=fake.json(),
                )
                plugins.append(plugin)
                # Assign random permissions to groups and users for plugins
                for group in groups:
                    assign_perm(random.choice(model_permissions['k8sclusterplugin']), group, plugin)
                for user in users:
                    assign_perm(random.choice(model_permissions['k8sclusterplugin']), user, plugin)
        self.stdout.write("Created K8s cluster plugins and assigned permissions.")

        # Create Bastion Cluster Associations
        bastion_assocs = []
        for _ in range(5):
            assoc = models.BastionClusterAssociation.objects.create(
                bastion=random.choice(vms),
                k8s_cluster=random.choice(clusters),
            )
            bastion_assocs.append(assoc)
            # Assign random permissions to groups and users for bastion associations
            for group in groups:
                assign_perm(random.choice(model_permissions['bastionclusterassociation']), group, assoc)
            for user in users:
                assign_perm(random.choice(model_permissions['bastionclusterassociation']), user, assoc)
        self.stdout.write("Created bastion cluster associations and assigned permissions.")

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
            # Assign random permissions to groups and users for service meshes
            for group in groups:
                assign_perm(random.choice(model_permissions['servicemesh']), group, sm)
            for user in users:
                assign_perm(random.choice(model_permissions['servicemesh']), user, sm)
        self.stdout.write("Created service meshes and assigned permissions.")

        # Create K8s Cluster to Service Mesh Associations
        cluster_mesh_assocs = []
        for cluster in clusters:
            for service_mesh in service_meshes:
                assoc = models.K8sClusterToServiceMesh.objects.create(
                    cluster=cluster,
                    service_mesh=service_mesh,
                    role=random.choice(['primary', 'secondary']),
                )
                cluster_mesh_assocs.append(assoc)
                # Assign random permissions to groups and users for cluster-mesh associations
                for group in groups:
                    assign_perm(random.choice(model_permissions['k8sclustertoservicemesh']), group, assoc)
                for user in users:
                    assign_perm(random.choice(model_permissions['k8sclustertoservicemesh']), user, assoc)
        self.stdout.write("Created K8s cluster to service mesh associations and assigned permissions.")

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
