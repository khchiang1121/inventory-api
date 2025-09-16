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
    Manufacturer,
    Supplier,
    Tenant,
)
from .base import AbstractBase
from .infrastructure import DataCenter, Fabrication, Phase, Rack, Room
from .network import VLAN, VRF, BGPConfig, NetworkInterface
from .purchase import PurchaseOrder, PurchaseRequisition
from .users import CustomUser
from .virtual import (
    BastionClusterAssociation,
    K8sCluster,
    K8sClusterPlugin,
    K8sClusterToServiceMesh,
    ServiceMesh,
    VirtualMachine,
    VirtualMachineSpecification,
)

# Export all models
__all__ = [
    # Base
    "AbstractBase",
    # Users
    "CustomUser",
    # Infrastructure
    "Fabrication",
    "Phase",
    "DataCenter",
    "Room",
    "Rack",
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
    "Baremetal",
    "Tenant",
    "BaremetalGroupTenantQuota",
    # Virtual
    "VirtualMachineSpecification",
    "K8sCluster",
    "K8sClusterPlugin",
    "ServiceMesh",
    "K8sClusterToServiceMesh",
    "VirtualMachine",
    "BastionClusterAssociation",
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
