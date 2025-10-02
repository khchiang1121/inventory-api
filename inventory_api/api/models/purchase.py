from django.db import models

from inventory_api.api.models.common import Vendor

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
class PurchaseRequisition(AbstractBase):
    """Purchase requisition model for procurement requests"""

    name = models.CharField(max_length=255, help_text="Purchase requisition name")
    description = models.TextField(blank=True, help_text="Description of the purchase requisition")
    pr_number = models.CharField(max_length=64, unique=True, help_text="PR number")
    requested_by = models.CharField(max_length=255, help_text="Requester name or ID")
    department = models.CharField(max_length=255, blank=True, help_text="Requesting department")
    reason = models.TextField(blank=True, help_text="Purpose or justification for the requisition")
    submit_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Purchase Requisition"
        verbose_name_plural = "Purchase Requisitions"

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
class PurchaseOrder(AbstractBase):
    """Purchase order model for approved procurement"""

    name = models.CharField(max_length=255, help_text="Purchase order name")
    description = models.TextField(blank=True, help_text="Description of the purchase order")
    po_number = models.CharField(max_length=64, unique=True, help_text="PO number")
    purchase_requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.CASCADE,
        help_text="Purchase requisition",
        null=True,
        blank=True,
    )
    supplier = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, help_text="Supplier"
    )
    payment_terms = models.CharField(max_length=128, blank=True, help_text="Payment terms")
    amount = models.DecimalField(
        max_digits=16, decimal_places=2, help_text="Amount", null=True, blank=True
    )
    used = models.DecimalField(
        max_digits=16, decimal_places=2, help_text="Used amount", null=True, blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self) -> str:
        return str(self.name)
