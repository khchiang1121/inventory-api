from typing import Any, Optional, Tuple

from django.conf import settings

from rest_framework.authentication import TokenAuthentication

# class CustomTokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return None
#
#         token = auth_header.split(' ')[1]
#         if token == os.environ.get("DJANGO_BACKDOOR_API_TOKEN"):
#             return (None, token)
#         raise AuthenticationFailed('Invalid or missing API token')

#     def authenticate_header(self, request):
#         return 'Bearer'

# class TokenPermission(BasePermission):
#     def has_permission(self, request, view):
#         return request.auth is not None

# # Default permission classes for all views
# DEFAULT_PERMISSION_CLASSES = [TokenPermission]
# DEFAULT_AUTHENTICATION_CLASSES = [CustomTokenAuthentication]


class ConditionalTokenAuthentication(TokenAuthentication):
    """
    Token authentication that can be disabled via settings.
    When REQUIRE_API_AUTHENTICATION is False, this authentication class
    will not require authentication and will allow anonymous access.
    """

    def authenticate(self, request):
        # If authentication is not required, skip token authentication
        if not getattr(settings, "REQUIRE_API_AUTHENTICATION", True):
            return None

        # Otherwise, use the standard token authentication
        return super().authenticate(request)


# class HasPermissionForObject(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # 如果有 owner 欄位，且是 owner
#         if hasattr(obj, 'owner') and obj.owner == request.user:
#             return True
#         app_label = obj._meta.app_label
#         model_name = obj._meta.model_name

#         # 自動對應 HTTP method -> 權限
#         perm_map = {
#             'GET': f'{app_label}.view_{model_name}',
#             'OPTIONS': f'{app_label}.view_{model_name}',
#             'HEAD': f'{app_label}.view_{model_name}',
#             'POST': f'{app_label}.add_{model_name}',
#             'PUT': f'{app_label}.change_{model_name}',
#             'PATCH': f'{app_label}.change_{model_name}',
#             'DELETE': f'{app_label}.delete_{model_name}',
#         }

#         perm = perm_map.get(request.method)

#         if perm:
#             return request.user.has_perm(perm, obj)

#         return False
