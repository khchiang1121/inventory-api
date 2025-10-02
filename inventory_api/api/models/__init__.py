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

__all__ = [
    # Ansible
    "AnsibleGroup",
    "AnsibleGroupRelationship",
    "AnsibleGroupVariable",
    "AnsibleHost",
    "AnsibleHostVariable",
    "AnsibleInventory",
    "AnsibleInventoryTemplate",
    "AnsibleInventoryVariableSetAssociation",
    "AnsibleVariableSet",
    # Baremetal
    "Baremetal",
    "BaremetalGroup",
    "BaremetalGroupTenantQuota",
    "BaremetalModel",
    "BaremetalModelGPU",
    "GPUAllocation",
    # Base
    "AbstractBase",
    # Common (shared models)
    "Region",
    "Tenant",
    "Vendor",
    # GPU
    "GPUProfile",
    "PhysicalGPU",
    "PhysicalGPUModel",
    # Infrastructure
    "AvailableGroup",
    "DataCenter",
    "Fab",
    "Phase",
    "Rack",
    "Room",
    "Unit",
    # Network
    "VLAN",
    "VRF",
    "BGPConfig",
    "NetworkInterface",
    # Purchase
    "PurchaseOrder",
    "PurchaseRequisition",
    # Scheduling
    "SchedulingStrategy",
    "SchedulingStrategyModel",
    # Users
    "CustomGroup",
    "CustomUser",
    # Virtual
    "BastionClusterAssociation",
    "ClusterTemplate",
    "ClusterTemplateVirtualMachine",
    "K8sCluster",
    "K8sClusterPlugin",
    "K8sClusterPluginAssociation",
    "K8sClusterToServiceMesh",
    "ServiceMesh",
    "VirtualMachine",
    "VirtualMachineRole",
    "VirtualMachineSpecification",
    "VirtualMachineSpecificationRequiredGPU",
]
