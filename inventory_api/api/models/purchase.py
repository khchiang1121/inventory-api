from django.db import models

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
    vendor_name = models.CharField(max_length=255, help_text="Vendor name")
    payment_terms = models.CharField(max_length=128, blank=True, help_text="Payment terms")
    delivery_date = models.DateField(null=True, blank=True)
    issued_by = models.CharField(
        max_length=100, blank=True, help_text="Procurement staff name or ID"
    )
