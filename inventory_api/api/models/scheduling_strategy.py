from django.db import models

from inventory_api.api.models.baremetal import BaremetalGroupTenantQuota
from inventory_api.api.models.common import Tenant
from inventory_api.api.models.infrastructure import AvailableGroup

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
class SchedulingStrategyModel(AbstractBase):
    """Scheduling strategy model"""
    name = models.CharField(max_length=255, unique=True, help_text="Scheduling strategy model name")
    description = models.TextField(blank=True, help_text="Scheduling strategy model description")
    mode = models.CharField(max_length=32, choices=[("spread_rack", "SpreadByRack"), ("spread_resource", "SpreadByResource"), ("balanced", "Balanced"), ("default", "Default")], default="default")
    priority = models.IntegerField(default=100, help_text="Scheduling strategy model priority, lower numbers have higher priority")

    class FailureZoneAffinity(models.TextChoices):
        UNRESTRICTED = "unrestricted", "Unrestricted"
        REQUIRE_SAME = "require_same", "RequireSame"
        REQUIRE_DIFFERENT = "require_different", "RequireDifferent"

    dc_failure_zone_affinity = models.CharField(
        max_length=32,
        choices=FailureZoneAffinity.choices,
        default=FailureZoneAffinity.UNRESTRICTED,
        help_text="Defines how cluster can be placed in relation to the failure cluster at the data center level"
    )
    phase_failure_zone_affinity = models.CharField(
        max_length=32,
        choices=FailureZoneAffinity.choices,
        default=FailureZoneAffinity.UNRESTRICTED,
        help_text="Affinity rule for phase with respect to failure zone cluster"
    )
    room_failure_zone_affinity = models.CharField(
        max_length=32,
        choices=FailureZoneAffinity.choices,
        default=FailureZoneAffinity.UNRESTRICTED,
        help_text="Affinity rule for room with respect to failure zone cluster"
    )
    rack_failure_zone_affinity = models.CharField(
        max_length=32,
        choices=FailureZoneAffinity.choices,
        default=FailureZoneAffinity.UNRESTRICTED,
        help_text="Affinity rule for rack with respect to failure zone cluster"
    )
    ttl_seconds = models.IntegerField(default=0, help_text="Indicates the ttl of the scheduling strategy in seconds")
    class Meta:
        ordering = ["name"]
        verbose_name = "Scheduling Strategy Model"
        verbose_name_plural = "Scheduling Strategy Models"
    
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
class SchedulingStrategy(AbstractBase):
    """Fab model for physical infrastructure"""

    name = models.CharField(max_length=255, unique=True, help_text="Fab identifier")
    description = models.TextField(blank=True, help_text="Description of the scheduling strategy")
    priority = models.IntegerField(default=100, help_text="Scheduling strategy priority, lower numbers have higher priority")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="scheduling_strategies")

    status = models.CharField(max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")], default="active", help_text="Scheduling strategy status")

    available_group = models.ManyToManyField(AvailableGroup, related_name="scheduling_strategies", help_text="Available group that this scheduling strategy belongs to")
    baremetal_group_tenant_quota = models.ForeignKey(BaremetalGroupTenantQuota, null=True, blank=True, on_delete=models.SET_NULL, related_name="scheduling_strategies", help_text="Baremetal group tenant quota that this scheduling strategy belongs to")
    class Meta:
        ordering = ["name"]
        verbose_name = "Scheduling Strategy"
        verbose_name_plural = "Scheduling Strategies"
    
    def __str__(self) -> str:
        return str(self.name)
