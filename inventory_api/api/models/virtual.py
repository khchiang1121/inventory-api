from django.db import models

from .base import AbstractBase


class VirtualMachineSpecification(AbstractBase):
    """Virtual machine specification template"""

    name = models.CharField(max_length=255)
    generation = models.CharField(max_length=32)
    required_cpu = models.IntegerField()
    required_memory = models.IntegerField()
    required_storage = models.IntegerField()


class K8sCluster(AbstractBase):
    """Kubernetes cluster model"""

    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="k8s_clusters")
    scheduling_mode = models.CharField(
        max_length=50,
        choices=[
            ("spread_rack", "SpreadByRack"),
            ("spread_resource", "SpreadByResource"),
            ("balanced", "Balanced"),
            ("default", "Default"),
        ],
        default="default",
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)


class K8sClusterPlugin(AbstractBase):
    """Kubernetes cluster plugin model"""

    cluster = models.ForeignKey(K8sCluster, on_delete=models.CASCADE, related_name="plugins")
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
    )
    additional_info = models.JSONField(blank=True, null=True)


class ServiceMesh(AbstractBase):
    """Service mesh model"""

    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=[("cilium", "Cilium"), ("istio", "Istio"), ("other", "Other")],
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
    )


class K8sClusterToServiceMesh(AbstractBase):
    """Association between K8s clusters and service meshes"""

    cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="service_meshes"
    )
    service_mesh = models.ForeignKey(
        ServiceMesh, on_delete=models.CASCADE, related_name="clusters"
    )
    role = models.CharField(
        max_length=50, choices=[("primary", "Primary"), ("secondary", "Secondary")]
    )


class VirtualMachine(AbstractBase):
    """Virtual machine model"""

    name = models.CharField(max_length=255)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="virtual_machines")
    baremetal = models.ForeignKey(
        "Baremetal", null=True, on_delete=models.CASCADE, related_name="virtual_machines"
    )
    specification = models.ForeignKey(
        VirtualMachineSpecification,
        on_delete=models.CASCADE,
        related_name="virtual_machines",
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="virtual_machines",
    )
    type = models.CharField(
        max_length=50,
        choices=[
            ("control-plane", "K8s Control Plane"),
            ("worker", "K8s Worker"),
            ("management", "Management"),
            ("other", "Other"),
        ],
        default="other",
    )
    status = models.CharField(max_length=50)


class BastionClusterAssociation(AbstractBase):
    """Association between bastion VMs and K8s clusters"""

    bastion = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="managed_clusters"
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="bastion_machines"
    )
