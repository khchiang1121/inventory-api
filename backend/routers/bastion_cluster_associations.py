from uuid import UUID
from ninja import Router
from backend import schemas
from backend import models
from backend.dependencies import api_auth
from django.shortcuts import get_object_or_404

# ----------------------------
# BastionClusterAssociation Router
# ----------------------------
bastion_cluster_association_router = Router(tags=["BastionClusterAssociation"], auth=api_auth)

@bastion_cluster_association_router.get("/", response=list[schemas.BastionClusterAssociationOutSchema])
def list_bastion_cluster_associations(request):
    return models.BastionClusterAssociation.objects.all()

@bastion_cluster_association_router.get("/{association_id}", response=schemas.BastionClusterAssociationOutSchema)
def get_bastion_cluster_association(request, association_id: UUID):
    return get_object_or_404(models.BastionClusterAssociation, id=association_id)

@bastion_cluster_association_router.post("/", response=schemas.BastionClusterAssociationOutSchema)
def create_bastion_cluster_association(request, payload: schemas.BastionClusterAssociationCreateSchema):
    association = models.BastionClusterAssociation.objects.create(**payload.dict())
    return association

@bastion_cluster_association_router.put("/{association_id}", response=schemas.BastionClusterAssociationOutSchema)
def update_bastion_cluster_association(request, association_id: UUID, payload: schemas.BastionClusterAssociationUpdateSchema):
    association = get_object_or_404(models.BastionClusterAssociation, id=association_id)
    for attr, value in payload.dict().items():
        setattr(association, attr, value)
    association.save()
    return association

@bastion_cluster_association_router.delete("/{association_id}")
def delete_bastion_cluster_association(request, association_id: UUID):
    association = get_object_or_404(models.BastionClusterAssociation, id=association_id)
    association.delete()
    return {"success": True}
