"""
Comprehensive tests for API response validation and content checking.
Tests response structure, content validation, and data integrity.
"""

import json

import pytest
from django.contrib.auth import get_user_model
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
    Brand,
    DataCenter,
    Fabrication,
    K8sCluster,
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
    return APIClient()


@pytest.fixture
def authenticated_user(db):
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
    token, _ = Token.objects.get_or_create(user=authenticated_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.mark.django_db
class TestAPIResponseStructure:
    """Test API response structure and format"""

    def test_list_response_structure(self, auth_client):
        """Test that list endpoints return proper pagination structure"""
        # Create some test data
        Fabrication.objects.create(name="FAB001")
        Fabrication.objects.create(name="FAB002")

        response = auth_client.get("/api/v1/fabrications")
        assert response.status_code == status.HTTP_200_OK

        # Check pagination structure
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

        # Check results structure
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) == 2

        # Check individual result structure
        result = response.data["results"][0]
        expected_fields = ["id", "name", "old_system_id", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in result, f"Missing field: {field}"

    def test_detail_response_structure(self, auth_client):
        """Test that detail endpoints return proper object structure"""
        fab = Fabrication.objects.create(name="FAB001", old_system_id="legacy1")

        response = auth_client.get(f"/api/v1/fabrications/{fab.id}")
        assert response.status_code == status.HTTP_200_OK

        # Check all expected fields are present
        expected_fields = ["id", "name", "old_system_id", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in response.data, f"Missing field: {field}"

        # Check field types
        assert isinstance(response.data["id"], str)  # UUID as string
        assert isinstance(response.data["name"], str)
        assert response.data["created_at"] is not None
        assert response.data["updated_at"] is not None

    def test_create_response_structure(self, auth_client):
        """Test that create endpoints return proper response structure"""
        data = {"name": "FAB003", "old_system_id": "legacy3"}
        response = auth_client.post("/api/v1/fabrications", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        # Check all fields are returned
        expected_fields = ["id", "name", "old_system_id", "created_at", "updated_at"]
        for field in expected_fields:
            assert field in response.data, f"Missing field: {field}"

        # Check created object matches input
        assert response.data["name"] == data["name"]
        assert response.data["old_system_id"] == data["old_system_id"]


@pytest.mark.django_db
class TestAPIResponseContent:
    """Test API response content validation"""

    def test_fabrication_response_content(self, auth_client):
        """Test fabrication response contains correct content"""
        fab = Fabrication.objects.create(name="FAB001", old_system_id="legacy1")

        response = auth_client.get(f"/api/v1/fabrications/{fab.id}")
        assert response.status_code == status.HTTP_200_OK

        # Validate content
        assert response.data["name"] == "FAB001"
        assert response.data["old_system_id"] == "legacy1"
        assert response.data["id"] == str(fab.id)

    def test_rack_response_with_numeric_fields(self, auth_client):
        """Test rack response contains correct numeric field types"""
        rack = Rack.objects.create(
            name="RACK001",
            bgp_number="AS12345",
            as_number=65001,
            height_units=42,
            used_units=10,
            available_units=32,
            power_capacity=15.50,
            status="active",
        )

        response = auth_client.get(f"/api/v1/racks/{rack.id}")
        assert response.status_code == status.HTTP_200_OK

        # Check numeric fields
        assert response.data["as_number"] == 65001
        assert response.data["height_units"] == 42
        assert response.data["used_units"] == 10
        assert response.data["available_units"] == 32
        assert float(response.data["power_capacity"]) == 15.50

    def test_vlan_response_validation(self, auth_client):
        """Test VLAN response contains valid VLAN ID"""
        vlan = VLAN.objects.create(vlan_id=100, name="Production")

        response = auth_client.get(f"/api/v1/vlans/{vlan.id}")
        assert response.status_code == status.HTTP_200_OK

        # Validate VLAN-specific fields
        assert response.data["vlan_id"] == 100
        assert response.data["name"] == "Production"
        assert 1 <= response.data["vlan_id"] <= 4094  # Valid VLAN range

    def test_bgp_config_response_ip_validation(self, auth_client):
        """Test BGP config response contains valid IP addresses"""
        bgp = BGPConfig.objects.create(
            asn=65001,
            peer_ip="192.168.1.1",
            local_ip="192.168.1.2",
            password="secret123",
        )

        response = auth_client.get(f"/api/v1/bgp-configs/{bgp.id}")
        assert response.status_code == status.HTTP_200_OK

        # Validate IP addresses
        import ipaddress

        ipaddress.IPv4Address(response.data["peer_ip"])  # Should not raise exception
        ipaddress.IPv4Address(response.data["local_ip"])  # Should not raise exception

        # Validate ASN
        assert 1 <= response.data["asn"] <= 4294967295  # Valid ASN range


@pytest.mark.django_db
class TestComplexObjectResponses:
    """Test responses for objects with relationships"""

    def test_baremetal_model_with_brand_response(self, auth_client):
        """Test baremetal model response includes brand information"""
        brand = Brand.objects.create(name="Dell")
        model = BaremetalModel.objects.create(
            name="PowerEdge R740",
            brand=brand,
            total_cpu=64,
            total_memory=1024,
            total_storage=10000,
        )

        response = auth_client.get(f"/api/v1/baremetal-models/{model.id}")
        assert response.status_code == status.HTTP_200_OK

        # Check brand relationship is included
        assert "brand" in response.data
        # Brand is returned as a nested object, not just an ID
        assert response.data["brand"]["id"] == str(brand.id)
        assert response.data["brand"]["name"] == "Dell"

    def test_network_interface_response_structure(self, auth_client):
        """Test network interface response includes all network fields"""
        # Create a baremetal to associate with network interface
        brand = Brand.objects.create(name="Dell")
        model = BaremetalModel.objects.create(
            name="PowerEdge R740",
            brand=brand,
            total_cpu=64,
            total_memory=1024,
            total_storage=10000,
        )

        # Create required objects for baremetal
        fabrication = Fabrication.objects.create(name="FAB1")
        phase = Phase.objects.create(name="PHASE1")
        data_center = DataCenter.objects.create(name="DC1")
        rack = Rack.objects.create(name="RACK1", bgp_number="AS1", as_number=1)
        baremetal_group = BaremetalGroup.objects.create(
            name="Group1",
            total_cpu=100,
            total_memory=1000,
            total_storage=10000,
            available_cpu=100,
            available_memory=1000,
            available_storage=10000,
        )
        pr = PurchaseRequisition.objects.create(
            pr_number="PR-001", requested_by="Test", department="IT", reason="Test"
        )
        po = PurchaseOrder.objects.create(
            po_number="PO-001",
            vendor_name="Dell",
            payment_terms="Net 30",
            issued_by="Test",
        )

        baremetal = Baremetal.objects.create(
            name="BM001",
            serial_number="SN123",
            model=model,
            fabrication=fabrication,
            phase=phase,
            data_center=data_center,
            rack=rack,
            status="active",
            available_cpu=64,
            available_memory=1024,
            available_storage=10000,
            group=baremetal_group,
            pr=pr,
            po=po,
        )

        # Create VLAN and VRF for network interface
        vlan = VLAN.objects.create(vlan_id=100, name="Production")
        vrf = VRF.objects.create(name="VRF1", route_distinguisher="65001:100")

        # Create network interface
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Baremetal)

        ni = NetworkInterface.objects.create(
            content_type=content_type,
            object_id=baremetal.id,
            name="eth0",
            mac_address="00:11:22:33:44:55",
            is_primary=True,
            ipv4_address="192.168.1.10",
            ipv4_netmask="255.255.255.0",
            gateway="192.168.1.1",
            dns_servers="8.8.8.8,8.8.4.4",
            vlan=vlan,
            vrf=vrf,
        )

        response = auth_client.get(f"/api/v1/network-interfaces/{ni.id}")
        assert response.status_code == status.HTTP_200_OK

        # Check network-specific fields
        assert response.data["name"] == "eth0"
        assert response.data["mac_address"] == "00:11:22:33:44:55"
        assert response.data["is_primary"] is True
        assert response.data["ipv4_address"] == "192.168.1.10"
        assert response.data["ipv4_netmask"] == "255.255.255.0"
        assert response.data["gateway"] == "192.168.1.1"
        assert response.data["dns_servers"] == "8.8.8.8,8.8.4.4"
        # VLAN and VRF are returned as nested objects
        assert response.data["vlan"]["id"] == str(vlan.id)
        assert response.data["vlan"]["name"] == "Production"
        assert response.data["vrf"]["id"] == str(vrf.id)
        assert response.data["vrf"]["name"] == "VRF1"


@pytest.mark.django_db
class TestJSONResponseValidation:
    """Test JSON response format and structure"""

    def test_response_is_valid_json(self, auth_client):
        """Test that all responses are valid JSON"""
        endpoints = [
            "/api/v1/fabrications",
            "/api/v1/phases",
            "/api/v1/data-centers",
            "/api/v1/rooms",
            "/api/v1/racks",
            "/api/v1/vlans",
            "/api/v1/vrfs",
            "/api/v1/brands",
            "/api/v1/tenants",
        ]

        for endpoint in endpoints:
            response = auth_client.get(endpoint)
            assert response.status_code == status.HTTP_200_OK

            # Ensure response is valid JSON
            try:
                json.loads(response.content)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON response from {endpoint}")

    def test_response_content_type(self, auth_client):
        """Test that responses have correct content type"""
        response = auth_client.get("/api/v1/fabrications")
        assert response.status_code == status.HTTP_200_OK
        assert response["content-type"] == "application/json"

    def test_response_encoding(self, auth_client):
        """Test that responses handle UTF-8 encoding correctly"""
        # Create object with unicode characters
        fab = Fabrication.objects.create(
            name="FAB-测试",  # Chinese characters
            old_system_id="legacy-ñoño",  # Spanish characters
        )

        response = auth_client.get(f"/api/v1/fabrications/{fab.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "FAB-测试"
        assert response.data["old_system_id"] == "legacy-ñoño"


@pytest.mark.django_db
class TestErrorResponseStructure:
    """Test error response structure and content"""

    def test_404_error_response_structure(self, auth_client):
        """Test 404 error response structure"""
        response = auth_client.get(
            "/api/v1/fabrications/99999999-9999-9999-9999-999999999999"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Check error response structure
        assert "detail" in response.data
        assert isinstance(response.data["detail"], str)

    def test_400_error_response_structure(self, auth_client):
        """Test 400 error response structure for validation errors"""
        # Send invalid data
        data = {"name": ""}  # Empty name should cause validation error
        response = auth_client.post("/api/v1/fabrications", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Check error response has field-specific errors
        assert isinstance(response.data, dict)

    def test_405_error_response_structure(self, auth_client):
        """Test 405 error response for method not allowed"""
        # Try unsupported method on system-info (assuming it's read-only)
        response = auth_client.patch("/api/v1/system-info")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        assert "detail" in response.data
        assert "method" in response.data["detail"].lower()


@pytest.mark.django_db
class TestSystemInfoResponse:
    """Test system info endpoint response structure and content"""

    def test_system_info_response_structure(self, auth_client):
        """Test system info response has all required fields"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

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

    def test_system_info_field_types(self, auth_client):
        """Test system info response field types are correct"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

        # Check field types
        assert isinstance(response.data["version"], str)
        assert isinstance(response.data["database_status"], str)
        assert isinstance(response.data["cache_status"], str)
        assert isinstance(response.data["uptime"], (int, float))

        # Check status values are valid
        valid_statuses = ["connected", "disconnected", "healthy", "unhealthy"]
        assert response.data["database_status"] in valid_statuses
        assert response.data["cache_status"] in valid_statuses

    def test_system_info_disk_usage_structure(self, auth_client):
        """Test system info disk usage has correct structure"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

        disk_usage = response.data["disk_usage"]
        assert isinstance(disk_usage, dict)

        required_disk_fields = ["total", "used", "free", "percentage"]
        for field in required_disk_fields:
            assert field in disk_usage, f"Missing disk field: {field}"
            assert isinstance(disk_usage[field], (int, float))

    def test_system_info_memory_usage_structure(self, auth_client):
        """Test system info memory usage has correct structure"""
        response = auth_client.get("/api/v1/system-info")
        assert response.status_code == status.HTTP_200_OK

        memory_usage = response.data["memory_usage"]
        assert isinstance(memory_usage, dict)

        required_memory_fields = ["total", "free", "used", "percentage"]
        for field in required_memory_fields:
            assert field in memory_usage, f"Missing memory field: {field}"
            assert isinstance(memory_usage[field], (int, float))


@pytest.mark.django_db
class TestHealthCheckResponse:
    """Test health check endpoint response"""

    def test_health_check_response_structure(self, api_client):
        """Test health check endpoint response structure"""
        response = api_client.get("/health/")
        assert response.status_code == status.HTTP_200_OK

        required_fields = ["status", "timestamp", "database", "cache", "memory", "disk"]
        for field in required_fields:
            assert field in response.data, f"Missing field: {field}"

    def test_health_check_status_values(self, api_client):
        """Test health check status values are valid"""
        response = api_client.get("/health/")
        assert response.status_code == status.HTTP_200_OK

        valid_statuses = ["healthy", "unhealthy"]
        assert response.data["status"] in valid_statuses
        assert response.data["database"] in valid_statuses
        assert response.data["cache"] in valid_statuses

    def test_health_check_timestamp_format(self, api_client):
        """Test health check timestamp is valid"""
        response = api_client.get("/health/")
        assert response.status_code == status.HTTP_200_OK

        timestamp = response.data["timestamp"]
        assert isinstance(timestamp, (int, float))
        assert timestamp > 0  # Should be a valid Unix timestamp
