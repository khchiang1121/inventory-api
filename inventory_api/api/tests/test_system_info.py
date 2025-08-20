import pytest
from django.urls import reverse
from rest_framework import status

from .base import auth_client


@pytest.mark.django_db
def test_system_info_list(auth_client):
    resp = auth_client.get("/api/v1/system-info")
    assert resp.status_code == 200
    for key in [
        "version",
        "database_status",
        "cache_status",
        "disk_usage",
        "memory_usage",
        "uptime",
        "last_backup",
    ]:
        assert key in resp.data
