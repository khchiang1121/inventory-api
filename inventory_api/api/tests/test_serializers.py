"""
Comprehensive tests for Django REST Framework serializers.
Tests serialization, deserialization, validation, and edge cases.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from ..models import (
    VLAN,
    VRF,
    AnsibleGroup,
    AnsibleHost,
    Baremetal,
    BaremetalGroup,
    BaremetalModel,
    BGPConfig,
    DataCenter,
    Fabrication,
    K8sCluster,
    Manufacturer,
    NetworkInterface,
    Phase,
    PurchaseOrder,
    PurchaseRequisition,
    Rack,
    Room,
    ServiceMesh,
    Tenant,
    VirtualMachine,
    VirtualMachineSpecification,
)
from ..v1.serializers import (
    AnsibleGroupCreateSerializer,
    AnsibleHostCreateSerializer,
    BaremetalGroupSerializer,
    BaremetalModelCreateSerializer,
    BaremetalSerializer,
    BGPConfigSerializer,
    CustomUserSerializer,
    DataCenterSerializer,
    FabricationSerializer,
    K8sClusterSerializer,
    ManufacturerSerializer,
    NetworkInterfaceSerializer,
    PhaseSerializer,
    PurchaseOrderSerializer,
    PurchaseRequisitionSerializer,
    RackSerializer,
    RoomSerializer,
    ServiceMeshSerializer,
    TenantSerializer,
    UserProfileSerializer,
    VirtualMachineSerializer,
    VirtualMachineSpecificationSerializer,
    VLANSerializer,
    VRFSerializer,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializers:
    """Test user-related serializers"""

    def test_custom_user_serializer_valid_data(self):
        """Test CustomUserSerializer with valid data"""
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
            "account": "test_account",
            "status": "active",
        }
        serializer = CustomUserSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"

    def test_custom_user_serializer_missing_required_fields(self):
        """Test CustomUserSerializer with missing required fields"""
        data = {"email": "test@example.com"}
        serializer = CustomUserSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_user_profile_serializer_excludes_password(self):
        """Test UserProfileSerializer excludes sensitive fields"""
        user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        serializer = UserProfileSerializer(user)
        assert "password" not in serializer.data
        assert serializer.data["username"] == "testuser"
        assert serializer.data["email"] == "test@example.com"


@pytest.mark.django_db
class TestInfrastructureSerializers:
    """Test infrastructure-related serializers"""

    def test_fabrication_serializer_valid_data(self):
        """Test FabricationSerializer with valid data"""
        data = {"name": "FAB001", "external_system_id": "legacy_001"}
        serializer = FabricationSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        fabrication = serializer.save()
        assert fabrication.name == "FAB001"

    def test_fabrication_serializer_duplicate_name(self):
        """Test FabricationSerializer with duplicate name"""
        Fabrication.objects.create(name="FAB001")
        data = {"name": "FAB001"}
        serializer = FabricationSerializer(data=data)
        assert not serializer.is_valid()

    def test_rack_serializer_with_all_fields(self):
        """Test RackSerializer with all fields"""
        data = {
            "name": "RACK001",
            "bgp_number": "AS12345",
            "as_number": 65001,
            "height_units": 42,
            "used_units": 10,
            "available_units": 32,
            "power_capacity": "10.50",
            "status": "active",
        }
        serializer = RackSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        rack = serializer.save()
        assert rack.height_units == 42
        assert rack.power_capacity == 10.50

    def test_rack_serializer_invalid_status(self):
        """Test RackSerializer with invalid status"""
        data = {
            "name": "RACK001",
            "bgp_number": "AS12345",
            "as_number": 65001,
            "status": "invalid_status",
        }
        serializer = RackSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestNetworkSerializers:
    """Test network-related serializers"""

    def test_vlan_serializer_valid_data(self):
        """Test VLANSerializer with valid data"""
        data = {"vlan_id": 100, "name": "Production"}
        serializer = VLANSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        vlan = serializer.save()
        assert vlan.vlan_id == 100

    def test_vlan_serializer_duplicate_vlan_id(self):
        """Test VLANSerializer with duplicate VLAN ID"""
        VLAN.objects.create(vlan_id=100, name="Existing")
        data = {"vlan_id": 100, "name": "New"}
        serializer = VLANSerializer(data=data)
        assert not serializer.is_valid()

    def test_bgp_config_serializer_valid_ips(self):
        """Test BGPConfigSerializer with valid IP addresses"""
        data = {
            "asn": 65001,
            "peer_ip": "192.168.1.1",
            "local_ip": "192.168.1.2",
            "password": "secret123",
        }
        serializer = BGPConfigSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"

    def test_bgp_config_serializer_invalid_ip(self):
        """Test BGPConfigSerializer with invalid IP address"""
        data = {
            "asn": 65001,
            "peer_ip": "256.256.256.256",  # Invalid IP
            "local_ip": "192.168.1.2",
        }
        serializer = BGPConfigSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestBaremetalSerializers:
    """Test baremetal-related serializers"""

    def test_manufacturer_serializer_valid_data(self):
        """Test ManufacturerSerializer with valid data"""
        data = {"name": "Dell"}
        serializer = ManufacturerSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        manufacturer = serializer.save()
        assert manufacturer.name == "Dell"

    def test_baremetal_model_serializer_with_specs(self):
        """Test BaremetalModelSerializer with specifications"""
        manufacturer = Manufacturer.objects.create(name="Dell")
        data = {
            "name": "PowerEdge R740",
            "manufacturer": str(manufacturer.id),
            "suppliers": [],
            "total_cpu": 64,
            "total_memory": 1024,
            "total_storage": 10000,
            "total_gpu": 4,
        }
        serializer = BaremetalModelCreateSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        model = serializer.save()
        assert model.total_cpu == 64
        assert model.manufacturer == manufacturer


@pytest.mark.django_db
class TestTenantSerializers:
    """Test tenant and VM-related serializers"""

    def test_tenant_serializer_valid_data(self):
        """Test TenantSerializer with valid data"""
        data = {
            "name": "Test Tenant",
            "description": "Test Description",
            "status": "active",
        }
        serializer = TenantSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        tenant = serializer.save()
        assert tenant.name == "Test Tenant"
        assert tenant.status == "active"

    def test_vm_specification_serializer_with_requirements(self):
        """Test VirtualMachineSpecificationSerializer with resource requirements"""
        data = {
            "name": "Standard VM",
            "generation": "v2",
            "required_cpu": 4,
            "required_memory": 8,
            "required_storage": 100,
            "description": "Standard VM configuration",
        }
        serializer = VirtualMachineSpecificationSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        spec = serializer.save()
        assert spec.required_cpu == 4
        assert spec.required_memory == 8


@pytest.mark.django_db
class TestPurchaseSerializers:
    """Test purchase-related serializers"""

    def test_purchase_requisition_serializer_valid_data(self):
        """Test PurchaseRequisitionSerializer with valid data"""
        data = {
            "pr_number": "PR-2024-001",
            "requested_by": "John Doe",
            "department": "IT",
            "reason": "Server upgrade",
            "status": "pending",
        }
        serializer = PurchaseRequisitionSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        pr = serializer.save()
        assert pr.pr_number == "PR-2024-001"

    def test_purchase_order_serializer_with_vendor_info(self):
        """Test PurchaseOrderSerializer with vendor information"""
        data = {
            "po_number": "PO-2024-001",
            "vendor_name": "Dell Technologies",
            "payment_terms": "Net 30",
            "issued_by": "Procurement Team",
            "status": "issued",
        }
        serializer = PurchaseOrderSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        po = serializer.save()
        assert po.vendor_name == "Dell Technologies"


@pytest.mark.django_db
class TestAnsibleSerializers:
    """Test Ansible-related serializers"""

    def test_ansible_group_serializer_valid_data(self):
        """Test AnsibleGroupSerializer with valid data"""
        # First create an inventory
        from inventory_api.api.models import AnsibleInventory

        inventory = AnsibleInventory.objects.create(
            name="test_inventory", description="Test inventory", status="active"
        )

        data = {
            "inventory": str(inventory.id),
            "name": "web_servers",
            "description": "Web server group",
            "status": "active",
        }
        serializer = AnsibleGroupCreateSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        group = serializer.save()
        assert group.name == "web_servers"
        assert group.description == "Web server group"

    def test_ansible_host_serializer_with_connection_details(self):
        """Test AnsibleHostSerializer with connection details"""
        # Create required objects for AnsibleHost
        from inventory_api.api.models import AnsibleInventory

        inventory = AnsibleInventory.objects.create(
            name="test_inventory_host", description="Test inventory for host", status="active"
        )
        group = AnsibleGroup.objects.create(name="test_group", inventory=inventory)
        tenant = Tenant.objects.create(name="Test Tenant", status="active")

        # Get content type for tenant
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Tenant)

        data = {
            "inventory": str(inventory.id),
            "group": str(group.id),
            "content_type": content_type.id,
            "object_id": str(tenant.id),
            "ansible_host": "192.168.1.10",
            "ansible_port": 22,
            "ansible_user": "deploy",
            "metadata": {"role": "primary"},
        }
        serializer = AnsibleHostCreateSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"
        host = serializer.save()
        assert host.ansible_host == "192.168.1.10"
        assert host.ansible_port == 22


@pytest.mark.django_db
class TestSerializerEdgeCases:
    """Test edge cases and error handling in serializers"""

    def test_serializer_with_none_values(self):
        """Test serializers handle None values correctly"""
        data = {
            "name": "Test",
            "description": "",  # Empty string instead of None
            "status": "active",
        }
        serializer = TenantSerializer(data=data)
        assert serializer.is_valid(), f"Validation errors: {serializer.errors}"

    def test_serializer_with_empty_strings(self):
        """Test serializers handle empty strings correctly"""
        data = {"name": "Test", "description": "", "status": "active"}  # Empty string
        serializer = TenantSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_with_very_long_strings(self):
        """Test serializers handle string length validation"""
        long_name = "x" * 1000  # Very long name
        data = {"name": long_name}
        serializer = FabricationSerializer(data=data)
        assert not serializer.is_valid()  # Should fail due to max_length

    def test_serializer_with_special_characters(self):
        """Test serializers handle special characters"""
        data = {"name": "Test-Fab_001@#$", "external_system_id": "legacy!@#$%"}
        serializer = FabricationSerializer(data=data)
        assert serializer.is_valid()  # Should handle special characters
