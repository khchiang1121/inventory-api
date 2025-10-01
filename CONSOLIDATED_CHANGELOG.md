# 整合變更清單 (2025-08-01 至 2025-09-22)

## 專案重構與命名
- 將專案名稱從 VirtFlow 重命名為 Inventory API
- 更新所有相關文檔和配置檔案
- 更新 API 端點從 `/fabrications` 改為 `/fab` 以保持一致性

## 開發環境與工具
- 新增 VS Code devcontainer 配置
- 設定 Docker 和 docker-compose 開發環境
- 新增 entrypoint.sh 腳本
- 配置 APT 和 pip 源管理
- 新增 pylint-django 插件配置到 pyproject.toml
- 更新 devcontainer 配置以反映預安裝功能
- 簡化 Dockerfile 並增強命令結構清晰度

## 測試與品質保證
- 引入 pytest 配置和測試支援
- 新增大量測試套件，涵蓋所有模型和 API 端點
- 修復基礎設施階層關係變更導致的測試失敗
- 修復假資料生成器中供應商電話號碼長度限制問題
- 更新所有測試以適應新的模型結構和關聯關係
- 新增 313 行綜合測試用於 Unit 模型
- 修復 12 個失敗的測試，確保所有 321 個測試通過

## 模型架構重構
- 將單一 models.py 文件拆分為模組化結構
- 分離關注點：ansible.py, baremetal.py, infrastructure.py, purchase.py, users.py, scheduling_strategy.py
- 建立完整的基礎設施階層：Fab → Phase → DataCenter → Room → Rack → Unit
- 所有外鍵關係設定為 `null=True, blank=True` 以支援漸進式遷移
- 使用 `on_delete=models.CASCADE` 確保階層刪除一致性

## 基礎設施模型變更
- 新增 `Phase.fab` (ForeignKey to Fab) - 每個階段必須屬於一個製造廠
- 新增 `DataCenter.phase` (ForeignKey to Phase) - 每個資料中心必須屬於一個階段
- 新增 `Room.datacenter` (ForeignKey to DataCenter) - 每個機房必須屬於一個資料中心
- 新增 `Rack.room` (ForeignKey to Room) - 每個機架必須屬於一個機房
- 新增 `Unit.rack` (ForeignKey to Rack) - 每個單位已屬於一個機架
- 新增 `Unit.unit_number` (PositiveIntegerField) 欄位
- 新增 `Rack.bgp_number` (unique) 和 `Rack.as_number` 欄位
- 新增 `Rack.height_units`, `used_units`, `available_units`, `power_capacity`, `status` 欄位
- 新增 `Rack.available_group` (ForeignKey to AvailableGroup)
- 新增 `Unit.bgp` 欄位
- 新增 `AvailableGroup` 模型用於 Rack 可用群組管理

## 裸機與虛擬機模型變更
- 更新 `BaremetalGroup.user` 的 related_name 從 "baremetals" 改為 "baremetal_groups"
- 更新 `BaremetalGroup.user_group` 從自定義 UserGroup 改為 Django 內建 Group
- 更新 `BaremetalGroup.user_group` 的 related_name 從 "baremetals" 改為 "baremetal_groups"
- 新增 `BaremetalGroup.is_multi_tenant` 布林欄位
- 更新 `Baremetal.user` 的 related_name 從 "baremetals" 改為 "owned_baremetals"
- 更新 `Baremetal.user_group` 從自定義 UserGroup 改為 Django 內建 Group
- 更新 `Baremetal.user_group` 的 related_name 從 "baremetals" 改為 "owned_baremetals"
- 更新 `BaremetalModelGPU.count` 欄位新增 `default=0`
- 更新 `K8sCluster.user` 從 FK("User") 改為 FK("CustomUser")
- 新增 `K8sCluster.failure_zone_cluster` 欄位設定為 `null=True, blank=True`
- 新增 `K8sCluster.scheduling_strategy` (ForeignKey to SchedulingStrategy)

## GPU 能力建模
- 將 GPU 模型從 virtual.py 移動到 infrastructure.py 集中管理
- 新增 `PhysicalGPUModel` 模型，包含 name, vendor, architecture, status, created_at, updated_at 欄位
- 新增 `PhysicalGPU` 模型，包含 name, serial_number, model, baremetal, virtual_machine, status 欄位
- 修正 `VirtualMachineSpecificationGPU.count` 欄位新增 `default=0`
- 維持 `VirtualMachineSpecification.required_gpu` 與 `PhysicalGPUModel` 的多對多關係

