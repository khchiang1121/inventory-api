# 🔍 Model/Endpoint 檢查清單

## 📋 說明
此清單包含系統中所有 Model 和對應的 API Endpoint，以及完整的 CRUD 操作。請逐一檢查每個項目，完成後在對應的 checkbox 打勾。

**格式說明：**
- ✅ **Model Name** (`/api/v1/endpoint-name`)
  - [ ] **Model** - 模型定義檢查
  - [ ] **Serializer** - 序列化器檢查
  - [ ] **View** - 視圖檢查
  - [ ] **C**reate (POST)
  - [ ] **R**ead List (GET)
  - [ ] **R**ead Detail (GET /:id)
  - [ ] **U**pdate (PUT/PATCH /:id)
  - [ ] **D**elete (DELETE /:id)

---

## 👤 **用戶管理 (User Management)**

### ✅ **CustomUser** (`/api/v1/users`)
- [ ] **Model** - CustomUser 模型定義檢查
- [ ] **Serializer** - CustomUserSerializer 檢查
- [ ] **View** - CustomUserViewSet 檢查
- [ ] **Create** - `POST /api/v1/users`
- [ ] **Read List** - `GET /api/v1/users`
- [ ] **Read Detail** - `GET /api/v1/users/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/users/:id`
- [ ] **Delete** - `DELETE /api/v1/users/:id`

---

## 🏗️ **基礎設施 (Infrastructure)**

### ✅ **Fab** (`/api/v1/fab`)
- [x] **Model** - Fab 模型定義檢查
- [x] **Serializer** - FabSerializer 檢查
- [x] **View** - FabViewSet 檢查
- [ ] **Create** - `POST /api/v1/fab`
- [ ] **Read List** - `GET /api/v1/fab`
- [ ] **Read Detail** - `GET /api/v1/fab/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/fab/:id`
- [ ] **Delete** - `DELETE /api/v1/fab/:id`

### ✅ **Phase** (`/api/v1/phases`)
- [ ] **Model** - Phase 模型定義檢查
- [ ] **Serializer** - PhaseSerializer 檢查
- [x] **View** - PhaseViewSet 檢查
- [ ] **Create** - `POST /api/v1/phases` (需要 fab_id)
- [ ] **Read List** - `GET /api/v1/phases`
- [ ] **Read Detail** - `GET /api/v1/phases/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/phases/:id`
- [ ] **Delete** - `DELETE /api/v1/phases/:id`

### ✅ **DataCenter** (`/api/v1/data-centers`)
- [ ] **Model** - DataCenter 模型定義檢查
- [ ] **Serializer** - DataCenterSerializer 檢查
- [x] **View** - DataCenterViewSet 檢查
- [ ] **Create** - `POST /api/v1/data-centers` (需要 phase_id)
- [ ] **Read List** - `GET /api/v1/data-centers`
- [ ] **Read Detail** - `GET /api/v1/data-centers/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/data-centers/:id`
- [ ] **Delete** - `DELETE /api/v1/data-centers/:id`

### ✅ **Room** (`/api/v1/rooms`)
- [ ] **Model** - Room 模型定義檢查
- [ ] **Serializer** - RoomSerializer 檢查
- [x] **View** - RoomViewSet 檢查
- [ ] **Create** - `POST /api/v1/rooms` (需要 datacenter_id)
- [ ] **Read List** - `GET /api/v1/rooms`
- [ ] **Read Detail** - `GET /api/v1/rooms/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/rooms/:id`
- [ ] **Delete** - `DELETE /api/v1/rooms/:id`

### ✅ **Rack** (`/api/v1/racks`)
- [ ] **Model** - Rack 模型定義檢查
- [ ] **Serializer** - RackSerializer 檢查
- [x] **View** - RackViewSet 檢查
- [ ] **Create** - `POST /api/v1/racks` (需要 room_id)
- [ ] **Read List** - `GET /api/v1/racks`
- [ ] **Read Detail** - `GET /api/v1/racks/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/racks/:id`
- [ ] **Delete** - `DELETE /api/v1/racks/:id`

