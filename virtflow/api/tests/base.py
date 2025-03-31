from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import Tenant, Rack, BaremetalGroup, Baremetal, VirtualMachineSpecification

User = get_user_model()

class APITestSetup(APITestCase):
    """Base test class with common setup methods"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user with superuser privileges
        self.user = User.objects.create_superuser(
            username='testuser',
            password='testpass123',
            account='test_account',
            status='active'
        )
        
        # Create test tenant
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            description='Test Description',
            status='active'
        )
        
        # Create test rack
        self.rack = Rack.objects.create(
            name='Test Rack',
            bgp_number='AS12345',
            as_number='AS67890'
        )
        
        # Create test baremetal group
        self.baremetal_group = BaremetalGroup.objects.create(
            name='Test Group',
            description='Test Description',
            total_cpu=100,
            total_memory=1000,
            total_storage=10000,
            available_cpu=100,
            available_memory=1000,
            available_storage=10000,
            status='active'
        )
        
        # Create test baremetal
        self.baremetal = Baremetal.objects.create(
            name='Test Baremetal',
            serial_number='SN123456',
            rack=self.rack,
            status='active',
            total_cpu=100,
            total_memory=1000,
            total_storage=10000,
            available_cpu=100,
            available_memory=1000,
            available_storage=10000,
            group=self.baremetal_group
        )
        
        # Create test VM specification
        self.vm_spec = VirtualMachineSpecification.objects.create(
            name='Test Spec',
            generation='v1',
            required_cpu=2,
            required_memory=4,
            required_storage=100
        ) 