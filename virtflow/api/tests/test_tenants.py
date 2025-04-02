from django.urls import reverse
from rest_framework import status
from ..models import Tenant
from .base import APITestSetup

class TenantAPITests(APITestSetup):
    """Test tenant API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('v1:tenant-list')
    
    def test_create_tenant(self):
        """Test creating a new tenant"""
        data = {
            'name': 'New Tenant',
            'description': 'New Description',
            'status': 'active'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tenant.objects.count(), 2)  # Including the one from setup
    
    def test_list_tenants(self):
        """Test listing tenants"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only the one from setup
    
    def test_retrieve_tenant(self):
        """Test retrieving a specific tenant"""
        url = reverse('v1:tenant-detail', kwargs={'pk': self.tenant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.tenant.name)
    
    def test_update_tenant(self):
        """Test updating a tenant"""
        url = reverse('v1:tenant-detail', kwargs={'pk': self.tenant.pk})
        data = {
            'name': 'Updated Tenant',
            'description': 'Updated Description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.name, 'Updated Tenant') 