### ✅ **Unit** (`/api/v1/units`)
- [ ] **Model** - Unit 模型定義檢查
- [ ] **Serializer** - UnitSerializer 檢查
- [x] **View** - UnitViewSet 檢查
- [ ] **Create** - `POST /api/v1/units` (需要 rack_id)
- [ ] **Read List** - `GET /api/v1/units`
- [ ] **Read Detail** - `GET /api/v1/units/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/units/:id`
- [ ] **Delete** - `DELETE /api/v1/units/:id`

---

## 🌐 **網路 (Network)**

### ✅ **VLAN** (`/api/v1/vlans`)
- [ ] **Model** - VLAN 模型定義檢查
- [ ] **Serializer** - VLANSerializer 檢查
- [ ] **View** - VLANViewSet 檢查
- [ ] **Create** - `POST /api/v1/vlans`
- [ ] **Read List** - `GET /api/v1/vlans`
- [ ] **Read Detail** - `GET /api/v1/vlans/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/vlans/:id`
- [ ] **Delete** - `DELETE /api/v1/vlans/:id`

### ✅ **VRF** (`/api/v1/vrfs`)
- [ ] **Model** - VRF 模型定義檢查
- [ ] **Serializer** - VRFSerializer 檢查
- [ ] **View** - VRFViewSet 檢查
- [ ] **Create** - `POST /api/v1/vrfs`
- [ ] **Read List** - `GET /api/v1/vrfs`
- [ ] **Read Detail** - `GET /api/v1/vrfs/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/vrfs/:id`
- [ ] **Delete** - `DELETE /api/v1/vrfs/:id`

### ✅ **BGPConfig** (`/api/v1/bgp-configs`)
- [ ] **Model** - BGPConfig 模型定義檢查
- [ ] **Serializer** - BGPConfigSerializer 檢查
- [ ] **View** - BGPConfigViewSet 檢查
- [ ] **Create** - `POST /api/v1/bgp-configs`
- [ ] **Read List** - `GET /api/v1/bgp-configs`
- [ ] **Read Detail** - `GET /api/v1/bgp-configs/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/bgp-configs/:id`
- [ ] **Delete** - `DELETE /api/v1/bgp-configs/:id`

### ✅ **NetworkInterface** (`/api/v1/network-interfaces`)
- [ ] **Model** - NetworkInterface 模型定義檢查
- [ ] **Serializer** - NetworkInterfaceSerializer 檢查
- [ ] **View** - NetworkInterfaceViewSet 檢查
- [ ] **Create** - `POST /api/v1/network-interfaces`
- [ ] **Read List** - `GET /api/v1/network-interfaces`
- [ ] **Read Detail** - `GET /api/v1/network-interfaces/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/network-interfaces/:id`
- [ ] **Delete** - `DELETE /api/v1/network-interfaces/:id`

---

## 💰 **採購 (Purchase)**

### ✅ **PurchaseRequisition** (`/api/v1/purchase-requisitions`)
- [ ] **Model** - PurchaseRequisition 模型定義檢查
- [ ] **Serializer** - PurchaseRequisitionSerializer 檢查
- [ ] **View** - PurchaseRequisitionViewSet 檢查
- [ ] **Create** - `POST /api/v1/purchase-requisitions`
- [ ] **Read List** - `GET /api/v1/purchase-requisitions`
- [ ] **Read Detail** - `GET /api/v1/purchase-requisitions/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/purchase-requisitions/:id`
- [ ] **Delete** - `DELETE /api/v1/purchase-requisitions/:id`

