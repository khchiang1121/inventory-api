import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .base import APITestSetup, api_client


@pytest.mark.django_db
def test_login_obtain_token(api_client):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="tester")
    user.set_password("pass1234")
    user.save()

    resp = api_client.post(
        "/api/v1/auth/login/",
        {"username": "tester", "password": "pass1234"},
        format="json",
    )
    assert resp.status_code == 200
    assert "token" in resp.data


@pytest.mark.django_db
def test_me_requires_auth(api_client):
    resp = api_client.get("/api/v1/auth/me/")
    # Since REQUIRE_API_AUTHENTICATION is False, endpoint allows access but user is not authenticated
    assert resp.status_code == 401
    assert resp.data["message"] == "User not authenticated"


@pytest.mark.django_db
def test_me_with_token(api_client):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username="tester2")
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    resp = api_client.get("/api/v1/auth/me/")
    assert resp.status_code == 200
    assert resp.data["username"] == user.username


class AuthenticationTests(APITestSetup):
    """Test authentication endpoints"""

    def test_user_login(self):
        """Test user login endpoint"""
        url = reverse("api_token_auth")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
