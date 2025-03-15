import random
import uuid
from faker import Faker
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "virtflow.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from backend import models

fake = Faker()

def create_maintainer():
    return models.Maintainer.objects.create(
        name=fake.name(),
        account=fake.user_name(),
        email=fake.email(),
        status=random.choice(['active', 'inactive'])
    )

def create_maintainer_group(manager):
    return models.MaintainerGroup.objects.create(
        name=fake.company(),
        group_manager=manager,
        description=fake.text(),
        status=random.choice(['active', 'inactive'])
    )

def create_maintainer_to_maintainer_group(group, maintainer):
    return models.MaintainerToMaintainerGroup.objects.create(
        maintainer_group=group,
        maintainer=maintainer
    )

def create_resource_maintainer(resource_type, resource_id, maintainer_type, maintainer_id):
    return models.ResourceMaintainer.objects.create(
        resource_type=resource_type,
        resource_id=resource_id,
        maintainer_type=maintainer_type,
        maintainer_id=maintainer_id
    )

def create_rack():
    return models.Rack.objects.create(
        name=fake.bothify(text='Rack-##'),
        bgp_number=fake.bothify(text='BGP-####'),
        as_number=fake.bothify(text='AS-####'),
        old_system_id=fake.uuid4()
    )

def create_baremetal_group():
    return models.BaremetalGroup.objects.create(
        name=fake.company(),
        description=fake.text(),
        total_cpu=random.randint(16, 64),
        total_memory=random.randint(32768, 131072),
        total_storage=random.randint(1024, 4096),
        available_cpu=random.randint(8, 32),
        available_memory=random.randint(16384, 65536),
        available_storage=random.randint(512, 2048),
        status=random.choice(['active', 'inactive'])
    )

def create_baremetal(rack, group):
    return models.Baremetal.objects.create(
        name=fake.hostname(),
        serial_number=fake.uuid4(),
        region=fake.state(),
        fab=fake.word(),
        phase=fake.word(),
        dc=fake.city(),
        room=fake.bothify(text='Room-###'),
        rack=rack,
        unit=fake.bothify(text='Unit-##'),
        status=random.choice(['active', 'inactive']),
        total_cpu=random.randint(16, 64),
        total_memory=random.randint(32768, 131072),
        total_storage=random.randint(1024, 4096),
        available_cpu=random.randint(8, 32),
        available_memory=random.randint(16384, 65536),
        available_storage=random.randint(512, 2048),
        group=group,
        old_system_id=fake.uuid4()
    )

def create_baremetal_group_tenant_quota(group, tenant):
    return models.BaremetalGroupTenantQuota.objects.create(
        group=group,
        tenant=tenant,
        cpu_quota_percentage=random.uniform(10.0, 90.0),
        memory_quota=random.randint(16384, 65536),
        storage_quota=random.randint(512, 2048)
    )

def create_tenant():
    return models.Tenant.objects.create(
        name=fake.company(),
        description=fake.text(),
        status=random.choice(['active', 'inactive'])
    )

def create_virtual_machine_specification():
    return models.VirtualMachineSpecification.objects.create(
        name=fake.word(),
        generation=fake.word(),
        required_cpu=random.randint(2, 16),
        required_memory=random.randint(2048, 16384),
        required_storage=random.randint(50, 500)
    )

def create_k8s_cluster(tenant):
    return models.K8sCluster.objects.create(
        name=fake.word(),
        version=fake.word(),
        tenant=tenant,
        description=fake.text(),
        status=random.choice(['active', 'inactive'])
    )

def create_k8s_cluster_plugin(cluster):
    return models.K8sClusterPlugin.objects.create(
        cluster=cluster,
        name=fake.word(),
        version=fake.word(),
        status=random.choice(['active', 'inactive', 'error']),
        additional_info={"info": fake.text()}
    )

def create_bastion_cluster_association(bastion, k8s_cluster):
    return models.BastionClusterAssociation.objects.create(
        bastion=bastion,
        k8s_cluster=k8s_cluster
    )

def create_k8s_cluster_to_service_mesh(cluster, service_mesh):
    return models.K8sClusterToServiceMesh.objects.create(
        cluster=cluster,
        service_mesh=service_mesh,
        role=random.choice(['primary', 'secondary'])
    )

def create_service_mesh():
    return models.ServiceMesh.objects.create(
        name=fake.word(),
        type=random.choice(['cilium', 'istio', 'other']),
        description=fake.text(),
        status=random.choice(['active', 'inactive', 'error'])
    )

def create_virtual_machine(tenant, baremetal, specification, k8s_cluster=None):
    return models.VirtualMachine.objects.create(
        name=fake.hostname(),
        tenant=tenant,
        baremetal=baremetal,
        specification=specification,
        k8s_cluster=k8s_cluster,
        type=random.choice(['control-plane', 'worker', 'management', 'other']),
        status=random.choice(['active', 'inactive'])
    )

# Example usage
if __name__ == "__main__":
    maintainer = create_maintainer()
    maintainer_group = create_maintainer_group(maintainer)
    create_maintainer_to_maintainer_group(maintainer_group, maintainer)
    rack = create_rack()
    baremetal_group = create_baremetal_group()
    baremetal = create_baremetal(rack, baremetal_group)
    tenant = create_tenant()
    create_baremetal_group_tenant_quota(baremetal_group, tenant)
    vm_spec = create_virtual_machine_specification()
    k8s_cluster = create_k8s_cluster(tenant)
    create_k8s_cluster_plugin(k8s_cluster)
    service_mesh = create_service_mesh()
    create_k8s_cluster_to_service_mesh(k8s_cluster, service_mesh)
    vm = create_virtual_machine(tenant, baremetal, vm_spec, k8s_cluster)
    create_bastion_cluster_association(vm, k8s_cluster)
