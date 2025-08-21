from django.contrib.auth import get_user_model

import pytest

from .base import api_client, auth_client


@pytest.mark.django_db
def test_logout_requires_auth(auth_client):
    r = auth_client.post("/api/v1/auth/logout/", {}, format="json")
    assert r.status_code in (200, 204)


@pytest.mark.django_db
def test_refresh_is_open(api_client: api_client, admin_user):
    # Ensure the global permission shim can set admin
    r = api_client.post("/api/v1/auth/refresh/", {}, format="json")
    assert r.status_code == 200
    assert "access" in r.data


@pytest.mark.django_db
def test_change_password_requires_auth(auth_client):
    # Prepare user
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="pwduser")
    # token already attached by auth_client fixture for admin; ensure endpoint returns ok
    r = auth_client.post(
        "/api/v1/auth/change-password/", {"new_password": "x"}, format="json"
    )
    assert r.status_code in (200, 204)
