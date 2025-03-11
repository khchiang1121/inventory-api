from uuid import UUID
from datetime import datetime
from typing import Optional
from ninja import Schema, Field

# -----------------------
# Maintainer Schemas
# -----------------------

class MaintainerSchemaIn(Schema):
    name: str
    email: Optional[str] = Field(examples=['user@example.com'])
    status: str

class MaintainerSchemaOut(Schema):
    id: UUID
    name: str
    email: Optional[str] = Field(examples=['user@example.com'])
    status: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# MaintainerGroup Schemas
# -----------------------

class MaintainerGroupSchemaIn(Schema):
    name: str
    group_manager: UUID  # Provide the manager's UUID in request.
    description: Optional[str] = None
    status: str

class MaintainerGroupSchemaOut(Schema):
    id: UUID
    name: str
    group_manager: MaintainerSchemaOut  # Nested maintainer details.
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# MaintainerGroupMember Schemas
# -----------------------

class MaintainerGroupMemberSchemaIn(Schema):
    group: UUID
    maintainer: UUID

class MaintainerGroupMemberSchemaOut(Schema):
    id: UUID
    group: MaintainerGroupSchemaOut
    maintainer: MaintainerSchemaOut
    created_at: datetime
    updated_at: datetime


# -----------------------
# ResourceMaintainer Schemas
# -----------------------

class ResourceMaintainerSchemaIn(Schema):
    resource_type: str
    resource_id: UUID
    maintainer_type: str  # "individual" or "group"
    maintainer_id: UUID

class ResourceMaintainerSchemaOut(Schema):
    id: UUID
    resource_type: str
    resource_id: UUID
    maintainer_type: str
    maintainer_id: UUID
    created_at: datetime
    updated_at: datetime


# -----------------------
# HostGroup Schemas
# -----------------------

class HostGroupSchemaIn(Schema):
    name: str
    description: Optional[str] = None
    status: str

class HostGroupSchemaOut(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

class HostResourceSchemaOut(Schema):
    id: str
    name: str
    total_cpu: int
    available_cpu: int
    used_cpu: int
    total_memory: int
    available_memory: int
    used_memory: int
    total_storage: int
    available_storage: int
    used_storage: int
# -----------------------
# Host Schemas
# -----------------------

class HostSchemaIn(Schema):
    name: str
    status: str
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    group: UUID  # Provide HostGroup UUID
    region: str
    dc: str
    room: str
    rack: str
    unit: Optional[str] = None
    old_system_id: str

class HostSchemaOut(Schema):
    id: UUID
    name: str
    status: str
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    group: HostGroupSchemaOut  # Nested host group details.
    region: str
    dc: str
    room: str
    rack: str
    unit: Optional[str] = None
    old_system_id: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# Tenant Schemas
# -----------------------

class TenantSchemaIn(Schema):
    name: str
    description: Optional[str] = None
    status: str

class TenantSchemaOut(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# VirtualMachineSpecification Schemas
# -----------------------

class VirtualMachineSpecificationSchemaIn(Schema):
    name: str
    required_cpu: int
    required_memory: int
    required_storage: int

class VirtualMachineSpecificationSchemaOut(Schema):
    id: UUID
    name: str
    required_cpu: int
    required_memory: int
    required_storage: int
    created_at: datetime
    updated_at: datetime


# -----------------------
# K8sCluster Schemas
# -----------------------

class K8sClusterSchemaIn(Schema):
    name: str
    tenant: UUID  # Provide tenant's UUID.
    description: Optional[str] = None
    status: str

class K8sClusterSchemaOut(Schema):
    id: UUID
    name: str
    tenant: TenantSchemaOut  # Nested tenant details.
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# VirtualMachine Schemas
# -----------------------
# Note: The ForeignKey "specification" refers to VirtualMachineSpecification.

class VirtualMachineSchemaIn(Schema):
    name: str
    tenant: UUID  # Tenant's UUID.
    host: UUID    # Host's UUID.
    specification: UUID  # VirtualMachineSpecification UUID.
    k8s_cluster: Optional[UUID] = None  # Optional cluster association.
    status: str

class VirtualMachineSchemaOut(Schema):
    id: UUID
    name: str
    tenant: TenantSchemaOut
    host: HostSchemaOut
    specification: VirtualMachineSpecificationSchemaOut
    k8s_cluster: Optional[K8sClusterSchemaOut] = None
    status: str
    created_at: datetime
    updated_at: datetime


# -----------------------
# HostGroupTenantQuota Schemas
# -----------------------

class HostGroupTenantQuotaSchemaIn(Schema):
    group: UUID  # HostGroup UUID.
    tenant: UUID  # Tenant UUID.
    cpu_quota_percentage: float
    memory_quota: int
    storage_quota: int

class HostGroupTenantQuotaSchemaOut(Schema):
    id: UUID
    group: HostGroupSchemaOut
    tenant: TenantSchemaOut
    cpu_quota_percentage: float
    memory_quota: int
    storage_quota: int
    created_at: datetime
    updated_at: datetime
