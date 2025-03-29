from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import os

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        if token == os.environ.get("DJANGO_API_TOKEN"):
            return (None, token)
        raise AuthenticationFailed('Invalid or missing API token')

    def authenticate_header(self, request):
        return 'Bearer'

class TokenPermission(BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None

# Default permission classes for all views
DEFAULT_PERMISSION_CLASSES = [TokenPermission]
DEFAULT_AUTHENTICATION_CLASSES = [CustomTokenAuthentication] 
