import os
from typing import Any, List, Optional, Type, cast

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.shortcuts import get_object_or_404

from guardian.models import Group
from guardian.shortcuts import (
    assign_perm,
    get_objects_for_group,
    get_objects_for_user,
    remove_perm,
)
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import ObjectPermissionSerializer


class ObjectPermissionViewSet(viewsets.ViewSet):
    """
    ViewSet for managing object-level permissions.
    """

    serializer_class = ObjectPermissionSerializer

    def get_object(self, model: Type[Model], object_id: str) -> Model:
        """Helper method to get object by model and id."""
        content_type = ContentType.objects.get_for_model(model)
        return get_object_or_404(model, id=object_id)

    def get_model_class(self, model_name: str) -> Type[Model]:
        """Helper method to get model class from model name."""
        app_label, model = model_name.split(".")
        model_class = ContentType.objects.get(
            app_label=app_label, model=model
        ).model_class()
        if model_class is None:
            raise ValueError(f"Could not find model class for {model_name}")
        return cast(Type[Model], model_class)

    @action(detail=False, methods=["POST"])
    def assign_user_permission(self, request: Request) -> Response:
        """
        Assign permission to a user for a specific object.

        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        serializer = ObjectPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = self.get_model_class(serializer.validated_data["model_name"])
            obj = self.get_object(model, serializer.validated_data["object_id"])
            user = get_object_or_404(
                get_user_model(), id=serializer.validated_data["user_id"]
            )

            assign_perm(serializer.validated_data["permission"], user, obj)
            return Response({"status": "Permission assigned"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def assign_group_permission(self, request: Request) -> Response:
        """
        Assign permission to a group for a specific object.

        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        serializer = ObjectPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = self.get_model_class(serializer.validated_data["model_name"])
            obj = self.get_object(model, serializer.validated_data["object_id"])
            group = get_object_or_404(Group, id=serializer.validated_data["group_id"])

            assign_perm(serializer.validated_data["permission"], group, obj)
            return Response({"status": "Permission assigned"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def remove_user_permission(self, request: Request) -> Response:
        """
        Remove permission from a user for a specific object.

        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        serializer = ObjectPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = self.get_model_class(serializer.validated_data["model_name"])
            obj = self.get_object(model, serializer.validated_data["object_id"])
            user = get_object_or_404(
                get_user_model(), id=serializer.validated_data["user_id"]
            )

            remove_perm(serializer.validated_data["permission"], user, obj)
            return Response({"status": "Permission removed"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def remove_group_permission(self, request: Request) -> Response:
        """
        Remove permission from a group for a specific object.

        Required data:
        - model_name: string (e.g., 'api.tenant')
        - object_id: UUID
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        serializer = ObjectPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = self.get_model_class(serializer.validated_data["model_name"])
            obj = self.get_object(model, serializer.validated_data["object_id"])
            group = get_object_or_404(Group, id=serializer.validated_data["group_id"])

            remove_perm(serializer.validated_data["permission"], group, obj)
            return Response({"status": "Permission removed"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_user_objects(self, request: Request) -> Response:
        """
        Get all objects of a model that a user has specific permission for.

        Required query params:
        - model_name: string (e.g., 'api.tenant')
        - user_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = self.get_model_class(request.query_params["model_name"])
            user = get_object_or_404(
                get_user_model(), id=request.query_params["user_id"]
            )

            objects = get_objects_for_user(
                user, request.query_params["permission"], model
            )
            return Response({"objects": [str(obj.id) for obj in objects]})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_group_objects(self, request: Request) -> Response:
        """
        Get all objects of a model that a group has specific permission for.

        Required query params:
        - model_name: string (e.g., 'api.tenant')
        - group_id: UUID
        - permission: string (e.g., 'view_tenant')
        """
        try:
            model = self.get_model_class(request.query_params["model_name"])
            group = get_object_or_404(Group, id=request.query_params["group_id"])

            objects = get_objects_for_group(
                group, request.query_params["permission"], model
            )
            return Response({"objects": [str(obj.id) for obj in objects]})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
