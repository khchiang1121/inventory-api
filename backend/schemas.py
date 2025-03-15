from uuid import UUID
from datetime import datetime
from typing import Optional
from ninja import Schema, Field

# =============================================================================
# Maintainer Schemas
# =============================================================================

class MaintainerCreateSchema(Schema):
    name: str
    account: str  # new field in model
    email: Optional[str] = Field(None, examples=["user@example.com"])
    status: str

class MaintainerUpdateSchema(Schema):
    name: Optional[str] = None
    account: Optional[str] = None
    email: Optional[str] = Field(None, examples=["user@example.com"])
    status: Optional[str] = None

class MaintainerOutSchema(Schema):
    id: UUID
    name: str
    account: str
    email: Optional[str] = Field(None, examples=["user@example.com"])
    status: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Maintainer Group Schemas
# =============================================================================

class MaintainerGroupCreateSchema(Schema):
    name: str
    group_manager: UUID  # manager's UUID
    description: Optional[str] = None
    status: str

class MaintainerGroupUpdateSchema(Schema):
    name: Optional[str] = None
    group_manager: Optional[UUID] = None
    description: Optional[str] = None
    status: Optional[str] = None

class MaintainerGroupOutSchema(Schema):
    id: UUID
    name: str
    group_manager: MaintainerOutSchema  # nested maintainer details
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Maintainer Group Member (Through Model) Schemas
# =============================================================================

class MaintainerToMaintainerGroupCreateSchema(Schema):
    maintainer_group: UUID
    maintainer: UUID

class MaintainerToMaintainerGroupUpdateSchema(Schema):
    maintainer_group: Optional[UUID] = None
    maintainer: Optional[UUID] = None

class MaintainerToMaintainerGroupOutSchema(Schema):
    id: UUID
    maintainer_group: MaintainerGroupOutSchema
    maintainer: MaintainerOutSchema
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Resource Maintainer Schemas
# =============================================================================

class ResourceMaintainerCreateSchema(Schema):
    resource_type: str
    resource_id: UUID
    maintainer_type: str  # allowed: "maintainer" or "maintainer_group"
    maintainer_id: UUID

class ResourceMaintainerUpdateSchema(Schema):
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    maintainer_type: Optional[str] = None
    maintainer_id: Optional[UUID] = None

class ResourceMaintainerOutSchema(Schema):
    id: UUID
    resource_type: str
    resource_id: UUID
    maintainer_type: str
    maintainer_id: UUID
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Rack Schemas (for Baremetal placement)
# =============================================================================

class RackCreateSchema(Schema):
    name: str
    bgp_number: str
    as_number: str
    old_system_id: Optional[str] = None

class RackUpdateSchema(Schema):
    name: Optional[str] = None
    bgp_number: Optional[str] = None
    as_number: Optional[str] = None
    old_system_id: Optional[str] = None

class RackOutSchema(Schema):
    id: UUID
    name: str
    bgp_number: str
    as_number: str
    old_system_id: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Baremetal Group Schemas (replacing HostGroup)
# =============================================================================

class BaremetalGroupCreateSchema(Schema):
    name: str
    description: Optional[str] = None
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    status: str

class BaremetalGroupUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    total_cpu: Optional[int] = None
    total_memory: Optional[int] = None
    total_storage: Optional[int] = None
    available_cpu: Optional[int] = None
    available_memory: Optional[int] = None
    available_storage: Optional[int] = None
    status: Optional[str] = None