## 排程策略模型
- 新增 `SchedulingStrategy` 模型，包含 mode (spread_rack/spread_resource/balanced/default) 欄位
- 新增多種容錯同域限制布林欄位：phase, dc, region, tenant
- 新增 `SchedulingStrategy.available_group` (ManyToManyField)
- 新增 `SchedulingStrategy.priority` 和 `SchedulingStrategy.cluster_shared` 欄位
- 新增 `SchedulingStrategyCondition` 模型

## 使用者與群組模型變更
- 移除自定義 `UserGroup` 類別
- 改用 Django 內建 `Group` 模型
- 更新所有相關的 related_name 以語意化

## 採購模型重構
- 移除 `PurchaseOrder` 的 `vendor_name`, `delivery_date`, `issued_by` 欄位
- 新增 `PurchaseOrder.purchase_requisition` (ForeignKey to PurchaseRequisition)
- 新增 `PurchaseOrder.supplier` (ForeignKey to Supplier)
- 新增 `PurchaseOrder.amount` (Decimal, 可空)
- 新增 `PurchaseOrder.used` (Decimal, 可空)
- 新增 `PurchaseOrder.description` 欄位
- 維持 `PurchaseRequisition` 基本欄位：pr_number, requested_by, department, reason, submit_date

## 品牌與供應商模型變更
- 移除 `Brand` 模型
- 新增 `Manufacturer` 模型 (製造商)
- 新增 `Supplier` 模型 (供應商)
- 更新 Baremetal 模型以使用新的供應商關係

## Ansible 模型變更
- 將 `AnsibleHost.group` (ForeignKey) 改為 `AnsibleHost.groups` (ManyToManyField)
- 更新 unique_together 約束
- 改善 `__str__` 方法處理多群組顯示
- 修復 `AnsibleInventory.source_plugin` 欄位從 blank=True 改為 null=True

## 序列化器增強
- 啟用所有基礎設施序列化器的嵌套關係顯示功能
- 啟用嵌套序列化器：PhaseSerializer.fab, DataCenterSerializer.phase, RoomSerializer.datacenter, RackSerializer.room, UnitSerializer.rack
- 所有嵌套欄位設定為 `read_only=True`
- 建立對應的 Create/Update 序列化器：FabCreateSerializer, PhaseCreateSerializer, DataCenterCreateSerializer, RoomCreateSerializer, UnitCreateSerializer
- 統一欄位順序並確保所有序列化器包含 `created_at` 和 `updated_at` 欄位
- 修復 Unit 序列化器欄位：新增 `unit_number` 欄位支援
- 新增自定義 `create()` 和 `update()` 方法處理 ManyToMany 關係
- 更新 `PurchaseOrderSerializer` 新增嵌套顯示採購申請和供應商詳細資訊
- 新增 `PurchaseOrderCreateSerializer` 和 `PurchaseOrderUpdateSerializer`

## 視圖與 API 更新
- 為所有基礎設施 ViewSets 添加 `get_serializer_class` 方法
- 確保 create/update 操作使用正確的序列化器，retrieve/list 操作顯示嵌套資料
- 修復 AnsibleHost 排序問題 (`group__name` → `id`)
- 更新 AnsibleHostVariable 排序邏輯
- 修復 BaremetalModelViewSet 中被註解的 `get_serializer_class` 方法

## 假資料生成器更新
- 修復變數名稱衝突問題（`fab` vs `fabs`）
- 更新 Unit 建立邏輯以包含 `unit_number` 欄位
- 確保階層關係正確建立
- 從獨立建立改為階層式建立流程：3個製造廠 → 5個階段 → 4個資料中心 → 8個機房 → 12個機架
- 更新使用 `host.groups.set([group])` 替代直接賦值
- 重新設計以正確建立採購申請→採購訂單→供應商關係

## 資料庫遷移
- 建立 `0002_datacenter_phase_phase_fab_rack_room_room_datacenter.py` 遷移
- 更新 `0001_initial.py` 遷移時間戳以保持與 Django 生成時間的一致性
- 成功應用所有外鍵關係變更

## CI/CD 與部署
- 新增 GitLab CI/CD 配置
- 新增 Helm chart 用於 Kubernetes 部署
- 新增健康檢查端點用於系統狀態監控
- 更新生產部署 URL

## API 文檔與設計
- 新增大量 API 和設計文檔
- 重新組織文檔結構到 `docs/` 目錄下
- 新增 `MODEL_ENDPOINT_CHECKLIST.md` 文件

## 統計資訊
- 總提交數：約 20+ 個提交
- 檔案變更：約 100+ 個檔案
- 程式碼行數：新增約 2,000+ 行，刪除約 1,000+ 行
- 測試覆蓋：321 個測試全部通過
- 主要影響區域：模型層、序列化器、測試套件、資料庫遷移、假資料生成
