import pytest

from .base import auth_client


@pytest.mark.django_db
def test_baremetal_group_quota(auth_client):
    tenant = auth_client.post(
        "/api/v1/tenants", {"name": "tq", "status": "active"}, format="json"
    ).data
    group = auth_client.post(
        "/api/v1/baremetal-groups",
        {
            "name": "gq",
            "description": "",
            "total_cpu": 100,
            "total_memory": 100,
            "total_storage": 100,
            "available_cpu": 100,
            "available_memory": 100,
            "available_storage": 100,
            "status": "active",
        },
        format="json",
    ).data
    payload = {
        "group": group["id"],
        "tenant": tenant["id"],
        "cpu_quota_percentage": 50.0,
        "memory_quota": 50,
        "storage_quota": 50,
    }
    r = auth_client.post(
        "/api/v1/baremetal-group-tenant-quotas", payload, format="json"
    )
    assert r.status_code == 201
    qid = r.data["id"]
    assert (
        auth_client.patch(
            f"/api/v1/baremetal-group-tenant-quotas/{qid}",
            {"cpu_quota_percentage": 60.0},
            format="json",
        ).status_code
        == 200
    )
    assert auth_client.delete(
        f"/api/v1/baremetal-group-tenant-quotas/{qid}"
    ).status_code in (204, 200)
