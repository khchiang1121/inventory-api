import uuid
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.mixins import GuardianUserMixin  # type: ignore

class AbstractBase(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 告訴 Django 這是抽象類別，不會建資料表

# ------------------------------------------------------------------------------
# User Models
# ------------------------------------------------------------------------------
class CustomUser(GuardianUserMixin, AbstractUser):
    account: models.CharField = models.CharField(max_length=32, unique=True, null=True, blank=True, help_text="Unique account identifier")
    status: models.CharField = models.CharField(max_length=32,choices=[('active', 'Active'), ('inactive', 'Inactive')],help_text="Account status")
# ------------------------------------------------------------------------------
# Physical Infrastructure Models
# ------------------------------------------------------------------------------
class Rack(AbstractBase):
    """
    Represents a physical rack in a data center.
    """
    name: models.CharField = models.CharField(max_length=20, unique=True, help_text="Rack identifier")
    bgp_number: models.CharField = models.CharField(max_length=20, unique=True, help_text="Associated BGP number")
    as_number: models.CharField = models.CharField(max_length=20, unique=True, help_text="Associated AS number")
    old_system_id: models.CharField = models.CharField(max_length=100,blank=True,help_text="Identifier from legacy system")


class BaremetalGroup(AbstractBase):
    """
    Grouping for baremetal servers.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Name of the baremetal group")
    description: models.TextField= models.TextField(blank=True, help_text="Description of the group")
    total_cpu: models.IntegerField= models.IntegerField(help_text="Total CPU capacity")
    total_memory: models.IntegerField= models.IntegerField(help_text="Total memory capacity")
    total_storage: models.IntegerField= models.IntegerField(help_text="Total storage capacity")
    available_cpu: models.IntegerField= models.IntegerField(help_text="Available CPU capacity")
    available_memory: models.IntegerField= models.IntegerField(help_text="Available memory capacity")
    available_storage: models.IntegerField= models.IntegerField(help_text="Available storage capacity")
    status: models.CharField = models.CharField(max_length=32,choices=[('active', 'Active'), ('inactive', 'Inactive')],help_text="Group status")


class Baremetal(AbstractBase):
    """
    Represents a baremetal server.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Server name")
    serial_number: models.CharField = models.CharField(max_length=255, unique=True, help_text="Unique serial number")
    region: models.CharField = models.CharField(max_length=32, blank=True, help_text="Geographical region")
    fab: models.CharField = models.CharField(max_length=32, blank=True, help_text="Fabrication details")
    phase: models.CharField = models.CharField(max_length=32, blank=True, help_text="Deployment phase")
    dc: models.CharField = models.CharField(max_length=32, blank=True, help_text="Data center identifier")
    room: models.CharField = models.CharField(max_length=32, blank=True, help_text="Room identifier")
    rack: models.ForeignKey = models.ForeignKey("Rack",on_delete=models.SET_NULL,null=True,related_name="baremetals",help_text="Associated rack")
    unit: models.CharField = models.CharField(max_length=32, blank=True, help_text="Unit identifier within the rack")
    status: models.CharField = models.CharField(max_length=32,choices=[('active', 'Active'), ('inactive', 'Inactive')],help_text="Server status")
    total_cpu: models.IntegerField= models.IntegerField(help_text="Total CPU capacity")
    total_memory: models.IntegerField= models.IntegerField(help_text="Total memory capacity")
    total_storage: models.IntegerField= models.IntegerField(help_text="Total storage capacity")
    available_cpu: models.IntegerField= models.IntegerField(help_text="Available CPU capacity")
    available_memory: models.IntegerField= models.IntegerField(help_text="Available memory capacity")
    available_storage: models.IntegerField= models.IntegerField(help_text="Available storage capacity")
    group: models.ForeignKey = models.ForeignKey("BaremetalGroup",on_delete=models.CASCADE,related_name="baremetals",help_text="Baremetal group")
    old_system_id: models.CharField = models.CharField(max_length=100,blank=True,help_text="Identifier from legacy system")


class BaremetalGroupTenantQuota(AbstractBase):
    """
    Quota assigned to a tenant for a specific baremetal group.
    """
    group: models.ForeignKey = models.ForeignKey("BaremetalGroup",on_delete=models.CASCADE,related_name="tenant_quotas",help_text="Associated baremetal group")
    tenant: models.ForeignKey = models.ForeignKey("Tenant",on_delete=models.CASCADE,related_name="group_quotas",help_text="Associated tenant")
    cpu_quota_percentage: models.FloatField= models.FloatField(help_text="CPU quota percentage allocated")
    memory_quota: models.IntegerField= models.IntegerField(help_text="Memory quota allocated")
    storage_quota: models.IntegerField= models.IntegerField(help_text="Storage quota allocated")


# ------------------------------------------------------------------------------
# Virtual Resources and Cloud Models
# ------------------------------------------------------------------------------
class Tenant(AbstractBase):
    """
    Represents a tenant in the system.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Tenant name")
    description: models.TextField= models.TextField(blank=True, help_text="Description of the tenant")
    status: models.CharField = models.CharField(max_length=32,choices=[('active', 'Active'), ('inactive', 'Inactive')],help_text="Tenant status")


class VirtualMachineSpecification(AbstractBase):
    """
    Specification template for virtual machines.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Specification name")
    generation: models.CharField = models.CharField(max_length=32, help_text="Generation or version")
    required_cpu: models.IntegerField= models.IntegerField(help_text="Required CPU capacity")
    required_memory: models.IntegerField= models.IntegerField(help_text="Required memory capacity")
    required_storage: models.IntegerField= models.IntegerField(help_text="Required storage capacity")


class K8sCluster(AbstractBase):
    """
    Represents a Kubernetes cluster.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Cluster name")
    version: models.CharField = models.CharField(max_length=255, help_text="Kubernetes version")
    tenant: models.ForeignKey = models.ForeignKey("Tenant",on_delete=models.CASCADE,related_name="k8s_clusters",help_text="Tenant that owns the cluster")
    scheduling_mode:models.CharField = models.CharField(max_length=50, choices=[("spread_rack", "SpreadByRack"), ("spread_resource", "SpreadByResource"), ("balanced", "Balanced"), ("default", "Default")], default="default", help_text="VM scheduling strategy for this cluster")
    description: models.TextField= models.TextField(blank=True, help_text="Cluster description")
    status: models.CharField = models.CharField(max_length=50, help_text="Cluster status")


class K8sClusterPlugin(AbstractBase):
    """
    Plugins installed on a Kubernetes cluster.
    """
    cluster: models.ForeignKey = models.ForeignKey("K8sCluster",on_delete=models.CASCADE,related_name="plugins",help_text="Associated cluster")
    name: models.CharField = models.CharField(max_length=255, help_text="Plugin name")
    version: models.CharField = models.CharField(max_length=255, help_text="Plugin version")
    status: models.CharField = models.CharField(max_length=64,choices=[('active', 'Active'), ('inactive', 'Inactive'), ('error', 'Error')],help_text="Plugin status")
    additional_info = models.JSONField(blank=True,null=True,help_text="Additional plugin information")


class BastionClusterAssociation(AbstractBase):
    """
    Association between a bastion virtual machine and a Kubernetes cluster.
    """
    bastion: models.ForeignKey = models.ForeignKey("VirtualMachine",on_delete=models.CASCADE,related_name="managed_clusters",help_text="Bastion VM")
    k8s_cluster: models.ForeignKey = models.ForeignKey("K8sCluster",on_delete=models.CASCADE,related_name="bastion_machines",help_text="Associated Kubernetes cluster")


class K8sClusterToServiceMesh(AbstractBase):
    """
    Association between a Kubernetes cluster and a service mesh.
    """
    cluster: models.ForeignKey = models.ForeignKey("K8sCluster",on_delete=models.CASCADE,related_name="service_meshes",help_text="Associated cluster")
    service_mesh: models.ForeignKey = models.ForeignKey("ServiceMesh",on_delete=models.CASCADE,related_name="clusters",help_text="Associated service mesh")
    role: models.CharField = models.CharField(max_length=50,choices=[('primary', 'Primary'), ('secondary', 'Secondary')],help_text="Role of the service mesh in the cluster")


class ServiceMesh(AbstractBase):
    """
    Represents a service mesh.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="Service mesh name")
    type: models.CharField = models.CharField(max_length=50,choices=[('cilium', 'Cilium'), ('istio', 'Istio'), ('other', 'Other')],help_text="Type of service mesh")
    description: models.TextField= models.TextField(blank=True, help_text="Description of the service mesh")
    status: models.CharField = models.CharField(max_length=64,choices=[('active', 'Active'), ('inactive', 'Inactive'), ('error', 'Error')],help_text="Service mesh status")


class VirtualMachine(AbstractBase):
    """
    Represents a virtual machine.
    """
    name: models.CharField = models.CharField(max_length=255, help_text="VM name")
    tenant: models.ForeignKey = models.ForeignKey("Tenant",on_delete=models.CASCADE,related_name="virtual_machines",help_text="Owning tenant")
    baremetal: models.ForeignKey = models.ForeignKey("Baremetal", null=True,on_delete=models.CASCADE,related_name="virtual_machines",help_text="Host baremetal server")
    specification: models.ForeignKey = models.ForeignKey("VirtualMachineSpecification",on_delete=models.CASCADE,related_name="virtual_machines",help_text="VM specification template")
    k8s_cluster: models.ForeignKey = models.ForeignKey("K8sCluster",on_delete=models.SET_NULL,blank=True,null=True,related_name="virtual_machines",help_text="Associated Kubernetes cluster (if any)")
    type: models.CharField = models.CharField(max_length=50,choices= [('control-plane', 'K8s Control Plane'),('worker', 'K8s Worker'),('management', 'Management'), ('other', "Other")], default='other',help_text="Type of virtual machine")
    status: models.CharField = models.CharField(max_length=50, help_text="VM status")

