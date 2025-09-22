# Import all models to maintain backward compatibility
from .ansible import (
    AnsibleGroup,
    AnsibleGroupRelationship,
    AnsibleGroupVariable,
    AnsibleHost,
    AnsibleHostVariable,
    AnsibleInventory,
    AnsibleInventoryPlugin,
    AnsibleInventoryTemplate,
    AnsibleInventoryVariable,
    AnsibleInventoryVariableSetAssociation,
    AnsibleVariableSet,
)
from .baremetal import (
    Baremetal,
    BaremetalGroup,
    BaremetalGroupTenantQuota,
    BaremetalModel,
    BaremetalModelGPU,
    Manufacturer,
    Supplier,
)
from .base import AbstractBase
from .infrastructure import AvailableGroup, DataCenter, Fab, Phase, Rack, Room, Unit
from .network import VLAN, VRF, BGPConfig, NetworkInterface
from .purchase import PurchaseOrder, PurchaseRequisition
from .scheduling_strategy import SchedulingStrategy, SchedulingStrategyCondition
from .users import CustomUser
from .virtual import (
    BastionClusterAssociation,
    K8sCluster,
    K8sClusterPlugin,
    K8sClusterToServiceMesh,
    PhysicalGPU,
    PhysicalGPUModel,
    Region,
    ServiceMesh,
    Tenant,
    VirtualMachine,
    VirtualMachineSpecification,
    VirtualMachineSpecificationGPU,
)

# Export all models
__all__ = [
    # Base
    "AbstractBase",
    # Users
    "CustomUser",
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
    # Baremetal
    "BaremetalGroup",
    "Manufacturer",
    "Supplier",
    "BaremetalModel",
    "BaremetalModelGPU",
    "Baremetal",
    "BaremetalGroupTenantQuota",
    # Virtual
    "Tenant",
    "Region",
    "PhysicalGPUModel",
    "PhysicalGPU",
    "VirtualMachineSpecification",
    "VirtualMachineSpecificationGPU",
    "K8sCluster",
    "K8sClusterPlugin",
    "ServiceMesh",
    "K8sClusterToServiceMesh",
    "VirtualMachine",
    "BastionClusterAssociation",
    # Scheduling
    "SchedulingStrategy",
    "SchedulingStrategyCondition",
    # Ansible
    "AnsibleInventory",
    "AnsibleInventoryVariable",
    "AnsibleVariableSet",
    "AnsibleGroup",
    "AnsibleGroupVariable",
    "AnsibleGroupRelationship",
    "AnsibleHost",
    "AnsibleHostVariable",
    "AnsibleInventoryPlugin",
    "AnsibleInventoryTemplate",
    "AnsibleInventoryVariableSetAssociation",
]
