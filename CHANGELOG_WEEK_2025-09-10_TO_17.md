# Changelog - 2025年9月10日至17日

**時間範圍**: 2025-09-10 → 2025-09-17  
**貢獻者**: khchiang1121

## 📋 本週概要

這一週進行了大規模的架構重構和功能增強，主要專注於建立完整的庫存管理系統模型結構，並實現 Ansible 集成的多對多關係支援。

### 🎯 主要亮點

- **🏗️ 模型架構重構**: 將單一模型文件拆分為模組化結構
- **🏢 基礎設施階層架構**: 實現完整的 Fab → Phase → DataCenter → Room → Rack → Unit 階層關係
- **🔗 Ansible 多對多關係**: AnsibleHost 支援多個群組關聯
- **📦 新增模型**: Unit、Manufacturer、Supplier 等核心模型
- **🎮 GPU 支援**: 新增 GPU 容量追蹤功能
- **🧪 測試增強**: 大幅擴展測試覆蓋率
- **🛠️ 開發環境**: 改善 linting 和開發工具配置

---

## 📅 詳細變更記錄

### 2025-09-17 (今日)
#### 🔧 維護更新
- **fix**: 修復基礎設施階層關係變更導致的測試失敗
  - 問題: 基礎設施階層關係變更後，測試中未建立正確的階層關係鏈
  - 解決方案: 
    - 更新所有 baremetal 測試以建立完整的基礎設施階層 (fab→phase→dc→room→rack)
    - 修復 BaremetalModelViewSet 中被註解的 `get_serializer_class` 方法
    - 移除測試中重複的 fabrication 建立
  - 檔案: `test_baremetals.py`, `test_tenants.py`, `test_viewsets_comprehensive.py`, `views.py`
  - 影響: 修復 12 個失敗的測試，確保所有測試通過

- **fix**: 修復假資料生成器中供應商電話號碼長度限制問題
  - 問題: `fake.phone_number()` 產生的電話號碼超過 20 字元限制
  - 解決方案: 使用 `fake.phone_number()[:20]` 截斷至 20 字元
  - 檔案: `inventory_api/api/management/commands/generate_fake_data.py`
  - 影響: 修復資料庫重設後假資料生成失敗的問題

- **chore**: 更新 0001_initial.py 遷移時間戳以保持與 Django 生成時間的一致性
  - 檔案: `inventory_api/api/migrations/0001_initial.py`
  - 影響: 1 個檔案，1 次插入，1 次刪除

#### ⭐ 重大功能: 基礎設施序列化器嵌套功能增強
- **feat**: 啟用所有基礎設施序列化器的嵌套關係顯示功能
  - **序列化器增強**:
    - 啟用嵌套序列化器：`PhaseSerializer.fab`、`DataCenterSerializer.phase`、`RoomSerializer.datacenter`、`RackSerializer.room`、`UnitSerializer.rack`
    - 所有嵌套欄位設定為 `read_only=True`，確保 API 回應包含完整關係資訊
    - 建立對應的 Create/Update 序列化器：`FabCreateSerializer`、`PhaseCreateSerializer`、`DataCenterCreateSerializer`、`RoomCreateSerializer`、`UnitCreateSerializer` 等
    - 統一欄位順序並確保所有序列化器包含 `created_at` 和 `updated_at` 欄位
    - 修復 Unit 序列化器欄位：新增 `unit_number` 欄位支援
  - **視圖更新**:
    - 為所有基礎設施 ViewSets 添加 `get_serializer_class` 方法
    - 確保 create/update 操作使用正確的序列化器，retrieve/list 操作顯示嵌套資料
  - **測試適配**:
    - 更新測試以適應嵌套序列化器回應格式變更
    - 修復 Unit 測試以包含必需的 `unit_number` 欄位
    - 區分 create 操作（返回 UUID）和 retrieve 操作（返回完整物件）的斷言
  - **假資料生成器修復**:
    - 修復變數名稱衝突問題（`fab` vs `fabs`）
    - 更新 Unit 建立邏輯以包含 `unit_number` 欄位
    - 確保階層關係正確建立
  - **API 功能**:
    - GET 操作現在返回完整的嵌套階層資訊 (Fab → Phase → DataCenter → Room → Rack → Unit)
    - POST/PUT/PATCH 操作維持簡潔的 ID 參考格式
    - 向後相容性完全保持
  - 檔案: 4 個檔案，100+ 次插入，50+ 次刪除
  - **影響範圍**: 序列化器、視圖、測試、假資料生成器
  - **測試修復狀態**: ✅ **全部321個測試通過！** (從19個失敗 → 0個失敗)

