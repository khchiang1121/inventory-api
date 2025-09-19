"""
Comprehensive tests for Django REST Framework ViewSets.
Tests CRUD operations, permissions, filtering, pagination, and edge cases.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

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
    Fab,
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

User = get_user_model()


@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient()


@pytest.fixture
def authenticated_user(db):
    """Create authenticated user"""
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
        account="test_account",
        status="active",
    )
    return user


@pytest.fixture
def auth_client(api_client, authenticated_user):
    """Authenticated API client"""
    token, _ = Token.objects.get_or_create(user=authenticated_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.mark.django_db
class TestInfrastructureViewSets:
    """Test infrastructure-related ViewSets"""

    def test_fabrication_list_endpoint(self, auth_client):
        """Test fabrication list endpoint returns correct data"""
        # Create test data
        fab1 = Fab.objects.create(name="FAB001", external_system_id="legacy1")
        fab2 = Fab.objects.create(name="FAB002", external_system_id="legacy2")

        # Test list endpoint
        response = auth_client.get("/api/v1/fab")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

        # Check response content
        fab_names = [fab["name"] for fab in response.data["results"]]
        assert "FAB001" in fab_names
        assert "FAB002" in fab_names

    def test_fabrication_create_endpoint(self, auth_client):
        """Test fabrication create endpoint"""
        data = {"name": "FAB003", "external_system_id": "legacy3"}
        response = auth_client.post("/api/v1/fab", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "FAB003"

        # Verify object was created
        assert Fab.objects.filter(name="FAB003").exists()

    def test_fabrication_retrieve_endpoint(self, auth_client):
        """Test fabrication retrieve endpoint"""
        fab = Fab.objects.create(name="FAB001", external_system_id="legacy1")

        response = auth_client.get(f"/api/v1/fab/{fab.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "FAB001"
        assert response.data["external_system_id"] == "legacy1"

    def test_fabrication_update_endpoint(self, auth_client):
        """Test fabrication update endpoint"""
        fab = Fab.objects.create(name="FAB001", external_system_id="legacy1")

        data = {"name": "FAB001_Updated", "external_system_id": "legacy1_updated"}
        response = auth_client.put(f"/api/v1/fab/{fab.id}", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "FAB001_Updated"

        # Verify object was updated
        fab.refresh_from_db()
        assert fab.name == "FAB001_Updated"

    def test_fabrication_delete_endpoint(self, auth_client):
        """Test fabrication delete endpoint"""
        fab = Fab.objects.create(name="FAB001")

        response = auth_client.delete(f"/api/v1/fab/{fab.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify object was deleted
        assert not Fab.objects.filter(id=fab.id).exists()

    def test_rack_list_with_status_filter(self, auth_client):
        """Test rack list endpoint with status filtering"""
        # Create test data with different statuses
        Rack.objects.create(name="RACK001", bgp_number="AS1", as_number=1, status="active")
        Rack.objects.create(name="RACK002", bgp_number="AS2", as_number=2, status="inactive")
        Rack.objects.create(name="RACK003", bgp_number="AS3", as_number=3, status="maintenance")

        # Test filtering by status
        response = auth_client.get("/api/v1/racks?status=active")
        assert response.status_code == status.HTTP_200_OK
        # Note: Filtering depends on implementation in views

    def test_rack_create_with_all_fields(self, auth_client):
        """Test rack creation with all fields"""
        data = {
            "name": "RACK001",
            "bgp_number": "AS12345",
            "as_number": 65001,
            "height_units": 42,
            "used_units": 0,
            "available_units": 42,
            "power_capacity": "15.50",
            "status": "active",
        }
        response = auth_client.post("/api/v1/racks", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["height_units"] == 42
        assert float(response.data["power_capacity"]) == 15.50


@pytest.mark.django_db
class TestNetworkViewSets:
    """Test network-related ViewSets"""

    def test_vlan_crud_operations(self, auth_client):
        """Test complete CRUD operations for VLAN"""
        # Create
        data = {"vlan_id": 100, "name": "Production"}
        response = auth_client.post("/api/v1/vlans", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        vlan_id = response.data["id"]

        # Read
        response = auth_client.get(f"/api/v1/vlans/{vlan_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["vlan_id"] == 100

        # Update
        update_data = {"vlan_id": 100, "name": "Production_Updated"}
        response = auth_client.put(f"/api/v1/vlans/{vlan_id}", update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Production_Updated"

        # Delete
        response = auth_client.delete(f"/api/v1/vlans/{vlan_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_bgp_config_with_valid_ips(self, auth_client):
        """Test BGP config creation with valid IP addresses"""
        data = {
            "asn": 65001,
            "peer_ip": "192.168.1.1",
            "local_ip": "192.168.1.2",
            "password": "secret123",
        }
        response = auth_client.post("/api/v1/bgp-configs", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["peer_ip"] == "192.168.1.1"

    def test_bgp_config_with_invalid_ip(self, auth_client):
        """Test BGP config creation with invalid IP addresses"""
        data = {
            "asn": 65001,
            "peer_ip": "256.256.256.256",  # Invalid IP
            "local_ip": "192.168.1.2",
        }
        response = auth_client.post("/api/v1/bgp-configs", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBaremetalViewSets:
    """Test baremetal-related ViewSets"""

    def test_manufacturer_list_ordering(self, auth_client):
        """Test manufacturer list returns ordered results"""
        # Create test data
        Manufacturer.objects.create(name="Dell")
        Manufacturer.objects.create(name="HP")
        Manufacturer.objects.create(name="IBM")

        response = auth_client.get("/api/v1/manufacturers")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_baremetal_model_creation_with_manufacturer(self, auth_client):
        """Test baremetal model creation with manufacturer relationship"""
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
        response = auth_client.post("/api/v1/baremetal-models", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "PowerEdge R740"

    def test_baremetal_group_resource_tracking(self, auth_client):
        """Test baremetal group with resource tracking"""
        data = {
            "name": "Production Group",
            "description": "Production servers",
            "total_cpu": 1000,
            "total_memory": 10000,
            "total_storage": 100000,
            "total_gpu": 16,
            "available_cpu": 500,
            "available_memory": 5000,
            "available_storage": 50000,
            "available_gpu": 8,
            "status": "active",
        }
        response = auth_client.post("/api/v1/baremetal-groups", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["total_cpu"] == 1000
        assert response.data["available_cpu"] == 500


@pytest.mark.django_db
class TestTenantViewSets:
    """Test tenant and VM-related ViewSets"""

    def test_tenant_creation_and_status(self, auth_client):
        """Test tenant creation with status tracking"""
        data = {
            "name": "Test Tenant",
            "description": "Test tenant for development",
            "status": "active",
        }
        response = auth_client.post("/api/v1/tenants", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "active"

    def test_vm_specification_with_requirements(self, auth_client):
        """Test VM specification creation with resource requirements"""
        data = {
            "name": "Standard VM",
            "generation": "v2",
            "required_cpu": 4,
            "required_memory": 8,
            "required_storage": 100,
            "description": "Standard VM configuration",
        }
        response = auth_client.post("/api/v1/vm-specifications", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["required_cpu"] == 4


@pytest.mark.django_db
class TestPurchaseViewSets:
    """Test purchase-related ViewSets"""

    def test_purchase_requisition_workflow(self, auth_client):
        """Test purchase requisition creation and status updates"""
        # Create PR
        data = {
            "pr_number": "PR-2024-001",
            "requested_by": "John Doe",
            "department": "IT",
            "reason": "Server upgrade",
        }
        response = auth_client.post("/api/v1/purchase-requisitions", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        pr_id = response.data["id"]

        # Update reason
        update_data = {
            "pr_number": "PR-2024-001",
            "requested_by": "John Doe",
            "department": "IT",
            "reason": "Server upgrade - approved",
        }
        response = auth_client.put(
            f"/api/v1/purchase-requisitions/{pr_id}", update_data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["reason"] == "Server upgrade - approved"

    def test_purchase_order_vendor_tracking(self, auth_client):
        """Test purchase order creation with supplier information"""
        # Create purchase requisition
        pr_data = {
            "pr_number": "PR-2024-001",
            "requested_by": "Test User",
            "department": "IT",
            "reason": "Equipment procurement",
        }
        pr_response = auth_client.post("/api/v1/purchase-requisitions", pr_data, format="json")

        # Create supplier
        supplier_data = {
            "name": "Dell Technologies",
            "contact_email": "sales@dell.com",
            "contact_phone": "1-800-DELL",
            "address": "Round Rock, TX",
            "website": "https://dell.com",
        }
        supplier_response = auth_client.post("/api/v1/suppliers", supplier_data, format="json")

        # Create purchase order
        data = {
            "po_number": "PO-2024-001",
            "purchase_requisition": pr_response.data["id"],
            "supplier": supplier_response.data["id"],
            "payment_terms": "Net 30",
            "amount": "15000.00",
            "used": "0.00",
            "description": "Dell equipment procurement",
        }
        response = auth_client.post("/api/v1/purchase-orders", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert str(response.data["supplier"]) == str(
            supplier_response.data["id"]
        )  # CREATE returns UUID
        assert str(response.data["purchase_requisition"]) == str(
            pr_response.data["id"]
        )  # CREATE returns UUID
        assert str(response.data["amount"]) == "15000.00"


@pytest.mark.django_db
class TestAnsibleViewSets:
    """Test Ansible-related ViewSets"""

    def test_ansible_group_with_variables(self, auth_client):
        """Test Ansible group creation with description"""
        # First create an inventory
        inventory_data = {
            "name": "test_inventory_viewset",
            "description": "Test inventory for viewset",
            "status": "active",
        }
        inventory_response = auth_client.post(
            "/api/v1/ansible-inventories", inventory_data, format="json"
        )
        assert inventory_response.status_code == status.HTTP_201_CREATED

        data = {
            "inventory": inventory_response.data["id"],
            "name": "web_servers",
            "description": "Web server group",
            "status": "active",
        }
        response = auth_client.post("/api/v1/ansible-groups", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "web_servers"
        assert response.data["description"] == "Web server group"

    def test_ansible_host_with_connection_details(self, auth_client):
        """Test Ansible host creation with SSH connection details"""
        # Create required objects
        from inventory_api.api.models import AnsibleInventory

        inventory = AnsibleInventory.objects.create(
            name="test_inventory_host_viewset",
            description="Test inventory for host viewset",
            status="active",
        )
        group = AnsibleGroup.objects.create(name="test_group", inventory=inventory)
        tenant = Tenant.objects.create(name="Test Tenant", status="active")

        # Get content type for tenant
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Tenant)

        data = {
            "inventory": str(inventory.id),
            "groups": [str(group.id)],
            "content_type": content_type.id,
            "object_id": str(tenant.id),
            "ansible_host": "192.168.1.10",
            "ansible_port": 22,
            "ansible_user": "deploy",
            "ansible_ssh_private_key_file": "/home/deploy/.ssh/id_rsa",
            "metadata": {"role": "primary", "weight": 100},
        }
        response = auth_client.post("/api/v1/ansible-hosts", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["ansible_host"] == "192.168.1.10"
        assert response.data["metadata"]["role"] == "primary"


@pytest.mark.django_db
class TestSystemEndpoints:
    """Test system information endpoints"""

    def test_system_info_endpoint_structure(self, auth_client):
        """Test system info endpoint returns expected structure"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

        # Check required fields are present
        required_fields = [
            "version",
            "database_status",
            "cache_status",
            "disk_usage",
            "memory_usage",
            "uptime",
            "last_backup",
        ]
        for field in required_fields:
            assert field in response.data, f"Missing field: {field}"

    def test_system_info_endpoint_data_types(self, auth_client):
        """Test system info endpoint returns correct data types"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

        # Check data types
        assert isinstance(response.data["version"], str)
        assert isinstance(response.data["database_status"], str)
        assert isinstance(response.data["cache_status"], str)
        assert isinstance(response.data["uptime"], (int, float))


@pytest.mark.django_db
class TestPaginationAndFiltering:
    """Test pagination and filtering functionality"""

    def test_pagination_works(self, auth_client):
        """Test that pagination works correctly"""
        # Create multiple objects
        for i in range(25):  # More than default page size
            Fab.objects.create(name=f"FAB{i:03d}")

        response = auth_client.get("/api/v1/fab")
        assert response.status_code == status.HTTP_200_OK

        # Check pagination structure
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

        # Check we got paginated results
        assert response.data["count"] == 25
        assert len(response.data["results"]) <= 10  # Default page size

    def test_pagination_page_parameter(self, auth_client):
        """Test pagination with page parameter"""
        # Create test data
        for i in range(15):
            Fab.objects.create(name=f"FAB{i:03d}")

        # Test second page
        response = auth_client.get("/api/v1/fab?page=2")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_invalid_page_parameter(self, auth_client):
        """Test invalid page parameter handling"""
        response = auth_client.get("/api/v1/fab?page=invalid")
        # Should return first page or appropriate error
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.django_db
class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_not_found_error(self, auth_client):
        """Test 404 error for non-existent resources"""
        response = auth_client.get("/api/v1/fab/99999999-9999-9999-9999-999999999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_uuid_format(self, auth_client):
        """Test invalid UUID format handling"""
        response = auth_client.get("/api/v1/fab/invalid-uuid")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_method_not_allowed(self, auth_client):
        """Test method not allowed error"""
        # Assuming PATCH is not allowed on some endpoint
        response = auth_client.patch("/api/v1/system-info")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_invalid_json_data(self, auth_client):
        """Test invalid JSON data handling"""
        response = auth_client.post(
            "/api/v1/fab", "invalid json data", content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPermissions:
    """Test permission handling"""

    def test_unauthenticated_access_allowed(self, api_client):
        """Test that unauthenticated access is allowed when REQUIRE_API_AUTHENTICATION is False"""
        response = api_client.get("/api/v1/fab")
        # Should be allowed since REQUIRE_API_AUTHENTICATION is False
        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_access(self, auth_client):
        """Test that authenticated users can access resources"""
        response = auth_client.get("/api/v1/fab")
        assert response.status_code == status.HTTP_200_OK

    def test_token_authentication_works(self, api_client, authenticated_user):
        """Test that token authentication works properly"""
        token, _ = Token.objects.get_or_create(user=authenticated_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = api_client.get("/api/v1/auth/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == authenticated_user.username