### ✅ **PurchaseOrder** (`/api/v1/purchase-orders`)
- [ ] **Model** - PurchaseOrder 模型定義檢查
- [ ] **Serializer** - PurchaseOrderSerializer 檢查
- [ ] **View** - PurchaseOrderViewSet 檢查
- [ ] **Create** - `POST /api/v1/purchase-orders`
- [ ] **Read List** - `GET /api/v1/purchase-orders`
- [ ] **Read Detail** - `GET /api/v1/purchase-orders/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/purchase-orders/:id`
- [ ] **Delete** - `DELETE /api/v1/purchase-orders/:id`

---

## 🖥️ **裸機 (Baremetal)**

### ✅ **Manufacturer** (`/api/v1/manufacturers`)
- [ ] **Model** - Manufacturer 模型定義檢查
- [ ] **Serializer** - ManufacturerSerializer 檢查
- [ ] **View** - ManufacturerViewSet 檢查
- [ ] **Create** - `POST /api/v1/manufacturers`
- [ ] **Read List** - `GET /api/v1/manufacturers`
- [ ] **Read Detail** - `GET /api/v1/manufacturers/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/manufacturers/:id`
- [ ] **Delete** - `DELETE /api/v1/manufacturers/:id`

### ✅ **Supplier** (`/api/v1/suppliers`)
- [ ] **Model** - Supplier 模型定義檢查
- [ ] **Serializer** - SupplierSerializer 檢查
- [ ] **View** - SupplierViewSet 檢查
- [ ] **Create** - `POST /api/v1/suppliers`
- [ ] **Read List** - `GET /api/v1/suppliers`
- [ ] **Read Detail** - `GET /api/v1/suppliers/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/suppliers/:id`
- [ ] **Delete** - `DELETE /api/v1/suppliers/:id`

### ✅ **BaremetalModel** (`/api/v1/baremetal-models`)
- [ ] **Model** - BaremetalModel 模型定義檢查
- [ ] **Serializer** - BaremetalModelSerializer 檢查
- [ ] **View** - BaremetalModelViewSet 檢查
- [ ] **Create** - `POST /api/v1/baremetal-models` (需要 manufacturer_id)
- [ ] **Read List** - `GET /api/v1/baremetal-models`
- [ ] **Read Detail** - `GET /api/v1/baremetal-models/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/baremetal-models/:id`
- [ ] **Delete** - `DELETE /api/v1/baremetal-models/:id`

### ✅ **BaremetalGroup** (`/api/v1/baremetal-groups`)
- [ ] **Model** - BaremetalGroup 模型定義檢查
- [ ] **Serializer** - BaremetalGroupSerializer 檢查
- [ ] **View** - BaremetalGroupViewSet 檢查
- [ ] **Create** - `POST /api/v1/baremetal-groups`
- [ ] **Read List** - `GET /api/v1/baremetal-groups`
- [ ] **Read Detail** - `GET /api/v1/baremetal-groups/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/baremetal-groups/:id`
- [ ] **Delete** - `DELETE /api/v1/baremetal-groups/:id`

### ✅ **Baremetal** (`/api/v1/baremetals`)
- [ ] **Model** - Baremetal 模型定義檢查
- [ ] **Serializer** - BaremetalSerializer 檢查
- [ ] **View** - BaremetalViewSet 檢查
- [ ] **Create** - `POST /api/v1/baremetals` (需要完整基礎設施階層)
- [ ] **Read List** - `GET /api/v1/baremetals`
- [ ] **Read Detail** - `GET /api/v1/baremetals/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/baremetals/:id`
- [ ] **Delete** - `DELETE /api/v1/baremetals/:id`

### ✅ **BaremetalGroupTenantQuota** (`/api/v1/baremetal-group-tenant-quotas`)
- [ ] **Model** - BaremetalGroupTenantQuota 模型定義檢查
- [ ] **Serializer** - BaremetalGroupTenantQuotaSerializer 檢查
- [ ] **View** - BaremetalGroupTenantQuotaViewSet 檢查
- [ ] **Create** - `POST /api/v1/baremetal-group-tenant-quotas`
- [ ] **Read List** - `GET /api/v1/baremetal-group-tenant-quotas`
- [ ] **Read Detail** - `GET /api/v1/baremetal-group-tenant-quotas/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/baremetal-group-tenant-quotas/:id`
- [ ] **Delete** - `DELETE /api/v1/baremetal-group-tenant-quotas/:id`

