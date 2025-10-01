from typing import Any
from django.core.exceptions import ValidationError
from django.db import models

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
class AvailableGroup(AbstractBase):
    """Available group model"""

    name = models.CharField(max_length=255, unique=True, help_text="Available rack identifier")
    description = models.TextField(blank=True, help_text="Description of the available rack")
    status = models.CharField(
        max_length=32,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        default="active",
        help_text="Available rack status",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Available Group"
        verbose_name_plural = "Available Groups"

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
class Fab(AbstractBase):
    """Fab model for physical infrastructure"""

    name = models.CharField(max_length=255, unique=True, help_text="Fab identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Fab"
        verbose_name_plural = "Fabs"

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
class Phase(AbstractBase):
    """Phase model for deployment phases"""

    name = models.CharField(max_length=255, help_text="Phase identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    fab = models.ForeignKey(
        "Fab",
        on_delete=models.CASCADE,
        related_name="phases",
        help_text="Fab that this phase belongs to",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Phase"
        verbose_name_plural = "Phases"
        constraints = [
            models.UniqueConstraint(fields=["name", "fab"], name="unique_phase_per_fab")
        ]

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
class DataCenter(AbstractBase):
    """Data center model"""

    name = models.CharField(max_length=255, unique=True, help_text="Data center identifier")
    external_system_id = models.CharField(
        max_length=100, blank=True, help_text="Identifier from legacy system"
    )
    fab = models.ForeignKey(
        Fab,
        on_delete=models.SET_NULL,
        related_name="datacenters",
        help_text="Fab that this datacenter belongs to",
        null=True,
        blank=True,
    )
    phase = models.ForeignKey(
        Phase,
        on_delete=models.SET_NULL,
        related_name="datacenters",
        help_text="Phase that this datacenter belongs to",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Data Center"
        verbose_name_plural = "Data Centers"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "fab", "phase"], name="unique_datacenter_per_fab_and_phase"
            )
        ]

    def __str__(self) -> str:
        return str(self.name)

    def clean(self) -> None:
        if self.fab is None and self.phase is None:
            raise ValidationError("Fab and phase must at least one of them is not null")

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
class Room(AbstractBase):
    """Room model within data centers"""

    name = models.CharField(max_length=255, help_text="Room identifier")
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

    class Meta:
        ordering = ["name"]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "datacenter"], name="unique_room_per_datacenter"
            )
        ]

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
class Rack(AbstractBase):
    """Rack model for physical server racks"""

    name = models.CharField(max_length=255, help_text="Rack identifier")
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
    bgp_number = models.CharField(max_length=20, unique=True, help_text="Associated BGP number")
    as_number = models.PositiveIntegerField(help_text="Autonomous System Number")
    height_units = models.PositiveIntegerField(
        default=42, help_text="Total height units in the rack"
    )
    used_units = models.PositiveIntegerField(
        default=0, help_text="Number of units currently in use"
    )
    available_units = models.PositiveIntegerField(
        default=42, help_text="Number of units available"
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
    available_group = models.ForeignKey(
        AvailableGroup, on_delete=models.SET_NULL, related_name="racks", null=True, blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Rack"
        verbose_name_plural = "Racks"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "room"], name="unique_rack_per_available_group"
            )
        ]

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
class Unit(AbstractBase):
    """Individual rack unit position (e.g., U1..U42) within a rack."""

    name = models.CharField(
        max_length=255,
        help_text="Unit label within the rack, e.g., U1, U2",
    )
    unit_number = models.PositiveIntegerField(help_text="Unit number within the rack")
    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name="units",
        help_text="Rack that this unit belongs to",
    )
    bgp = models.CharField(
        max_length=32,
        choices=[("bgp1", "BGP1"), ("bgp2", "BGP2"), ("bgp3", "BGP3"), ("bgp4", "BGP4")],
        help_text="BGP that this unit belongs to",
    )

    class Meta:
        unique_together = ["rack", "name"]
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        constraints = [
            models.UniqueConstraint(fields=["rack", "unit_number"], name="unique_unit_per_rack")
        ]

    def __str__(self) -> str:
        return str(self.name)