class BaremetalGroupOutSchema(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    status: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Baremetal Schemas (replacing Host)
# =============================================================================

class BaremetalCreateSchema(Schema):
    name: str
    serial_number: str
    region: str
    fab: str
    phase: str
    dc: str
    room: str
    rack: UUID  # reference to Rack
    unit: Optional[str] = None
    status: str
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    group: UUID  # reference to BaremetalGroup
    old_system_id: str

class BaremetalUpdateSchema(Schema):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    region: Optional[str] = None
    fab: Optional[str] = None
    phase: Optional[str] = None
    dc: Optional[str] = None
    room: Optional[str] = None
    rack: Optional[UUID] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    total_cpu: Optional[int] = None
    total_memory: Optional[int] = None
    total_storage: Optional[int] = None
    available_cpu: Optional[int] = None
    available_memory: Optional[int] = None
    available_storage: Optional[int] = None
    group: Optional[UUID] = None
    old_system_id: Optional[str] = None

class BaremetalOutSchema(Schema):
    id: UUID
    name: str
    serial_number: str
    region: str
    fab: str
    phase: str
    dc: str
    room: str
    rack: RackOutSchema  # nested rack details
    unit: Optional[str] = None
    status: str
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    group: BaremetalGroupOutSchema  # nested group details
    old_system_id: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Baremetal Group Tenant Quota Schemas
# =============================================================================

class BaremetalGroupTenantQuotaCreateSchema(Schema):
    """
    Schema for creating a Baremetal Group Tenant Quota.
    """
    group: UUID 
    tenant: UUID
    cpu_quota_percentage: float
    memory_quota: int
    storage_quota: int

class BaremetalGroupTenantQuotaUpdateSchema(Schema):
    """
    Schema for updating a Baremetal Group Tenant Quota.
    """
    group: Optional[UUID]
    tenant: Optional[UUID]
    cpu_quota_percentage: Optional[float]
    memory_quota: Optional[int]
    storage_quota: Optional[int]

class BaremetalGroupTenantQuotaOutSchema(Schema):
    """
    Schema for outputting a Baremetal Group Tenant Quota.
    """
    id: UUID
    group: UUID 
    tenant: UUID
    cpu_quota_percentage: float
    memory_quota: int
    storage_quota: int
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Tenant Schemas
# =============================================================================

class TenantCreateSchema(Schema):
    name: str
    description: Optional[str] = None
    status: str

class TenantUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TenantOutSchema(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Virtual Machine Specification Schemas
# =============================================================================

class VirtualMachineSpecificationCreateSchema(Schema):
    name: str
    generation: str
    required_cpu: int
    required_memory: int
    required_storage: int

class VirtualMachineSpecificationUpdateSchema(Schema):
    name: Optional[str] = None
    generation: Optional[str] = None
    required_cpu: Optional[int] = None
    required_memory: Optional[int] = None
    required_storage: Optional[int] = None

class VirtualMachineSpecificationOutSchema(Schema):
    id: UUID
    name: str
    generation: str
    required_cpu: int
    required_memory: int
    required_storage: int
    created_at: datetime
    updated_at: datetime

# =============================================================================
# K8s Cluster Schemas
# =============================================================================

class K8sClusterCreateSchema(Schema):
    name: str
    version: str
    tenant: UUID  # tenant's UUID
    description: Optional[str] = None
    status: str

class K8sClusterUpdateSchema(Schema):
    name: Optional[str] = None
    version: Optional[str] = None
    tenant: Optional[UUID] = None
    description: Optional[str] = None
    status: Optional[str] = None

class K8sClusterOutSchema(Schema):
    id: UUID
    name: str
    version: str
    tenant: TenantOutSchema  # nested tenant details
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

from uuid import UUID
from datetime import datetime
from typing import Optional
from ninja import Schema, Field


# =============================================================================
# K8sClusterPlugin Schemas
# =============================================================================

class K8sClusterPluginCreateSchema(Schema):
    cluster: UUID
    name: str
    version: str
    status: str
    additional_info: Optional[dict] = None


class K8sClusterPluginUpdateSchema(Schema):
    cluster: Optional[UUID] = None
    name: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    additional_info: Optional[dict] = None


class K8sClusterPluginOutSchema(Schema):
    id: UUID
    cluster: UUID
    name: str
    version: str
    status: str
    additional_info: Optional[dict] = None
    created_at: datetime
    updated_at: datetime


# =============================================================================
# BastionClusterAssociation Schemas
# =============================================================================

class BastionClusterAssociationCreateSchema(Schema):
    bastion: UUID
    k8s_cluster: UUID

class BastionClusterAssociationUpdateSchema(Schema):
    bastion: Optional[UUID] = None
    k8s_cluster: Optional[UUID] = None

class BastionClusterAssociationOutSchema(Schema):
    id: UUID
    bastion: UUID
    k8s_cluster: UUID
    created_at: datetime
    updated_at: datetime

# =============================================================================
# K8sClusterToServiceMesh Schemas
# =============================================================================

class K8sClusterToServiceMeshCreateSchema(Schema):
    cluster: UUID
    service_mesh: UUID
    role: str

class K8sClusterToServiceMeshUpdateSchema(Schema):
    cluster: Optional[UUID] = None
    service_mesh: Optional[UUID] = None
    role: Optional[str] = None

class K8sClusterToServiceMeshOutSchema(Schema):
    id: UUID
    cluster: UUID
    service_mesh: UUID
    role: str
    created_at: datetime
    updated_at: datetime


# =============================================================================
# ServiceMesh Schemas
# =============================================================================

class ServiceMeshCreateSchema(Schema):
    name: str
    type: str
    description: Optional[str] = None
    status: str


class ServiceMeshUpdateSchema(Schema):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ServiceMeshOutSchema(Schema):
    id: UUID
    name: str
    type: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

# =============================================================================
# Virtual Machine Schemas
# =============================================================================

class VirtualMachineCreateSchema(Schema):
    name: str
    tenant: UUID
    baremetal: UUID  # now references a Baremetal server
    specification: UUID
    k8s_cluster: Optional[UUID] = None
    type: str  # e.g., "control-plane", "worker", "management", "other"
    status: str

class VirtualMachineUpdateSchema(Schema):
    name: Optional[str] = None
    tenant: Optional[UUID] = None
    baremetal: Optional[UUID] = None
    specification: Optional[UUID] = None
    k8s_cluster: Optional[UUID] = None
    type: Optional[str] = None
    status: Optional[str] = None

class VirtualMachineOutSchema(Schema):
    id: UUID
    name: str
    tenant: TenantOutSchema
    baremetal: BaremetalOutSchema
    specification: VirtualMachineSpecificationOutSchema
    k8s_cluster: Optional[K8sClusterOutSchema] = None
    type: str
    status: str
    created_at: datetime
    updated_at: datetime