---

## 🏢 **租戶與虛擬化 (Tenant & Virtualization)**

### ✅ **Tenant** (`/api/v1/tenants`)
- [ ] **Model** - Tenant 模型定義檢查
- [ ] **Serializer** - TenantSerializer 檢查
- [ ] **View** - TenantViewSet 檢查
- [ ] **Create** - `POST /api/v1/tenants`
- [ ] **Read List** - `GET /api/v1/tenants`
- [ ] **Read Detail** - `GET /api/v1/tenants/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/tenants/:id`
- [ ] **Delete** - `DELETE /api/v1/tenants/:id`

### ✅ **VirtualMachineSpecification** (`/api/v1/vm-specifications`)
- [ ] **Model** - VirtualMachineSpecification 模型定義檢查
- [ ] **Serializer** - VirtualMachineSpecificationSerializer 檢查
- [ ] **View** - VirtualMachineSpecificationViewSet 檢查
- [ ] **Create** - `POST /api/v1/vm-specifications`
- [ ] **Read List** - `GET /api/v1/vm-specifications`
- [ ] **Read Detail** - `GET /api/v1/vm-specifications/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/vm-specifications/:id`
- [ ] **Delete** - `DELETE /api/v1/vm-specifications/:id`

### ✅ **VirtualMachine** (`/api/v1/virtual-machines`)
- [ ] **Model** - VirtualMachine 模型定義檢查
- [ ] **Serializer** - VirtualMachineSerializer 檢查
- [ ] **View** - VirtualMachineViewSet 檢查
- [ ] **Create** - `POST /api/v1/virtual-machines`
- [ ] **Read List** - `GET /api/v1/virtual-machines`
- [ ] **Read Detail** - `GET /api/v1/virtual-machines/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/virtual-machines/:id`
- [ ] **Delete** - `DELETE /api/v1/virtual-machines/:id`

---

## ☸️ **Kubernetes**

### ✅ **K8sCluster** (`/api/v1/k8s-clusters`)
- [ ] **Model** - K8sCluster 模型定義檢查
- [ ] **Serializer** - K8sClusterSerializer 檢查
- [ ] **View** - K8sClusterViewSet 檢查
- [ ] **Create** - `POST /api/v1/k8s-clusters`
- [ ] **Read List** - `GET /api/v1/k8s-clusters`
- [ ] **Read Detail** - `GET /api/v1/k8s-clusters/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/k8s-clusters/:id`
- [ ] **Delete** - `DELETE /api/v1/k8s-clusters/:id`

### ✅ **K8sClusterPlugin** (`/api/v1/k8s-cluster-plugins`)
- [ ] **Model** - K8sClusterPlugin 模型定義檢查
- [ ] **Serializer** - K8sClusterPluginSerializer 檢查
- [ ] **View** - K8sClusterPluginViewSet 檢查
- [ ] **Create** - `POST /api/v1/k8s-cluster-plugins`
- [ ] **Read List** - `GET /api/v1/k8s-cluster-plugins`
- [ ] **Read Detail** - `GET /api/v1/k8s-cluster-plugins/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/k8s-cluster-plugins/:id`
- [ ] **Delete** - `DELETE /api/v1/k8s-cluster-plugins/:id`

### ✅ **ServiceMesh** (`/api/v1/service-meshes`)
- [ ] **Model** - ServiceMesh 模型定義檢查
- [ ] **Serializer** - ServiceMeshSerializer 檢查
- [ ] **View** - ServiceMeshViewSet 檢查
- [ ] **Create** - `POST /api/v1/service-meshes`
- [ ] **Read List** - `GET /api/v1/service-meshes`
- [ ] **Read Detail** - `GET /api/v1/service-meshes/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/service-meshes/:id`
- [ ] **Delete** - `DELETE /api/v1/service-meshes/:id`

