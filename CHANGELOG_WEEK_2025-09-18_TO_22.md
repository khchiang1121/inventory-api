# Changelog - 2025年9月18日至22日

**時間範圍**: 2025-09-18 → 2025-09-22  
**貢獻者**: khchiang1121

## 📋 本週概要

- **多租戶與群組關聯**: 擴充 Baremetal 與 Virtual 模型支援使用者與群組多對多關係，並引入群組可共享的資源池概念。
- **GPU 能力建模**: 新增實體 GPU 與 GPU 規格模型，將 GPU 模型集中於基礎設施領域，並完善與裸機/虛機/規格的關聯。
- **排程策略**: 新增 `SchedulingStrategy` 與條件模型，支援跨機架/資源分散與容錯分區限制。
- **採購領域**: 重構 `PurchaseOrder` 與 `PurchaseRequisition` 關聯，整合 `Supplier`，提供金額與已用額度欄位。
- **基礎設施**: Rack/Unit 維護可用群組 `AvailableGroup`，Unit 新增 `unit_number` 與 `bgp`；Rack 增加唯一 BGP 編號與 AS 編號等屬性。

---

## 📅 詳細變更記錄（含模型前後差異）

### 2025-09-22
**feat(models): 多租戶、使用者群組、GPU 與排程策略**  
檔案: `inventory_api/api/models/{baremetal.py,infrastructure.py,virtual.py,users.py,scheduling_strategy.py}`

- Baremetal 與群組
  - 變更:
    - `BaremetalGroup.user`: `ManyToMany(CustomUser, related_name="baremetals")` → `ManyToMany(CustomUser, related_name="baremetal_groups")`
    - `BaremetalGroup.user_group`: `ManyToMany(UserGroup, related_name="baremetals")` → `ManyToMany(django.contrib.auth.models.Group, related_name="baremetal_groups")`
    - `BaremetalGroup.is_multi_tenant`: 新增布林欄位（已存在但用途明確化）
  - 影響: 採用 Django 內建 `Group` 取代自定義 `UserGroup`，並調整 related_name 以語意化。

- Baremetal 實體
  - 變更:
    - `user`: `ManyToMany(CustomUser, related_name="baremetals")` → `ManyToMany(CustomUser, related_name="owned_baremetals")`
    - `user_group`: `ManyToMany(UserGroup, related_name="baremetals")` → `ManyToMany(Group, related_name="owned_baremetals")`
    - `purchase_order`: 維持 FK，但格式化與語意註解更新
    - `BaremetalModelGPU.count`: `IntegerField()` → `IntegerField(default=0)`
  - 影響: 欄位語意與預設值更合理；群組改用核心模型。

- 使用者與群組
  - 變更:
    - 移除自定義 `UserGroup` 類別；改為使用 Django 內建 `Group`
  - 影響: 降低重複建模，對序列化與授權策略需同步調整。

- GPU 能力建模（集中於基礎設施領域）
  - 新增（移動）到 `infrastructure.py`：
    - `PhysicalGPUModel`（欄位：`name/vendor/architecture/.../status/created_at/updated_at`）
    - `PhysicalGPU`（欄位：`name/serial_number/model/baremetal/virtual_machine/status`）
  - 自 `virtual.py` 移除舊的 `PhysicalGPUModel`/`PhisicalGPU` 定義，並修正關聯：
    - `VirtualMachineSpecification.required_gpu` 維持 M2M 至 `PhysicalGPUModel`
    - `VirtualMachineSpecificationGPU.count`: `IntegerField()` → `IntegerField(default=0)`
  - 影響: 名稱更正與領域邊界清晰，避免重複定義。

