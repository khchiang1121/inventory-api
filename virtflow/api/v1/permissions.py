from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user, get_objects_for_group
from guardian.models import Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import os

class ObjectPermissionViewSet(viewsets.ViewSet):
    """
    ViewSet for managing object-level permissions.
    """
    
    def get_object(self, model, object_id):
        """Helper method to get object by model and id."""
        content_type = ContentType.objects.get_for_model(model)
        return get_object_or_404(model, id=object_id)

    @action(detail=False, methods=['POST'])
    def assign_user_permission(self, request):
        """
        Assign permission to a user for a specific object.
        
        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.data['model_name'].split('.')[0],
                model=request.data['model_name'].split('.')[1]
            ).model_class()
            obj = self.get_object(model, request.data['object_id'])
            user = get_object_or_404(get_user_model(), id=request.data['user_id'])
            
            assign_perm(request.data['permission'], user, obj)
            return Response({'status': 'Permission assigned'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def assign_group_permission(self, request):
        """
        Assign permission to a group for a specific object.
        
        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.data['model_name'].split('.')[0],
                model=request.data['model_name'].split('.')[1]
            ).model_class()
            obj = self.get_object(model, request.data['object_id'])
            group = get_object_or_404(Group, id=request.data['group_id'])
            
            assign_perm(request.data['permission'], group, obj)
            return Response({'status': 'Permission assigned'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def remove_user_permission(self, request):
        """
        Remove permission from a user for a specific object.
        
        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.data['model_name'].split('.')[0],
                model=request.data['model_name'].split('.')[1]
            ).model_class()
            obj = self.get_object(model, request.data['object_id'])
            user = get_object_or_404(get_user_model(), id=request.data['user_id'])
            
            remove_perm(request.data['permission'], user, obj)
            return Response({'status': 'Permission removed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def remove_group_permission(self, request):
        """
        Remove permission from a group for a specific object.
        
        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.data['model_name'].split('.')[0],
                model=request.data['model_name'].split('.')[1]
            ).model_class()
            obj = self.get_object(model, request.data['object_id'])
            group = get_object_or_404(Group, id=request.data['group_id'])
            
            remove_perm(request.data['permission'], group, obj)
            return Response({'status': 'Permission removed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_user_objects(self, request):
        """
        Get all objects of a model that a user has specific permission for.
        
        Required query params:
        - model_name: string (e.g., 'api.tenant')
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.query_params['model_name'].split('.')[0],
                model=request.query_params['model_name'].split('.')[1]
            ).model_class()
            user = get_object_or_404(get_user_model(), id=request.query_params['user_id'])
            
            objects = get_objects_for_user(user, request.query_params['permission'], model)
            # You might want to serialize the objects here
            return Response({'objects': [str(obj.id) for obj in objects]})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_group_objects(self, request):
        """
        Get all objects of a model that a group has specific permission for.
        
        Required query params:
        - model_name: string (e.g., 'api.tenant')
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = ContentType.objects.get(
                app_label=request.query_params['model_name'].split('.')[0],
                model=request.query_params['model_name'].split('.')[1]
            ).model_class()
            group = get_object_or_404(Group, id=request.query_params['group_id'])
            
            objects = get_objects_for_group(group, request.query_params['permission'], model)
            # You might want to serialize the objects here
            return Response({'objects': [str(obj.id) for obj in objects]})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 