### ✅ **K8sClusterToServiceMesh** (`/api/v1/k8s-cluster-service-meshes`)
- [ ] **Model** - K8sClusterToServiceMesh 模型定義檢查
- [ ] **Serializer** - K8sClusterToServiceMeshSerializer 檢查
- [ ] **View** - K8sClusterToServiceMeshViewSet 檢查
- [ ] **Create** - `POST /api/v1/k8s-cluster-service-meshes`
- [ ] **Read List** - `GET /api/v1/k8s-cluster-service-meshes`
- [ ] **Read Detail** - `GET /api/v1/k8s-cluster-service-meshes/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/k8s-cluster-service-meshes/:id`
- [ ] **Delete** - `DELETE /api/v1/k8s-cluster-service-meshes/:id`

### ✅ **BastionClusterAssociation** (`/api/v1/bastion-cluster-associations`)
- [ ] **Model** - BastionClusterAssociation 模型定義檢查
- [ ] **Serializer** - BastionClusterAssociationSerializer 檢查
- [ ] **View** - BastionClusterAssociationViewSet 檢查
- [ ] **Create** - `POST /api/v1/bastion-cluster-associations`
- [ ] **Read List** - `GET /api/v1/bastion-cluster-associations`
- [ ] **Read Detail** - `GET /api/v1/bastion-cluster-associations/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/bastion-cluster-associations/:id`
- [ ] **Delete** - `DELETE /api/v1/bastion-cluster-associations/:id`

---

## 📚 **Ansible 庫存 (Ansible Inventory)**

### ✅ **AnsibleInventory** (`/api/v1/ansible-inventories`)
- [ ] **Model** - AnsibleInventory 模型定義檢查
- [ ] **Serializer** - AnsibleInventorySerializer 檢查
- [ ] **View** - AnsibleInventoryViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-inventories`
- [ ] **Read List** - `GET /api/v1/ansible-inventories`
- [ ] **Read Detail** - `GET /api/v1/ansible-inventories/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-inventories/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-inventories/:id`
- [ ] **Special** - `GET /api/v1/ansible-inventories/:id/merged_variables` (自定義端點)

### ✅ **AnsibleInventoryVariable** (`/api/v1/ansible-inventory-variables`)
- [ ] **Model** - AnsibleInventoryVariable 模型定義檢查
- [ ] **Serializer** - AnsibleInventoryVariableSerializer 檢查
- [ ] **View** - AnsibleInventoryVariableViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-inventory-variables`
- [ ] **Read List** - `GET /api/v1/ansible-inventory-variables`
- [ ] **Read Detail** - `GET /api/v1/ansible-inventory-variables/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-inventory-variables/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-inventory-variables/:id`

### ✅ **AnsibleVariableSet** (`/api/v1/ansible-variable-sets`)
- [ ] **Model** - AnsibleVariableSet 模型定義檢查
- [ ] **Serializer** - AnsibleVariableSetSerializer 檢查
- [ ] **View** - AnsibleVariableSetViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-variable-sets`
- [ ] **Read List** - `GET /api/v1/ansible-variable-sets`
- [ ] **Read Detail** - `GET /api/v1/ansible-variable-sets/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-variable-sets/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-variable-sets/:id`
- [ ] **Special** - `GET /api/v1/ansible-variable-sets/by_tags` (自定義端點)

### ✅ **AnsibleInventoryVariableSetAssociation** (`/api/v1/ansible-inventory-variable-set-associations`)
- [ ] **Model** - AnsibleInventoryVariableSetAssociation 模型定義檢查
- [ ] **Serializer** - AnsibleInventoryVariableSetAssociationSerializer 檢查
- [ ] **View** - AnsibleInventoryVariableSetAssociationViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-inventory-variable-set-associations`
- [ ] **Read List** - `GET /api/v1/ansible-inventory-variable-set-associations`
- [ ] **Read Detail** - `GET /api/v1/ansible-inventory-variable-set-associations/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-inventory-variable-set-associations/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-inventory-variable-set-associations/:id`

