from django.db import models

from .base import AbstractBase


class BaremetalGroup(AbstractBase):
    """Baremetal server group model"""

    name = models.CharField(max_length=255, help_text="Name of the baremetal group")
    description = models.TextField(blank=True, help_text="Description of the group")
    total_cpu = models.IntegerField(help_text="Total CPU capacity")
    total_memory = models.IntegerField(help_text="Total memory capacity")
    total_storage = models.IntegerField(help_text="Total storage capacity")
    total_gpu = models.IntegerField(default=0, help_text="Total GPU capacity")
    available_cpu = models.IntegerField(help_text="Available CPU capacity")
    available_memory = models.IntegerField(help_text="Available memory capacity")
    available_storage = models.IntegerField(help_text="Available storage capacity")
    available_gpu = models.IntegerField(default=0, help_text="Available GPU capacity")
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="Group status",
    )


class Manufacturer(AbstractBase):
    """Hardware manufacturer model"""

    name = models.CharField(
        max_length=100, unique=True, help_text="Manufacturer name, e.g., Dell, HPE, etc."
    )


class Supplier(AbstractBase):
    """Supplier/vendor model"""

    name = models.CharField(max_length=100, unique=True, help_text="Supplier/vendor name")
    contact_email = models.EmailField(blank=True, help_text="Supplier contact email")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Supplier contact phone")
    address = models.TextField(blank=True, help_text="Supplier address")
    website = models.URLField(blank=True, help_text="Supplier website")


class BaremetalModel(AbstractBase):
    """Baremetal hardware model"""

    name = models.CharField(max_length=100, help_text="Model name, e.g., PowerEdge R740")
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="models",
        help_text="Server manufacturer",
    )
    suppliers = models.ManyToManyField(
        Supplier,
        related_name="models",
        blank=True,
        help_text="Hardware suppliers",
    )
    total_cpu = models.IntegerField(help_text="Total CPU capacity")
    total_memory = models.IntegerField(help_text="Total memory capacity")
    total_storage = models.IntegerField(help_text="Total storage capacity")
    total_gpu = models.IntegerField(default=0, help_text="Total GPU capacity")


class Baremetal(AbstractBase):
    """Individual baremetal server model"""

    name = models.CharField(max_length=255, help_text="Server name")
    serial_number = models.CharField(max_length=255, unique=True, help_text="Unique serial number")
    model = models.ForeignKey(BaremetalModel, on_delete=models.PROTECT, related_name="baremetals")
    fabrication = models.ForeignKey(
        "Fab", on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    phase = models.ForeignKey(
        "Phase", on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    data_center = models.ForeignKey(
        "DataCenter", on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    room = models.CharField(max_length=32, blank=True)
    rack = models.ForeignKey(
        "Rack", on_delete=models.SET_NULL, null=True, related_name="baremetals"
    )
    unit = models.ForeignKey(
        "Unit", on_delete=models.SET_NULL, null=True, blank=True, related_name="baremetals"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("pending", "Pending"),
            ("retired", "Retired"),
        ],
    )
    available_cpu = models.IntegerField()
    available_memory = models.IntegerField()
    available_storage = models.IntegerField()
    available_gpu = models.IntegerField(default=0)
    group = models.ForeignKey(BaremetalGroup, on_delete=models.CASCADE, related_name="baremetals")
    pr = models.ForeignKey(
        "PurchaseRequisition", on_delete=models.PROTECT, related_name="baremetals"
    )
    po = models.ForeignKey("PurchaseOrder", on_delete=models.PROTECT, related_name="baremetals")
    external_system_id = models.CharField(max_length=100, blank=True)


class Tenant(AbstractBase):
    """Tenant model for multi-tenancy"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )


class BaremetalGroupTenantQuota(AbstractBase):
    """Quota management for baremetal groups per tenant"""

    group = models.ForeignKey(
        BaremetalGroup, on_delete=models.CASCADE, related_name="tenant_quotas"
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="baremetal_quotas")
    cpu_quota_percentage = models.IntegerField(default=0, help_text="CPU quota for tenant")
    memory_quota = models.IntegerField(default=0, help_text="Memory quota for tenant")
    storage_quota = models.IntegerField(default=0, help_text="Storage quota for tenant")
    gpu_quota = models.IntegerField(default=0, help_text="GPU quota for tenant")

    class Meta:
        unique_together = ["group", "tenant"]
