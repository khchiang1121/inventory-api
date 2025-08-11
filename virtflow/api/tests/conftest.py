import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="admin")
    if not user.is_staff:
        user.is_staff = True
        user.is_superuser = True
        user.set_password("admin")
        user.save()
    return user


@pytest.fixture
def auth_client(api_client: APIClient, admin_user) -> APIClient:
    from rest_framework.authtoken.models import Token

    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client

