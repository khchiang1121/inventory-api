import pytest

from .base import auth_client


@pytest.mark.django_db
def test_health_check_open(auth_client):
    r = auth_client.get("/health/")
    # health is AllowAny; returns 200 with system info
    assert r.status_code in (200, 503)
    assert "timestamp" in r.data


@pytest.mark.django_db
def test_schema_endpoints(auth_client):
    assert auth_client.get("/api/v1/schema/json/").status_code == 200
    assert auth_client.get("/api/v1/schema/yaml/").status_code == 200

    # Swagger/Redoc UIs
    assert auth_client.get("/api/v1/swagger-ui").status_code in (200, 301, 302)
    assert auth_client.get("/api/v1/redoc").status_code in (200, 301, 302)
