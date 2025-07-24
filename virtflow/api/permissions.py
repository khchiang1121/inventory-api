from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import os
from rest_framework import permissions
from rest_framework.request import Request
from typing import Any
from django.contrib.auth import get_user_model

User = get_user_model()
class HasPermissionForObject(permissions.BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        # if not login, set the current user to the superuser
        if not request.user or not request.user.is_authenticated:
            request.user = User.objects.get(username='admin')
            return True
        return True

        # # Check if user is authenticated
        # if not request.user or not request.user.is_authenticated:
        #     return False
        # return True

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        # Check if user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 如果有 owner 欄位，且是 owner
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        # 自動對應 HTTP method -> 權限
        perm_map = {
            'GET': f'{app_label}.view_{model_name}',
            'OPTIONS': f'{app_label}.view_{model_name}',
            'HEAD': f'{app_label}.view_{model_name}',
            'POST': f'{app_label}.add_{model_name}',
            'PUT': f'{app_label}.change_{model_name}',
            'PATCH': f'{app_label}.change_{model_name}',
            'DELETE': f'{app_label}.delete_{model_name}',
        }

        perm = perm_map.get(request.method or '')

        if perm:
            return request.user.has_perm(perm, obj)

        return False


