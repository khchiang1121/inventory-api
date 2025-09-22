from django.db import models

from inventory_api.api.models.infrastructure import AvailableGroup

from .base import AbstractBase


class SchedulingStrategy(AbstractBase):
    """Fab model for physical infrastructure"""

    name = models.CharField(max_length=32, unique=True, help_text="Fab identifier")
    description = models.TextField(blank=True, help_text="Description of the scheduling strategy")
    mode = models.CharField(max_length=32, choices=[("spread_rack", "SpreadByRack"), ("spread_resource", "SpreadByResource"), ("balanced", "Balanced"), ("default", "Default")], default="default")
    priority = models.IntegerField(default=0)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, related_name="scheduling_strategies")


    # add a field to represent the max number of rack to spread the scheduling strategy
    max_rack_number = models.IntegerField(default=0, help_text="Indicates the max number of racks to spread the scheduling strategy")
    
    # add a field to represent if the cluster can be deploy in the same dc with it's failure zone cluster
    same_dc_in_failure_zone = models.BooleanField(default=False, help_text="Indicates if the cluster can be deploy in the same dc with it's failure zone cluster")
    # add a field to represent if the cluster can be deploy in the same phase with it's failure zone cluster
    same_phase_in_failure_zone = models.BooleanField(default=False, help_text="Indicates if the cluster can be deploy in the same phase with it's failure zone cluster")
    # add a field to represent if the cluster can be deploy in the same region with it's failure zone cluster
    same_region_in_failure_zone = models.BooleanField(default=False, help_text="Indicates if the cluster can be deploy in the same region with it's failure zone cluster")
    # add a field to represent if the cluster can be deploy in the same tenant with it's failure zone cluster
    same_tenant_in_failure_zone = models.BooleanField(default=False, help_text="Indicates if the cluster can be deploy in the same tenant with it's failure zone cluster")
    
    
    cluster_shared = models.BooleanField(default=False, help_text="Indicates if the scheduling strategy can be shared by multiple clusters")
    balance_split_rack_number = models.IntegerField(default=0, help_text="Indicates the number of racks to balance the scheduling strategy")
    status = models.CharField(max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")

    available_group = models.ManyToManyField(AvailableGroup, related_name="scheduling_strategies")



class SchedulingStrategyCondition(AbstractBase):
    """Scheduling strategy condition model"""

    scheduling_strategy = models.ForeignKey(SchedulingStrategy, on_delete=models.CASCADE, related_name="conditions")
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=32)
    operator = models.CharField(max_length=32, choices=[("eq", "Equal"), ("ne", "NotEqual"), ("gt", "GreaterThan"), ("ge", "GreaterThanOrEqual"), ("lt", "LessThan"), ("le", "LessThanOrEqual")])
    status = models.CharField(max_length=32, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