- K8s 與排程
  - `K8sCluster.scheduling_strategy`: 新增 FK 至 `SchedulingStrategy`
  - `K8sCluster.user`: `FK("User")` → `FK("CustomUser")`
  - `K8sCluster.failure_zone_cluster`: 新增 `null=True, blank=True`
  - 新增 `SchedulingStrategy` 與 `SchedulingStrategyCondition` 模型：
    - 主要欄位：`mode`（`spread_rack/spread_resource/balanced/default`）、多種容錯同域限制布林欄位（phase/dc/region/tenant）、`available_group` M2M、`priority`、`cluster_shared` 等
  - 影響: 支援跨機架/資源分散策略與容錯區域限制，並與可用群組掛鉤。

- 基礎設施
  - 新增 `AvailableGroup`（Rack 可用群組）
  - `Rack` 新增/調整欄位：`bgp_number`（unique）、`as_number`、`height_units/used_units/available_units/power_capacity/status`、`available_group` FK
  - `Unit` 新增 `unit_number` 與 `bgp`；`unique_together = ["rack", "name"]` 維持

- 序列化/視圖影響（未納入本檔案詳細）：`inventory_api/api/v1/serializers.py` 與 `views.py` 已相應更新


### 2025-09-19
**feat(models): 採購模型重構與關聯整合**  
檔案: `inventory_api/api/models/purchase.py`

- `PurchaseOrder` 由舊結構調整為：
  - 新增 FK：`purchase_requisition`（可空）、`supplier`（可空，改為 FK 至 `Supplier`）
  - 新增金額欄位：`amount`、`used`（Decimal，可空）
  - 保留：`po_number`、`payment_terms`、`description`
- `PurchaseRequisition`：維持基本欄位（`pr_number/requested_by/department/reason/submit_date`）
- 舊→新（主要差異）:
  - 舊：`PurchaseOrder.vendor_name/delivery_date/issued_by`（推測已移除）
  - 新：改以 `supplier` 與 `purchase_requisition` 關聯管理，並加入金額追蹤


### 2025-09-18
**feat(models): 基礎設施階層與 `unit_number`**  
檔案: `inventory_api/api/models/infrastructure.py`

- 階層模型維持：`Fab → Phase → DataCenter → Room → Rack → Unit`
- `Unit` 新增欄位：`unit_number: PositiveIntegerField`
- 其他欄位與 FK 維持 `null=True, blank=True`（phase/datacenter/room/rack 之鏈）以利漸進遷移

---

## 🔄 未提交變更（Working Tree）

已檢視未提交差異，重點如下：

- `inventory_api/api/models/infrastructure.py`
  - 新增於檔尾：`PhysicalGPUModel` 與 `PhysicalGPU`（與 9/22 方向一致，集中 GPU 定義）
- `inventory_api/api/models/baremetal.py`
  - 調整 `Group` 導入與 related_name；`BaremetalModelGPU.count` 預設值 0
- `inventory_api/api/models/virtual.py`
  - 移除舊 `PhysicalGPUModel/PhisicalGPU`，導入自 `infrastructure` 的模型；`VirtualMachineSpecificationGPU.count` 預設值 0；`K8sCluster.user`、`failure_zone_cluster` 調整；`user_group` 改用內建 `Group`
- `inventory_api/api/models/users.py`
  - 移除自定義 `UserGroup` 類別，改採 Django 內建 `Group`

建議後續動作：
- 檢查並產生 Django migration（新增/移除/預設值變更、M2M 目標替換可能需要資料遷移腳本）
- 同步更新序列化器、viewsets 與測試（群組模型更動與 related_name 改動）

---

## 📊 統計與影響範圍

- 涉及領域：模型、序列化器、視圖、遷移、權限/授權（群組模型更換）
- 潛在破壞性變更：
  - `UserGroup` → `django.contrib.auth.models.Group`
  - related_name 調整（`baremetals` 改為 `baremetal_groups` / `owned_baremetals` 等）
  - GPU 模型位置/名稱更正與集中

---

**生成時間**: 2025-09-22  
**涵蓋期間**: 2025-09-18 至 2025-09-22
