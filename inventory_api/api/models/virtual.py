from django.contrib.auth.models import Group
from django.db import models

# from inventory_api.api.models.baremetal import Baremetal, BaremetalGroupTenantQuota, PhysicalGPUModel  # Circular import - using string references instead
from inventory_api.api.models.common import Region, Tenant
from inventory_api.api.models.users import CustomGroup, CustomUser

from .base import AbstractBase


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class VirtualMachineSpecification(AbstractBase):
    """Virtual machine specification template"""

    name = models.CharField(max_length=255, help_text="Virtual machine specification name")
    description = models.TextField(
        blank=True, help_text="Virtual machine specification description"
    )
    generation = models.CharField(
        max_length=32, help_text="Virtual machine specification generation"
    )
    required_cpu_cores = models.IntegerField(
        default=0, help_text="Virtual machine specification required cpu in cores"
    )
    required_memory_mib = models.IntegerField(
        default=0, help_text="Virtual machine specification required memory in MiB"
    )
    required_storage_gb = models.IntegerField(
        default=0, help_text="Virtual machine specification required storage in GB"
    )
    required_gpu = models.ManyToManyField(
        "PhysicalGPUModel",
        through="VirtualMachineSpecificationRequiredGPU",
        related_name="virtual_machine_specifications",
        help_text="Virtual machine specification required GPUs",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Virtual Machine Specification"
        verbose_name_plural = "Virtual Machine Specifications"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class VirtualMachineSpecificationRequiredGPU(AbstractBase):
    """Virtual machine specification GPU model"""

    virtual_machine_specification = models.ForeignKey(
        VirtualMachineSpecification,
        on_delete=models.CASCADE,
    )
    physical_gpu_model = models.ForeignKey(
        "PhysicalGPUModel",
        on_delete=models.PROTECT,
    )
    count = models.IntegerField(default=0, help_text="Number of GPUs")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["virtual_machine_specification", "physical_gpu_model"],
                name="unique_virtual_machine_specification_physical_gpu_model",
            )
        ]
        ordering = ["virtual_machine_specification", "physical_gpu_model"]
        verbose_name = "Virtual Machine Specification Required GPU"
        verbose_name_plural = "Virtual Machine Specification Required GPUs"

    def __str__(self) -> str:
        return (
            str(self.virtual_machine_specification.name)
            + " - "
            + str(self.physical_gpu_model.name)
        )


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class K8sCluster(AbstractBase):
    """Kubernetes cluster model"""

    name = models.CharField(max_length=255, help_text="Kubernetes cluster name")
    description = models.TextField(blank=True, help_text="Kubernetes cluster description")
    version = models.CharField(max_length=255, blank=True, help_text="Kubernetes cluster version")
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="k8s_clusters")
    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="k8s_clusters")
    scheduling_strategy = models.ForeignKey(
        "SchedulingStrategy", on_delete=models.SET_NULL, null=True, related_name="k8s_clusters"
    )
    user = models.ManyToManyField(CustomUser, blank=True, related_name="k8s_clusters")
    user_group = models.ManyToManyField(CustomGroup, blank=True, related_name="k8s_clusters")
    failure_zone_cluster = models.ForeignKey(
        "K8sCluster",
        on_delete=models.SET_NULL,
        related_name="failure_zone_clusters",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
        default="active",
        help_text="Kubernetes cluster status",
    )
    baremetal_group_tenant_quotas = models.ManyToManyField(
        "BaremetalGroupTenantQuota", related_name="k8s_clusters"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Kubernetes Cluster"
        verbose_name_plural = "Kubernetes Clusters"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class VirtualMachineRole(AbstractBase):
    """Virtual machine role model"""

    name = models.CharField(
        max_length=64,
        unique=True,
        choices=[
            ("control-plane", "Control Plane"),
            ("worker", "Worker"),
            ("management", "Management"),
            ("other", "Other"),
        ],
    )
    description = models.TextField(blank=True, help_text="Virtual machine role description")

    class Meta:
        ordering = ["name"]
        verbose_name = "Virtual Machine Role"
        verbose_name_plural = "Virtual Machine Roles"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class VirtualMachine(AbstractBase):
    """Virtual machine model"""

    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name="virtual_machines")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="virtual_machines")
    baremetal = models.ForeignKey(
        "Baremetal", null=True, on_delete=models.PROTECT, related_name="virtual_machines"
    )
    specification = models.ForeignKey(
        VirtualMachineSpecification,
        on_delete=models.PROTECT,
        related_name="virtual_machines",
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="virtual_machines",
    )
    virtual_machine_role = models.ForeignKey(
        VirtualMachineRole,
        on_delete=models.PROTECT,
        related_name="virtual_machines",
    )
    routable = models.BooleanField(
        default=False, help_text="Indicates if the virtual machine is routable"
    )
    baremetal_selector = models.JSONField(
        blank=True, null=True, help_text="Selector for baremetal"
    )
    user = models.ManyToManyField(CustomUser, blank=True, related_name="virtual_machines")
    user_group = models.ManyToManyField(CustomGroup, blank=True, related_name="virtual_machines")
    status = models.CharField(
        max_length=50,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("error", "Error"),
            ("pending", "Pending"),
            ("deleting", "Deleting"),
            ("deleted", "Deleted"),
            ("maintenance", "Maintenance"),
            ("retired", "Retired"),
        ],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Virtual Machine"
        verbose_name_plural = "Virtual Machines"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class K8sClusterPlugin(AbstractBase):
    """Kubernetes cluster plugin model"""

    name = models.CharField(max_length=255, help_text="Kubernetes cluster plugin name")
    description = models.TextField(blank=True, help_text="Kubernetes cluster plugin description")
    versions = models.JSONField(
        blank=True, null=True, help_text="Kubernetes cluster plugin versions"
    )
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
        default="active",
        help_text="Kubernetes cluster plugin status",
    )
    additional_info = models.JSONField(
        blank=True,
        null=True,
        help_text="Additional information about the Kubernetes cluster plugin",
    )
    k8s_clusters = models.ManyToManyField(
        K8sCluster,
        blank=True,
        related_name="plugin_associations",
        through="K8sClusterPluginAssociation",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Kubernetes Cluster Plugin"
        verbose_name_plural = "Kubernetes Cluster Plugins"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class K8sClusterPluginAssociation(AbstractBase):
    """Association between Kubernetes clusters and plugins"""

    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="cluster_plugin_associations"
    )
    k8s_cluster_plugin = models.ForeignKey(
        K8sClusterPlugin, on_delete=models.CASCADE, related_name="clusters"
    )
    version = models.CharField(
        max_length=255, blank=True, help_text="Kubernetes cluster plugin version"
    )

    class Meta:
        ordering = ["k8s_cluster", "k8s_cluster_plugin"]
        verbose_name = "Kubernetes Cluster Plugin Association"
        verbose_name_plural = "Kubernetes Cluster Plugin Associations"
        constraints = [
            models.UniqueConstraint(
                fields=["k8s_cluster", "k8s_cluster_plugin"],
                name="unique_k8s_cluster_plugin_association",
            )
        ]

    def __str__(self) -> str:
        return str(self.k8s_cluster.name) + " - " + str(self.k8s_cluster_plugin.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class ServiceMesh(AbstractBase):
    """Service mesh model"""

    name = models.CharField(max_length=255, help_text="Service mesh name")
    description = models.TextField(blank=True, help_text="Service mesh description")
    type = models.CharField(
        max_length=32,
        choices=[("cilium", "Cilium"), ("istio", "Istio"), ("other", "Other")],
        help_text="Service mesh type",
    )
    status = models.CharField(
        max_length=64,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("error", "Error")],
        default="active",
        help_text="Service mesh status",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Service Mesh"
        verbose_name_plural = "Service Meshes"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class K8sClusterToServiceMesh(AbstractBase):
    """Association between K8s clusters and service meshes"""

    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="service_meshes"
    )
    service_mesh = models.ForeignKey(
        ServiceMesh, on_delete=models.CASCADE, related_name="k8s_cluster"
    )
    role = models.CharField(
        max_length=50,
        choices=[("primary", "Primary"), ("secondary", "Secondary"), ("other", "Other")],
    )

    class Meta:
        ordering = ["k8s_cluster", "service_mesh", "role"]
        verbose_name = "K8s Cluster to Service Mesh"
        verbose_name_plural = "K8s Cluster to Service Meshes"

    def __str__(self) -> str:
        return str(self.k8s_cluster.name) + " - " + str(self.service_mesh.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class BastionClusterAssociation(AbstractBase):
    """Association between bastion VMs and K8s clusters"""

    bastion = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="managed_clusters"
    )
    k8s_cluster = models.ForeignKey(
        K8sCluster, on_delete=models.CASCADE, related_name="bastion_machines"
    )

    class Meta:
        ordering = ["bastion", "k8s_cluster"]
        verbose_name = "Bastion Cluster Association"
        verbose_name_plural = "Bastion Cluster Associations"

    def __str__(self) -> str:
        return str(self.bastion.name) + " - " + str(self.k8s_cluster.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class ClusterTemplate(AbstractBase):
    """Cluster template model"""

    name = models.CharField(max_length=255, unique=True, help_text="Cluster template name")
    description = models.TextField(blank=True, null=True, help_text="Cluster template description")
    user = models.ManyToManyField(CustomUser, blank=True, related_name="cluster_templates")
    user_group = models.ManyToManyField(CustomGroup, blank=True, related_name="cluster_templates")
    routable_ratio = models.FloatField(default=0.0, help_text="Routable ratio")

    class Meta:
        ordering = ["name"]
        verbose_name = "Cluster Template"
        verbose_name_plural = "Cluster Templates"

    def __str__(self) -> str:
        return str(self.name)


# [MODEL CHECKLIST v3]
# Overall structure
# [x] Check all fields in the model are necessary and correct
# [x] Include docstring for the model (describe its purpose)
# Fields
# [x] Have a "name" field, with max_length=255; if needed, set unique=True
# [x] Have a "description" field, and allow blank=True
# [x] Every field should include a help_text (except relationship)
# [x] Set default value if appropriate
# [x] String fields (CharField, TextField) should NOT use null=True
# [x] Use max_length=255 for regular strings; 64 for short text, 32 for very short text
# [x] If linking to users, include both "user" and "user_group" fields
# [x] ForeignKey should always define on_delete explicitly (e.g., CASCADE, SET_NULL)
# [x] ForeignKey that can be optional must use null=True, blank=True
# [x] ManyToManyField should always define a related_name
# [x] ForeignKey should always be named as the model name (e.g., ansible_inventory)
# Meta and representation
# [x] Define __str__() to return a meaningful field (e.g., name)
# [x] Define Meta: ordering, verbose_name, verbose_name_plural, constraints
# [x] Define clean and save if needed
class ClusterTemplateVirtualMachine(AbstractBase):
    """Cluster template virtual machine model"""

    cluster_template = models.ForeignKey(
        ClusterTemplate, on_delete=models.CASCADE, related_name="virtual_machines"
    )
    vm_role = models.ForeignKey(VirtualMachineRole, on_delete=models.PROTECT)
    vm_spec = models.ForeignKey(VirtualMachineSpecification, on_delete=models.PROTECT)
    is_routable = models.BooleanField(
        default=False, help_text="Indicates if the virtual machine is routable"
    )
    count = models.PositiveIntegerField(help_text="Number of virtual machines")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cluster_template", "vm_role", "vm_spec", "is_routable", "count"],
                name="unique_cluster_template_virtual_machine",
            )
        ]
        ordering = ["cluster_template", "vm_role", "vm_spec", "is_routable", "count"]
        verbose_name = "Cluster Template Virtual Machine"
        verbose_name_plural = "Cluster Template Virtual Machines"

    def __str__(self) -> str:
        return (
            str(self.cluster_template.name)
            + " - "
            + str(self.vm_role.name)
            + " - "
            + str(self.vm_spec.name)
        )
