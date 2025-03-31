from django.urls import reverse
from rest_framework import status
from .base import APITestSetup

class VirtualMachineAPITests(APITestSetup):
    """Test virtual machine API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('v1:virtualmachine-list')
    
    def test_create_virtual_machine(self):
        """Test creating a new virtual machine"""
        data = {
            'name': 'Test VM',
            'tenant': self.tenant.pk,
            'baremetal': self.baremetal.pk,
            'specification': self.vm_spec.pk,
            'type': 'worker',
            'status': 'active'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_virtual_machines(self):
        """Test listing virtual machines"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # No VMs created yet
    
    def test_virtual_machine_validation(self):
        """Test virtual machine creation validation"""
        data = {
            'name': 'Invalid VM',
            'tenant': self.tenant.pk,
            'baremetal': self.baremetal.pk,
            'specification': self.vm_spec.pk,
            'type': 'invalid_type',  # Invalid type
            'status': 'active'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 