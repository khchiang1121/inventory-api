import uuid
from django.db import models

class Maintainer(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(blank=True, null=True)
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class MaintainerGroup(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    group_manager: models.ForeignKey = models.ForeignKey("Maintainer", on_delete=models.CASCADE, related_name="managed_groups")
    description: models.TextField = models.TextField(blank=True, null=True)
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class MaintainerGroupMember(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group: models.ForeignKey = models.ForeignKey("MaintainerGroup", on_delete=models.CASCADE, related_name="members")
    maintainer: models.ForeignKey = models.ForeignKey("Maintainer", on_delete=models.CASCADE, related_name="group_memberships")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class ResourceMaintainer(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_type: models.CharField = models.CharField(max_length=50)
    resource_id: models.UUIDField = models.UUIDField()  # Each resource uses UUID as primary key
    maintainer_type: models.CharField = models.CharField(max_length=50)  # "individual" or "group"
    maintainer_id: models.UUIDField = models.UUIDField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class HostGroup(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True, null=True)
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class Host(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    status: models.CharField = models.CharField(max_length=50)
    total_cpu: models.IntegerField = models.IntegerField()
    total_memory: models.IntegerField = models.IntegerField()
    total_storage: models.IntegerField = models.IntegerField()
    available_cpu: models.IntegerField = models.IntegerField()
    available_memory: models.IntegerField = models.IntegerField()
    available_storage: models.IntegerField = models.IntegerField()
    group: models.ForeignKey = models.ForeignKey("HostGroup", on_delete=models.CASCADE, related_name="hosts")
    region: models.CharField = models.CharField(max_length=100)
    dc: models.CharField = models.CharField(max_length=100)
    room: models.CharField = models.CharField(max_length=100)
    rack: models.CharField = models.CharField(max_length=100)
    unit: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    old_system_id: models.CharField = models.CharField(max_length=100)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class Tenant(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True, null=True)
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class VirtualMachineSpecification(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    required_cpu: models.IntegerField = models.IntegerField()
    required_memory: models.IntegerField = models.IntegerField()
    required_storage: models.IntegerField = models.IntegerField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class K8sCluster(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    tenant: models.ForeignKey = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="k8s_clusters")
    description: models.TextField = models.TextField(blank=True, null=True)
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class VirtualMachine(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    tenant: models.ForeignKey = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="virtual_machines")
    host: models.ForeignKey = models.ForeignKey("Host", on_delete=models.CASCADE, related_name="virtual_machines")
    specification: models.ForeignKey = models.ForeignKey("VirtualMachineSpecification", on_delete=models.CASCADE, related_name="virtual_machines")
    k8s_cluster: models.ForeignKey = models.ForeignKey("K8sCluster", on_delete=models.SET_NULL, blank=True, null=True, related_name="virtual_machines")
    status: models.CharField = models.CharField(max_length=50)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

class HostGroupTenantQuota(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group: models.ForeignKey = models.ForeignKey("HostGroup", on_delete=models.CASCADE, related_name="tenant_quotas")
    tenant: models.ForeignKey = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="group_quotas")
    cpu_quota_percentage: models.FloatField = models.FloatField()
    memory_quota: models.IntegerField = models.IntegerField()
    storage_quota: models.IntegerField = models.IntegerField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