### ✅ **AnsibleInventoryPlugin** (`/api/v1/ansible-inventory-plugins`)
- [ ] **Model** - AnsibleInventoryPlugin 模型定義檢查
- [ ] **Serializer** - AnsibleInventoryPluginSerializer 檢查
- [ ] **View** - AnsibleInventoryPluginViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-inventory-plugins`
- [ ] **Read List** - `GET /api/v1/ansible-inventory-plugins`
- [ ] **Read Detail** - `GET /api/v1/ansible-inventory-plugins/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-inventory-plugins/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-inventory-plugins/:id`

### ✅ **AnsibleInventoryTemplate** (`/api/v1/ansible-inventory-templates`)
- [ ] **Model** - AnsibleInventoryTemplate 模型定義檢查
- [ ] **Serializer** - AnsibleInventoryTemplateSerializer 檢查
- [ ] **View** - AnsibleInventoryTemplateViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-inventory-templates`
- [ ] **Read List** - `GET /api/v1/ansible-inventory-templates`
- [ ] **Read Detail** - `GET /api/v1/ansible-inventory-templates/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-inventory-templates/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-inventory-templates/:id`

---

## 🎯 **Ansible 群組與主機 (Ansible Groups & Hosts)**

### ✅ **AnsibleGroup** (`/api/v1/ansible-groups`)
- [ ] **Model** - AnsibleGroup 模型定義檢查
- [ ] **Serializer** - AnsibleGroupSerializer 檢查
- [ ] **View** - AnsibleGroupViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-groups`
- [ ] **Read List** - `GET /api/v1/ansible-groups`
- [ ] **Read Detail** - `GET /api/v1/ansible-groups/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-groups/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-groups/:id`

### ✅ **AnsibleGroupVariable** (`/api/v1/ansible-group-variables`)
- [ ] **Model** - AnsibleGroupVariable 模型定義檢查
- [ ] **Serializer** - AnsibleGroupVariableSerializer 檢查
- [ ] **View** - AnsibleGroupVariableViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-group-variables`
- [ ] **Read List** - `GET /api/v1/ansible-group-variables`
- [ ] **Read Detail** - `GET /api/v1/ansible-group-variables/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-group-variables/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-group-variables/:id`

### ✅ **AnsibleGroupRelationship** (`/api/v1/ansible-group-relationships`)
- [ ] **Model** - AnsibleGroupRelationship 模型定義檢查
- [ ] **Serializer** - AnsibleGroupRelationshipSerializer 檢查
- [ ] **View** - AnsibleGroupRelationshipViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-group-relationships`
- [ ] **Read List** - `GET /api/v1/ansible-group-relationships`
- [ ] **Read Detail** - `GET /api/v1/ansible-group-relationships/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-group-relationships/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-group-relationships/:id`

### ✅ **AnsibleHost** (`/api/v1/ansible-hosts`)
- [ ] **Model** - AnsibleHost 模型定義檢查
- [ ] **Serializer** - AnsibleHostSerializer 檢查
- [ ] **View** - AnsibleHostViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-hosts` (支援多對多群組關係)
- [ ] **Read List** - `GET /api/v1/ansible-hosts`
- [ ] **Read Detail** - `GET /api/v1/ansible-hosts/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-hosts/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-hosts/:id`

### ✅ **AnsibleHostVariable** (`/api/v1/ansible-host-variables`)
- [ ] **Model** - AnsibleHostVariable 模型定義檢查
- [ ] **Serializer** - AnsibleHostVariableSerializer 檢查
- [ ] **View** - AnsibleHostVariableViewSet 檢查
- [ ] **Create** - `POST /api/v1/ansible-host-variables`
- [ ] **Read List** - `GET /api/v1/ansible-host-variables`
- [ ] **Read Detail** - `GET /api/v1/ansible-host-variables/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/ansible-host-variables/:id`
- [ ] **Delete** - `DELETE /api/v1/ansible-host-variables/:id`