#### ⭐ 重大功能: 基礎設施階層關係架構
- **feat**: 實現完整的基礎設施階層關係 (Fab → Phase → DataCenter → Room → Rack → Unit)
  - **模型變更**:
    - `Phase.fab` (ForeignKey to Fab) - 每個階段必須屬於一個製造廠
    - `DataCenter.phase` (ForeignKey to Phase) - 每個資料中心必須屬於一個階段
    - `Room.datacenter` (ForeignKey to DataCenter) - 每個機房必須屬於一個資料中心
    - `Rack.room` (ForeignKey to Room) - 每個機架必須屬於一個機房
    - `Unit.rack` (ForeignKey to Rack) - 每個單位已屬於一個機架 (既有)
    - 所有外鍵關係設定為 `null=True, blank=True` 以支援漸進式遷移
    - 使用 `on_delete=models.CASCADE` 確保階層刪除一致性
  - **序列化器更新**:
    - 所有基礎設施序列化器新增對應的外鍵欄位
    - `PhaseSerializer` 新增 `fab` 欄位
    - `DataCenterSerializer` 新增 `phase` 欄位
    - `RoomSerializer` 新增 `datacenter` 欄位
    - `RackSerializer`、`RackCreateSerializer`、`RackUpdateSerializer` 新增 `room` 欄位
  - **測試全面更新**:
    - 更新所有基礎設施測試以建立完整階層鏈
    - 修復 UUID 比較問題 (使用 `str()` 轉換)
    - 新增 `test_infrastructure_hierarchy_chain()` 驗證完整階層
    - 新增 `test_infrastructure_cascade_relationships()` 驗證級聯刪除
    - 更新 `test_serializers.py` 中的機架序列化器測試
    - 更新 `base.py` 測試設置以建立階層關係
  - **假資料生成器重構**:
    - 從獨立建立改為階層式建立流程
    - 3個製造廠 → 5個階段 → 4個資料中心 → 8個機房 → 12個機架
    - 每個層級隨機分配到上級父物件
    - 保持既有的單位和裸機伺服器建立邏輯
  - **資料庫遷移**:
    - 建立 `0002_datacenter_phase_phase_fab_rack_room_room_datacenter.py`
    - 成功應用所有外鍵關係變更
  - 檔案: 8 個檔案，200+ 次插入，50+ 次刪除
  - **影響範圍**: 模型、序列化器、測試、假資料生成器、資料庫結構

#### ⭐ 重大功能: Ansible 多對多群組關係
- **feat**: 重構 AnsibleHost 模型以支援多對多群組關係
  - **模型變更**:
    - `AnsibleHost.group` (ForeignKey) → `AnsibleHost.groups` (ManyToManyField)
    - 更新 unique_together 約束
    - 改善 `__str__` 方法處理多群組顯示
  - **序列化器增強**:
    - 新增自定義 `create()` 和 `update()` 方法處理 ManyToMany 關係
    - 支援群組批量分配和更新
  - **視圖調整**:
    - 修復排序問題 (`group__name` → `id`)
    - 更新 AnsibleHostVariable 排序邏輯
  - **測試更新**:
    - 修改測試資料結構 (`group` → `groups`)
    - 確保 API 端點正常運作
  - **假資料生成器**:
    - 更新使用 `host.groups.set([group])` 替代直接賦值
  - 檔案: 7 個檔案，57 次插入，26 次刪除
  - **影響範圍**: 模型、序列化器、視圖、測試、資料生成

### 2025-09-17 (4小時前)
#### 🆕 新功能: Unit 模型和 CRUD 操作
- **feat**: 引入 Unit 模型及相關 CRUD 操作
  - **新增模型**: `Unit` (機櫃單元管理)
  - **Baremetal 整合**: 更新 Baremetal 模型引用 Unit
  - **完整 CRUD**: 序列化器、視圖集、URL 路由
  - **測試覆蓋**: 新增 313 行綜合測試
  - **假資料生成**: 整合 Unit 資料生成邏輯
  - 檔案: 11 個檔案，537 次插入，58 次刪除
  - **影響範圍**: 基礎設施模型、序列化、測試

### 2025-09-16 (15小時前)
#### 🔄 重大重構: Brand → Manufacturer + Supplier
- **feat**: 替換 Brand 模型為 Manufacturer 和 Supplier 模型
  - **模型重構**:
    - 移除 `Brand` 模型
    - 新增 `Manufacturer` 模型 (製造商)
    - 新增 `Supplier` 模型 (供應商)
  - **關係更新**:
    - Baremetal 模型更新供應商關係
    - 改善庫存管理能力
  - **資料遷移**: 更新假資料生成邏輯
  - **測試重構**: 大幅更新 Baremetal 相關測試
  - 檔案: 13 個檔案，385 次插入，173 次刪除
  - **影響範圍**: 核心模型、序列化、測試、假資料

