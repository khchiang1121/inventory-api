from django.db import models

from .base import AbstractBase


class Fab(AbstractBase):
    """Fab model for physical infrastructure"""

    name = models.CharField(max_length=32, unique=True, help_text="Fab identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )


class Phase(AbstractBase):
    """Phase model for deployment phases"""

    name = models.CharField(max_length=32, unique=True, help_text="Phase identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    fab = models.ForeignKey(
        "Fab",
        on_delete=models.CASCADE,
        related_name="phases",
        help_text="Fab that this phase belongs to",
        null=True,
        blank=True,
    )


class DataCenter(AbstractBase):
    """Data center model"""

    name = models.CharField(max_length=32, unique=True, help_text="Data center identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
        related_name="datacenters",
        help_text="Phase that this datacenter belongs to",
        null=True,
        blank=True,
    )


class Room(AbstractBase):
    """Room model within data centers"""

    name = models.CharField(max_length=32, unique=True, help_text="Room identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    datacenter = models.ForeignKey(
        DataCenter,
        on_delete=models.CASCADE,
        related_name="rooms",
        help_text="Datacenter that this room belongs to",
        null=True,
        blank=True,
    )


class Rack(AbstractBase):
    """Rack model for physical server racks"""

    name = models.CharField(max_length=32, unique=True, help_text="Rack identifier")
    bgp_number = models.CharField(max_length=20, unique=True, help_text="Associated BGP number")
    as_number = models.PositiveIntegerField(help_text="Autonomous System Number")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="racks",
        help_text="Room that this rack belongs to",
        null=True,
        blank=True,
    )
    height_units = models.PositiveIntegerField(
        default=42, help_text="Total height units in the rack"
    )
    used_units = models.PositiveIntegerField(
        default=0, help_text="Number of units currently in use"
    )
    available_units = models.PositiveIntegerField(
        default=42, help_text="Number of units available"
    )
    power_capacity = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Power capacity in kW"
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("maintenance", "Maintenance"),
            ("full", "Full"),
        ],
        default="active",
        help_text="Rack status",
    )


class Unit(AbstractBase):
    """Individual rack unit position (e.g., U1..U42) within a rack."""

    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name="units",
        help_text="Rack that this unit belongs to",
    )
    name = models.CharField(
        max_length=32,
        help_text="Unit label within the rack, e.g., U1, U2",
    )

    class Meta:
        unique_together = ["rack", "name"]