---

## ⚙️ **系統 (System)**

### ✅ **SystemInfo** (`/api/v1/system-info`)
- [ ] **Model** - 系統資訊模型檢查
- [ ] **Serializer** - SystemInfoSerializer 檢查
- [ ] **View** - SystemInfoViewSet 檢查
- [ ] **Read List** - `GET /api/v1/system-info` (只讀端點)

### ✅ **ObjectPermissions** (`/api/v1/permissions`)
- [ ] **Model** - ObjectPermission 模型檢查
- [ ] **Serializer** - ObjectPermissionSerializer 檢查
- [ ] **View** - ObjectPermissionViewSet 檢查
- [ ] **Create** - `POST /api/v1/permissions`
- [ ] **Read List** - `GET /api/v1/permissions`
- [ ] **Read Detail** - `GET /api/v1/permissions/:id`
- [ ] **Update** - `PUT/PATCH /api/v1/permissions/:id`
- [ ] **Delete** - `DELETE /api/v1/permissions/:id`

---

## 📊 **檢查統計**

### 總計
- **Models**: 30 個
- **Endpoints**: 30 個 
- **檢查項目總數**: 239 個
  - **架構檢查**: 90 個 (Model + Serializer + View)
  - **CRUD Operations**: 149 個 (包含特殊端點)

### 按類別統計
- **用戶管理**: 1 個模型 (8 個檢查項目)
- **基礎設施**: 6 個模型 (48 個檢查項目)
- **網路**: 4 個模型 (32 個檢查項目)
- **採購**: 2 個模型 (16 個檢查項目)
- **裸機**: 6 個模型 (48 個檢查項目)
- **租戶與虛擬化**: 3 個模型 (24 個檢查項目)
- **Kubernetes**: 5 個模型 (40 個檢查項目)
- **Ansible**: 10 個模型 (80 個檢查項目)
- **系統**: 2 個模型 (13 個檢查項目)

---

## 🔗 **重要關係依賴**

### 基礎設施階層
```
Fabrication → Phase → DataCenter → Room → Rack → Unit
```

### 裸機階層
```
Manufacturer → BaremetalModel → Baremetal
Supplier ← BaremetalModel
Baremetal → Unit (位置)
Baremetal → BaremetalGroup
```

### Ansible 關係
```
AnsibleInventory → AnsibleGroup → AnsibleHost
AnsibleHost ↔ AnsibleGroup (多對多)
AnsibleVariableSet → AnsibleInventory (多對多)
```

---

**📝 使用說明：**
1. **架構檢查**：
   - [ ] **Model** - 檢查模型定義、欄位、關係、約束等
   - [ ] **Serializer** - 檢查序列化器欄位、驗證、自定義方法等
   - [ ] **View** - 檢查視圖集、權限、過濾、自定義動作等
2. **功能檢查**：按順序檢查每個 Model 的 CRUD 操作
3. 測試完成後在對應的 checkbox 打勾 ✅
4. 注意標註的依賴關係，確保先建立父物件
5. 特別注意基礎設施階層關係的完整性
6. 測試多對多關係的建立和更新功能

**🧪 建議檢查順序：**
1. **架構檢查** (Model → Serializer → View)
2. **基礎設施** (由上到下：Fab → Phase → DC → Room → Rack → Unit)
3. **裸機相關** (Manufacturer → Supplier → BaremetalModel → BaremetalGroup → Baremetal)
4. **網路相關**
5. **虛擬化相關**
6. **Ansible 相關**
7. **系統功能**

**🔍 檢查重點：**
- **Model**: 欄位定義、關係設定、Meta 選項、方法實現
- **Serializer**: 欄位對應、驗證邏輯、嵌套關係、自定義方法
- **View**: CRUD 實現、權限控制、過濾功能、自定義端點