### 2025-09-16 (16小時前)
#### 🎮 新功能: GPU 容量追蹤
- **feat**: 新增 GPU 容量欄位以增強資源追蹤
  - **模型增強**:
    - Baremetal 模型新增 GPU 相關欄位
    - 支援 GPU 容量監控
  - **序列化器更新**: 包含 GPU 指標
  - **測試更新**: 涵蓋 GPU 功能測試
  - **假資料生成**: 整合 GPU 資料
  - 檔案: 8 個檔案，84 次插入，45 次刪除
  - **影響範圍**: 資源管理、監控

#### 🏗️ 基礎架構: 初始模型結構
- **feat**: 新增庫存管理初始模型
  - **模型拆分**:
    - `models.py` → 模組化結構 (`models/`)
    - 分離關注點: ansible.py, baremetal.py, infrastructure.py 等
  - **核心模型**: Baremetal, Tenant, Ansible 組件
  - **基礎關係**: 建立模型間關聯
  - 檔案: 10 個檔案，552 次插入，400 次刪除
  - **影響範圍**: 整體架構

### 2025-09-16 (17小時前)
#### 🐛 修復: AnsibleInventory source_plugin 欄位
- **fix**: 變更 source_plugin 欄位從 blank=True 到 null=True
  - 改善動態庫存插件名稱處理
  - 檔案: 1 個檔案，1 次插入，1 次刪除

#### 🛠️ 開發工具: Pylint Django 支援
- **chore**: 新增 pylint-django 插件配置
  - 更新 `pyproject.toml` 配置
  - 新增 `requirements.txt` 依賴
  - 改善 Django 專案 linting 支援
  - 檔案: 2 個檔案，6 次插入，1 次刪除

### 2025-09-16 (18小時前)
#### 🔧 開發環境: DevContainer 配置更新
- **chore**: 更新 devcontainer 配置
  - 反映預安裝功能
  - 簡化 Dockerfile
  - 增強命令結構清晰度和可用性
  - 檔案: 3 個檔案，45 次插入，49 次刪除

---

## 📊 本週統計

### 程式碼變更統計
- **總提交數**: 11 個提交
- **檔案變更**: 約 50+ 個檔案
- **程式碼行數**: 
  - 新增: ~1,500+ 行
  - 刪除: ~750+ 行
  - 淨增加: ~750+ 行

### 主要影響區域
1. **模型層** (`inventory_api/api/models/`): 完全重構
2. **序列化器** (`inventory_api/api/v1/serializers.py`): 大幅增強
3. **測試套件** (`inventory_api/api/tests/`): 新增大量測試
4. **資料庫遷移** (`inventory_api/api/migrations/`): 重大結構變更
5. **假資料生成** (`generate_fake_data.py`): 適配新模型

### 功能模組
- ✅ **Ansible 集成**: 多對多群組關係支援
- ✅ **庫存管理**: Unit, Manufacturer, Supplier 模型
- ✅ **資源追蹤**: GPU 容量監控
- ✅ **測試覆蓋**: 綜合測試套件
- ✅ **開發工具**: Linting 和環境配置

---

## 🎯 技術影響

### 架構改善
- **模組化設計**: 從單一模型文件拆分為專業模組
- **關係靈活性**: AnsibleHost 支援多群組歸屬
- **資源完整性**: GPU 等硬體資源完整追蹤
- **供應鏈管理**: Manufacturer/Supplier 分離管理

### API 增強
- **CRUD 完整性**: 所有新模型提供完整 API 操作
- **關係處理**: 改善 ManyToMany 序列化和驗證
- **資料驗證**: 增強輸入驗證和錯誤處理

### 開發體驗
- **測試覆蓋**: 大幅提升測試覆蓋率和品質
- **程式碼品質**: 改善 linting 配置和標準
- **開發環境**: 優化 devcontainer 配置

---

## 🚀 下週展望

基於本週的重大重構，下週可能的發展方向：

1. **效能優化**: 資料庫查詢優化和索引調整
2. **API 文檔**: 更新 API 文檔以反映新的模型結構
3. **權限系統**: 實現基於角色的存取控制
4. **監控儀表板**: 建立資源使用監控介面
5. **整合測試**: 端到端測試和整合測試套件

---

**生成時間**: 2025-09-17 09:17 UTC  
**涵蓋期間**: 2025-09-10 至 2025-09-17 (7天)  
**主要貢獻者**: khchiang1121
