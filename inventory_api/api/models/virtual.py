from django.db import models

from .base import AbstractBase

class Tenant(AbstractBase):
    """Tenant model for multi-tenancy"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )


class Region(AbstractBase):
    """Region model"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )


# add a phisical gpu model
class PhysicalGPUModel(AbstractBase):
    """Physical GPU model"""

    name = models.CharField(max_length=255)  # ex: NVIDIA A100
    vendor = models.CharField(max_length=64, default="NVIDIA")
    architecture = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)

    memory = models.IntegerField(help_text="GPU memory in MB")
    memory_bandwidth = models.IntegerField(null=True, blank=True, help_text="GB/s")
    cores = models.IntegerField(null=True, blank=True)
    compute_capability = models.CharField(max_length=16, blank=True)

    power_consumption = models.IntegerField(null=True, blank=True, help_text="W")
    driver_version = models.CharField(max_length=64, blank=True)
    supported_frameworks = models.JSONField(default=list, blank=True)

    release_date = models.DateField(null=True, blank=True)
    end_of_life = models.DateField(null=True, blank=True)
    is_multi_instance_supported = models.BooleanField(default=False)
    price_reference = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# add a phisical gpu class for each gpu type
class PhisicalGPU(AbstractBase):
    """Phisical GPU model"""

    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    model = models.ForeignKey("PhisicalGPUModel", on_delete=models.CASCADE, related_name="phisical_gpus")
    description = models.TextField(blank=True)
    baremetal = models.ForeignKey("Baremetal", on_delete=models.CASCADE, related_name="phisical_gpus")
    virtual_machine = models.ForeignKey("VirtualMachine", on_delete=models.CASCADE, related_name="phisical_gpus")
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )


class VirtualMachineSpecification(AbstractBase):
    """Virtual machine specification template"""

    name = models.CharField(max_length=255)
    generation = models.CharField(max_length=32)
    required_cpu = models.IntegerField()
    required_memory = models.IntegerField()
    required_storage = models.IntegerField()
    required_gpu = models.ManyToManyField("PhysicalGPUModel", through="VirtualMachineSpecificationGPU", related_name="virtual_machine_specifications")

class VirtualMachineSpecificationGPU(AbstractBase):
    """Virtual machine specification GPU model"""

    virtual_machine_specification = models.ForeignKey("VirtualMachineSpecification", on_delete=models.CASCADE, related_name="virtual_machine_specifications_gpus")
    physical_gpu_model = models.ForeignKey("PhysicalGPUModel", on_delete=models.CASCADE, related_name="virtual_machine_specifications_gpus")
    count = models.IntegerField()

class K8sCluster(AbstractBase):
    """Kubernetes cluster model"""

    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="k8s_clusters")
    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="k8s_clusters")
    # add a foreign key to the scheduling strategy
    scheduling_strategy = models.ForeignKey("SchedulingStrategy", on_delete=models.CASCADE, related_name="k8s_clusters")
    description = models.TextField(blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="k8s_clusters")
    failure_zone_cluster = models.ForeignKey("K8sCluster", on_delete=models.CASCADE, related_name="failure_zone_clusters")
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
    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="virtual_machines")
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
    routable = models.BooleanField(default=False)
    baremetal_selector = models.JSONField(blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="k8s_clusters")
    user_group = models.ManyToManyField("UserGroup", related_name="k8s_clusters")
    status = models.CharField(max_length=50)


class BastionClusterAssociation(AbstractBase):
    """Association between bastion VMs and K8s clusters"""

    bastion = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="managed_clusters"
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="bastion_machines"
    )
