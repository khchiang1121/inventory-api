# Import all models to maintain backward compatibility
from .ansible import (
    AnsibleGroup,
    AnsibleGroupRelationship,
    AnsibleGroupVariable,
    AnsibleHost,
    AnsibleHostVariable,
    AnsibleInventory,
    AnsibleInventoryTemplate,
    AnsibleInventoryVariableSetAssociation,
    AnsibleVariableSet,
)
from .baremetal import (
    Baremetal,
    BaremetalGroup,
    BaremetalGroupTenantQuota,
    BaremetalModel,
    BaremetalModelGPU,
    GPUAllocation,
)
from .base import AbstractBase
from .common import Region, Tenant, Vendor
from .gpu import GPUProfile, PhysicalGPU, PhysicalGPUModel
from .infrastructure import AvailableGroup, DataCenter, Fab, Phase, Rack, Room, Unit
from .network import VLAN, VRF, BGPConfig, NetworkInterface
from .purchase import PurchaseOrder, PurchaseRequisition
from .scheduling_strategy import SchedulingStrategy, SchedulingStrategyModel
from .users import CustomGroup, CustomUser
from .virtual import (
    BastionClusterAssociation,
    ClusterTemplate,
    ClusterTemplateVirtualMachine,
    K8sCluster,
    K8sClusterPlugin,
    K8sClusterPluginAssociation,
    K8sClusterToServiceMesh,
    ServiceMesh,
    VirtualMachine,
    VirtualMachineRole,
    VirtualMachineSpecification,
    VirtualMachineSpecificationRequiredGPU,
)

# Export all models
__all__ = [
    # Base
    "AbstractBase",
    # Users
    "CustomUser",
    "CustomGroup",
    # Infrastructure
    "AvailableGroup",
    "Fab",
    "Phase",
    "DataCenter",
    "Room",
    "Rack",
    "Unit",
    # Network
    "VLAN",
    "VRF",
    "BGPConfig",
    "NetworkInterface",
    # Purchase
    "PurchaseRequisition",
    "PurchaseOrder",
    # Common (shared models)
    "Vendor",
    "Region",
    "Tenant",
    "VirtualMachine",
    # Baremetal
    "BaremetalGroup",
    "BaremetalModel",
    "BaremetalModelGPU",
    "Baremetal",
    "BaremetalGroupTenantQuota",
    "GPUAllocation",
    "GPUProfile",
    "PhysicalGPU",
    "PhysicalGPUModel",
    # Virtual
    "VirtualMachine",
    "VirtualMachineSpecification",
    "VirtualMachineSpecificationRequiredGPU",
    "K8sCluster",
    "K8sClusterPlugin",
    "K8sClusterPluginAssociation",
    "ServiceMesh",
    "K8sClusterToServiceMesh",
    "BastionClusterAssociation",
    "ClusterTemplate",
    "ClusterTemplateVirtualMachine",
    "VirtualMachineRole",
    # Scheduling
    "SchedulingStrategy",
    "SchedulingStrategyModel",
    # Ansible
    "AnsibleInventory",
    "AnsibleVariableSet",
    "AnsibleGroup",
    "AnsibleGroupVariable",
    "AnsibleGroupRelationship",
    "AnsibleHost",
    "AnsibleHostVariable",
    "AnsibleInventoryTemplate",
    "AnsibleInventoryVariableSetAssociation",
]
