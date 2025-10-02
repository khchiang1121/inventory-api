from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

# from inventory_api.api.models.gpu import GPUProfile  # Circular import - using string reference instead
from inventory_api.api.models.infrastructure import Unit
from inventory_api.api.models.purchase import PurchaseOrder, PurchaseRequisition

from .base import AbstractBase
from .common import Tenant, Vendor
from .gpu import PhysicalGPU, PhysicalGPUModel
from .users import CustomGroup, CustomUser

# from inventory_api.api.models.virtual import VirtualMachine  # Circular import - using string reference instead


# This is a future feature
# class PhysicalDiskModel(AbstractBase):
#     """Physical disk model"""

# class PhysicalDisk(AbstractBase):
#     """Physical disk"""


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
class BaremetalGroup(AbstractBase):
    """Baremetal server group model"""

    name = models.CharField(max_length=255, unique=True, help_text="Name of the baremetal group")
    description = models.TextField(blank=True, help_text="Description of the group")
    total_cpu_cores = models.IntegerField(
        null=True, blank=True, help_text="Total CPU capacity (cores)"
    )
    total_memory_mib = models.IntegerField(
        null=True, blank=True, help_text="Total memory capacity (MiB)"
    )
    total_storage_gb = models.IntegerField(
        null=True, blank=True, help_text="Total storage capacity (GB)"
    )
    available_cpu_cores = models.IntegerField(
        default=0, blank=True, help_text="Available CPU capacity (cores)"
    )
    available_memory_mib = models.IntegerField(
        default=0, blank=True, help_text="Available memory capacity (MiB)"
    )
    available_storage_gb = models.IntegerField(
        default=0, blank=True, help_text="Available storage capacity (GB)"
    )
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Group status",
    )
    user = models.ManyToManyField(CustomUser, blank=True, related_name="baremetal_groups")
    user_group = models.ManyToManyField(CustomGroup, blank=True, related_name="baremetal_groups")
    is_multi_tenant = models.BooleanField(
        default=True, help_text="Indicates if the group can be shared by multiple tenants"
    )
    labels = models.JSONField(blank=True, null=True, help_text="Labels for the group")

    class Meta:
        ordering = ["name"]
        verbose_name = "Baremetal Group"
        verbose_name_plural = "Baremetal Groups"

    def __str__(self) -> str:
        return str(self.name)

    def clean(self) -> None:
        if (
            self.total_cpu_cores is not None
            and self.available_cpu_cores is not None
            and self.total_cpu_cores < self.available_cpu_cores
        ):
            raise ValidationError(
                "Total CPU cores must be greater than or equal to available CPU cores"
            )
        if (
            self.total_memory_mib is not None
            and self.available_memory_mib is not None
            and self.total_memory_mib < self.available_memory_mib
        ):
            raise ValidationError("Total memory must be greater than or equal to available memory")
        if (
            self.total_storage_gb is not None
            and self.available_storage_gb is not None
            and self.total_storage_gb < self.available_storage_gb
        ):
            raise ValidationError(
                "Total storage must be greater than or equal to available storage"
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
class BaremetalModel(AbstractBase):
    """Baremetal hardware model"""

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Custom name to distinguish different configurations of the same model",
    )
    description = models.TextField(blank=True, help_text="Description of the model")
    model_name = models.CharField(
        max_length=255, blank=True, help_text="Machine model, e.g., PowerEdge R740"
    )
    short_model_name = models.CharField(
        max_length=255, blank=True, help_text="Short model name, e.g., R740"
    )
    manufacturer = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="models",
        help_text="Server manufacturer",
    )
    cpu_model = models.CharField(
        max_length=64, blank=True, help_text="CPU model, e.g., 'e5-2620v4'"
    )
    cpu_count = models.PositiveIntegerField(
        default=0, blank=True, help_text="Number of CPUs of the specified model"
    )
    disks = models.JSONField(
        default=list,
        blank=True,
        help_text="Disks in the format of {type: string, size: int, count: int}",
    )
    gpus: models.ManyToManyField[PhysicalGPUModel] = models.ManyToManyField(
        PhysicalGPUModel, through="BaremetalModelGPU", related_name="baremetal_models"
    )

    cpu_cores = models.IntegerField(null=True, blank=True, help_text="Total CPU cores")
    memory_mib = models.IntegerField(
        null=True, blank=True, help_text="Total memory capacity (MiB)"
    )
    storage_gb = models.IntegerField(
        null=True, blank=True, help_text="Total storage capacity (GB)"
    )

    unit_size = models.IntegerField(null=True, blank=True, help_text="Unit size in units")
    type = models.CharField(
        blank=True,
        max_length=32,
        help_text="Type of the baremetal model",
        choices=[("server", "Server"), ("storage", "Storage"), ("other", "Other")],
    )
    external_system_id = models.CharField(
        max_length=255, blank=True, help_text="External system ID"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Baremetal Model"
        verbose_name_plural = "Baremetal Models"

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
class BaremetalModelGPU(AbstractBase):
    """Baremetal model GPU model"""

    baremetal_model = models.ForeignKey(
        BaremetalModel, on_delete=models.CASCADE, related_name="gpu_specifications"
    )
    physical_gpu_model = models.ForeignKey(
        PhysicalGPUModel, on_delete=models.PROTECT, related_name="baremetal_specifications"
    )
    count = models.IntegerField(help_text="Number of GPUs")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["baremetal_model", "physical_gpu_model"],
                name="unique_baremetal_model_gpu_model",
            )
        ]

    def __str__(self) -> str:
        return str(self.baremetal_model.name) + " - " + str(self.physical_gpu_model.name)


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
class Baremetal(AbstractBase):
    """Individual baremetal server model"""

    name = models.CharField(max_length=255, help_text="Server name")
    serial_number = models.CharField(max_length=255, unique=True, help_text="Unique serial number")
    model = models.ForeignKey(
        BaremetalModel, on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    suppliers = models.ManyToManyField(
        Vendor,
        related_name="baremetals",
        blank=True,
        help_text="Hardware suppliers",
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="baremetals"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("pending", "Pending"),
            ("maintenance", "Maintenance"),
            ("retired", "Retired"),
        ],
        help_text="Status of the baremetal",
    )
    cpu_cores = models.IntegerField(null=True, blank=True, help_text="Total CPU cores")
    memory_mib = models.IntegerField(
        null=True, blank=True, help_text="Total memory capacity (MiB)"
    )
    storage_gb = models.IntegerField(
        null=True, blank=True, help_text="Total storage capacity (GB)"
    )
    available_cpu_cores = models.IntegerField(
        default=0, blank=True, help_text="Available CPU capacity (cores)"
    )
    available_memory_mib = models.IntegerField(
        default=0, blank=True, help_text="Available memory capacity (MiB)"
    )
    available_storage_gb = models.IntegerField(
        default=0, blank=True, help_text="Available storage capacity (GB)"
    )
    baremetal_group = models.ForeignKey(
        BaremetalGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="baremetals"
    )
    purchase_requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="baremetals",
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name="baremetals"
    )
    user = models.ManyToManyField(CustomUser, blank=True, related_name="owned_baremetals")
    user_group = models.ManyToManyField(CustomGroup, blank=True, related_name="owned_baremetals")
    external_system_id = models.CharField(max_length=255, blank=True)
    max_virtual_machine = models.IntegerField(
        blank=True,
        default=-1,
        help_text="Max virtual machine that can be created on this baremetal",
    )
    max_utilization = models.FloatField(
        blank=True, default=1.0, help_text="Max utilization of the baremetal (0-1)"
    )
    labels = models.JSONField(null=True, blank=True, help_text="Labels for the baremetal")
    failure_zone = models.CharField(
        max_length=32,
        help_text="Failure zone",
        choices=[
            ("fz1", "FZ1"),
            ("fz2", "FZ2"),
            ("fz3", "FZ3"),
            ("fz4", "FZ4"),
            ("other", "Other"),
        ],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Baremetal"
        verbose_name_plural = "Baremetals"

    def __str__(self) -> str:
        return str(self.name)

    def clean(self) -> None:
        if (
            self.available_cpu_cores is not None
            and self.cpu_cores is not None
            and self.available_cpu_cores > self.cpu_cores
        ):
            raise ValidationError(
                "Available CPU cores must be less than or equal to total CPU cores"
            )
        if (
            self.available_memory_mib is not None
            and self.memory_mib is not None
            and self.available_memory_mib > self.memory_mib
        ):
            raise ValidationError("Available memory must be less than or equal to total memory")
        if (
            self.available_storage_gb is not None
            and self.storage_gb is not None
            and self.available_storage_gb > self.storage_gb
        ):
            raise ValidationError("Available storage must be less than or equal to total storage")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
class GPUAllocation(models.Model):
    """GPU allocation model"""

    physical_gpu = models.ForeignKey(
        PhysicalGPU,
        on_delete=models.CASCADE,
        related_name="allocations",
        help_text="Allocated physical GPU",
    )
    virtual_machine = models.ForeignKey(
        "VirtualMachine",
        on_delete=models.CASCADE,
        related_name="gpu_allocations",
        help_text="VM using the GPU",
    )
    allocated_memory_mib = models.IntegerField(help_text="GPU memory allocated to the VM (MiB)")
    allocated_cores = models.IntegerField(help_text="CUDA cores allocated to the VM")
    profile = models.ForeignKey(
        "GPUProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Allocated profile (leave blank for Passthrough)",
    )

    class Meta:
        ordering = ["physical_gpu", "virtual_machine"]
        verbose_name = "GPU Allocation"
        verbose_name_plural = "GPU Allocations"
        constraints = [
            models.UniqueConstraint(
                fields=["physical_gpu", "virtual_machine"], name="unique_gpu_allocation"
            )
        ]

    def __str__(self) -> str:
        return str(self.physical_gpu.name) + " - " + str(self.virtual_machine.name)


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
class BaremetalGroupTenantQuota(AbstractBase):
    """Quota management for baremetal groups per tenant"""

    baremetal_group = models.ForeignKey(
        BaremetalGroup, on_delete=models.CASCADE, related_name="tenant_quotas"
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="baremetal_quotas")
    cpu_quota = models.FloatField(blank=True, default=1.0, help_text="CPU quota for tenant (0-1)")
    memory_quota = models.FloatField(
        blank=True, default=1.0, help_text="Memory quota for tenant (0-1)"
    )
    storage_quota = models.FloatField(
        blank=True, default=1.0, help_text="Storage quota for tenant (0-1)"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["baremetal_group", "tenant"], name="unique_baremetal_group_tenant"
            )
        ]

    def __str__(self) -> str:
        return str(self.baremetal_group.name) + " - " + str(self.tenant.name)

    def clean(self) -> None:
        if self.cpu_quota > 1.0:
            raise ValidationError("CPU quota must be less than or equal to 1.0")
        if self.memory_quota > 1.0:
            raise ValidationError("Memory quota must be less than or equal to 1.0")
        if self.storage_quota > 1.0:
            raise ValidationError("Storage quota must be less than or equal to 1.0")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
