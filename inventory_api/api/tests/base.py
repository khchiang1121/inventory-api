from typing import Tuple

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="admin")
    if not user.is_staff:
        user.is_staff = True
        user.is_superuser = True
        user.set_password("admin")
        user.save()
    return user


@pytest.fixture
def auth_client(api_client: APIClient, admin_user) -> APIClient:
    # Using DRF token auth login endpoint
    from rest_framework.authtoken.models import Token

    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


from ..models import (
    Baremetal,
    BaremetalGroup,
    BaremetalModel,
    DataCenter,
    Fab,
    Manufacturer,
    Phase,
    PurchaseOrder,
    PurchaseRequisition,
    Rack,
    Room,
    Supplier,
    Tenant,
    VirtualMachineSpecification,
)

User = get_user_model()


class APITestSetup(APITestCase):
    """Base test class with common setup methods"""

    def setUp(self):
        """Set up test data"""
        # Create test user with superuser privileges
        self.user = User.objects.create_superuser(
            username="testuser",
            password="testpass123",
            account="test_account",
            status="active",
        )

        # Create test tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant", description="Test Description", status="active"
        )

        # Create test infrastructure hierarchy
        self.fabrication = Fab.objects.create(name="Test Fab")
        self.phase = Phase.objects.create(name="Test Phase", fab=self.fabrication)
        self.data_center = DataCenter.objects.create(name="Test DC", phase=self.phase)
        self.room = Room.objects.create(name="Test Room", datacenter=self.data_center)
        self.rack = Rack.objects.create(
            name="Test Rack", bgp_number="AS12345", as_number=67890, room=self.room
        )

        # Create test baremetal group
        self.baremetal_group = BaremetalGroup.objects.create(
            name="Test Group",
            description="Test Description",
            total_cpu=100,
            total_memory=1000,
            total_storage=10000,
            total_gpu=8,
            available_cpu=100,
            available_memory=1000,
            available_storage=10000,
            available_gpu=4,
            status="active",
        )

        # Create required related objects for baremetal
        self.manufacturer = Manufacturer.objects.create(name="Dell")
        self.baremetal_model = BaremetalModel.objects.create(
            name="PowerEdge R740",
            manufacturer=self.manufacturer,
            total_cpu=64,
            total_memory=1024,
            total_storage=10000,
            total_gpu=4,
        )
        # Use the already created infrastructure objects
        # self.fabrication, self.phase, self.data_center already created above
        self.purchase_requisition = PurchaseRequisition.objects.create(
            pr_number="PR-2024-001",
            requested_by="John Doe",
            department="IT",
            reason="Test server",
        )
        self.supplier = Supplier.objects.create(name="Dell")
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO-2024-001",
            supplier=self.supplier,
            payment_terms="Net 30",
        )

        # Create test baremetal
        self.baremetal = Baremetal.objects.create(
            name="Test Baremetal",
            serial_number="SN123456",
            model=self.baremetal_model,
            fabrication=self.fabrication,
            phase=self.phase,
            data_center=self.data_center,
            rack=self.rack,
            status="active",
            available_cpu=64,
            available_memory=1024,
            available_storage=10000,
            group=self.baremetal_group,
            pr=self.purchase_requisition,
            po=self.purchase_order,
        )

        # Create test VM specification
        self.vm_spec = VirtualMachineSpecification.objects.create(
            name="Test Spec",
            generation="v1",
            required_cpu=2,
            required_memory=4,
            required_storage=100,
        )
