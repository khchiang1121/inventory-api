from django.db import models

from inventory_api.api.models.baremetal import Supplier

from .base import AbstractBase


class PurchaseRequisition(AbstractBase):
    """Purchase requisition model for procurement requests"""

    pr_number = models.CharField(max_length=64, unique=True, help_text="PR number")
    requested_by = models.CharField(max_length=100, help_text="Requester name or ID")
    department = models.CharField(max_length=100, blank=True, help_text="Requesting department")
    reason = models.TextField(blank=True, help_text="Purpose or justification for the requisition")
    submit_date = models.DateField(auto_now_add=True)


class PurchaseOrder(AbstractBase):
    """Purchase order model for approved procurement"""

    po_number = models.CharField(max_length=64, unique=True, help_text="PO number")
    purchase_requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.CASCADE,
        help_text="Purchase requisition",
        null=True,
        blank=True,
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, help_text="Supplier"
    )
    payment_terms = models.CharField(max_length=128, blank=True, help_text="Payment terms")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Amount", null=True, blank=True
    )
    used = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Used amount", null=True, blank=True
    )
    description = models.TextField(blank=True, help_text="Description")
