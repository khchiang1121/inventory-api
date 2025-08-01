"""
URL configuration for virtflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from virtflow import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView, SpectacularYAMLAPIView, RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from virtflow.api.v1.serializers import CustomUserSerializer
from rest_framework.request import Request
from django.db import connection
from django.core.cache import cache
import psutil
import time

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request: Request) -> Response:
    """Get current user information"""
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request: Request) -> Response:
    """Logout current user"""
    # In a real implementation, you might want to invalidate the token
    # For now, we'll just return a success response
    return Response({'message': 'Successfully logged out'})

@api_view(['POST'])
def refresh_view(request: Request) -> Response:
    """Refresh authentication token"""
    # For now, we'll return a mock response
    # In a real implementation, you'd validate the refresh token and issue a new access token
    return Response({'access': 'new-access-token'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request: Request) -> Response:
    """Change user password"""
    # For now, we'll return a success response
    # In a real implementation, you'd validate the old password and update to the new password
    return Response({'message': 'Password changed successfully'})

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    try:
        # Check database connection
        database_status = 'healthy'
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            database_status = 'unhealthy'
        
        # Check cache connection (if available)
        cache_status = 'healthy'
        try:
            cache.set('health_check', 'ok', 1)
            if cache.get('health_check') != 'ok':
                cache_status = 'unhealthy'
        except Exception:
            cache_status = 'unhealthy'
        
        # Get basic system info
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data = {
            'status': 'healthy' if database_status == 'healthy' else 'unhealthy',
            'timestamp': time.time(),
            'database': database_status,
            'cache': cache_status,
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'free': disk.free,
                'percent': disk.percent
            }
        }
        
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return Response(health_data, status=status_code)
        
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }, status=503)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Schema
    path("api/v1/schema/json/", SpectacularJSONAPIView.as_view(), name="json"),
    path("api/v1/schema/yaml/", SpectacularYAMLAPIView.as_view(), name="yaml"),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger-ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=False)),
    # path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/auth/login/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/auth/logout/', logout_view, name='auth_logout'),
    path('api/v1/auth/refresh/', refresh_view, name='auth_refresh'),
    path('api/v1/auth/change-password/', change_password_view, name='auth_change_password'),
    path('api/v1/auth/me/', me_view, name='auth_me'),
    # Health check endpoint
    path('health/', health_check, name='health_check'),
    # add a me path to the api
    re_path(r'^api/v1/', include(('virtflow.api.v1.urls'), namespace='v1')),

] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
