from django.urls import reverse
from rest_framework import status
from ..models import Baremetal
from .base import APITestSetup

class BaremetalAPITests(APITestSetup):
    """Test baremetal API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('v1:baremetal-list')
    
    def test_create_baremetal(self):
        """Test creating a new baremetal server"""
        data = {
            'name': 'New Baremetal',
            'serial_number': 'SN789012',
            'rack': self.rack.pk,
            'status': 'active',
            'total_cpu': 100,
            'total_memory': 1000,
            'total_storage': 10000,
            'available_cpu': 100,
            'available_memory': 1000,
            'available_storage': 10000,
            'group': self.baremetal_group.pk
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Baremetal.objects.count(), 2)  # Including the one from setup
    
    def test_list_baremetals(self):
        """Test listing baremetal servers"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only the one from setup
    
    def test_retrieve_baremetal(self):
        """Test retrieving a specific baremetal server"""
        url = reverse('v1:baremetal-detail', kwargs={'pk': self.baremetal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.baremetal.name)
    
    def test_update_baremetal_status(self):
        """Test updating baremetal server status"""
        url = reverse('v1:baremetal-detail', kwargs={'pk': self.baremetal.pk})
        data = {'status': 'inactive'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.baremetal.refresh_from_db()
        self.assertEqual(self.baremetal.status, 'inactive') 