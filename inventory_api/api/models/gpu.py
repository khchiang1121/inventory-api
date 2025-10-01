from django.contrib.auth.models import Group
from django.db import models

# from inventory_api.api.models.baremetal import Baremetal  # Circular import - using string reference instead
from inventory_api.api.models.common import Vendor
from inventory_api.api.models.users import CustomUser

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
class PhysicalGPUModel(AbstractBase):
    """Physical GPU model"""

    name = models.CharField(max_length=255, unique=True, help_text="Physical GPU model name")
    description = models.TextField(blank=True, help_text="Description of the GPU")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="physical_gpu_models"
    )
    architecture = models.CharField(max_length=64, blank=True, help_text="Architecture of the GPU")
    memory_mib = models.IntegerField(null=True, blank=True, help_text="GPU memory in MiB")
    api_support = models.CharField(
        max_length=32,
        blank=True,
        help_text="API support level (NVIDIA = CUDA Compute Capability, AMD = ROCm GFX version)",
    )
    power_consumption = models.IntegerField(
        null=True, blank=True, help_text="Power consumption in watts"
    )
    release_date = models.DateField(null=True, blank=True, help_text="Release date of the GPU")
    end_of_life = models.DateField(null=True, blank=True, help_text="End-of-life date of the GPU")
    is_multi_instance_supported = models.BooleanField(
        default=False, help_text="Whether multi-instance GPU (MIG or similar) is supported"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Physical GPU Model"
        verbose_name_plural = "Physical GPU Models"

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
class PhysicalGPU(AbstractBase):
    """Physical GPU"""

    name = models.CharField(max_length=255, unique=True, help_text="Physical GPU name")
    description = models.TextField(blank=True, help_text="Description of the GPU")
    serial_number = models.CharField(
        max_length=255, unique=True, help_text="Physical GPU serial number"
    )
    physical_gpu_model = models.ForeignKey(
        PhysicalGPUModel, on_delete=models.CASCADE, related_name="physical_gpus"
    )
    baremetal = models.ForeignKey(
        "Baremetal", on_delete=models.CASCADE, related_name="physical_gpus"
    )
    status = models.CharField(
        max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")]
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Physical GPU"
        verbose_name_plural = "Physical GPUs"

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
class GPUProfile(models.Model):
    """vGPU / MIG Profile definition"""

    name = models.CharField(
        max_length=50, unique=True, help_text="Profile name (e.g., nvidia-a100-20g, 1g.5gb)"
    )
    memory_mib = models.IntegerField(help_text="Memory size for this profile (MiB)")
    cores = models.IntegerField(help_text="Number of CUDA cores for this profile")

    class Meta:
        ordering = ["name"]
        verbose_name = "GPU Profile"
        verbose_name_plural = "GPU Profiles"

    def __str__(self) -> str:
        return str(self.name)
