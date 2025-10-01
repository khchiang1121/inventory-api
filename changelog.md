# Changelog

### 2025-10-01
- feat(models): 完成核心模型結構更新與欄位調整（僅模型已同步）
  - 涉及檔案：`inventory_api/api/models/{baremetal.py,infrastructure.py,virtual.py,users.py,scheduling_strategy.py,purchase.py}`
  - 破壞性變更：
    - 移除自定義 `UserGroup`，改用 Django 內建 `Group`
    - 多處 `related_name` 調整（例如：`baremetals` → `baremetal_groups` / `owned_baremetals`）
    - GPU 模型集中至 `infrastructure`，並修正命名與關聯
    - 若有 M2M/外鍵目標替換，可能需要資料遷移腳本
- chore/partial: 測試、URL、序列化器與視圖僅部分更新，尚未完全對齊新模型
  - 目前狀態：
    - 僅部分測試案例與路由已調整；API 請求/回應格式暫不保證穩定
  - 待辦事項：
    - 產生並應用 Django migrations
    - 同步更新 serializers/views 與對應路由
    - 全面更新測試與假資料生成器
    - 更新 API 文件與使用指引
- 風險/注意：
  - 現階段主分支可能無法通過全部測試
  - 資料庫結構需遷移，請於非生產環境先驗證

#### 涉及模組與子系統
- 模型層（已完成）：
  - `inventory_api/api/models/baremetal.py`：群組關聯改用內建 `Group`；`related_name` 調整；`BaremetalModelGPU.count` 預設值 0
  - `inventory_api/api/models/infrastructure.py`：新增/整併 GPU 能力模型（`PhysicalGPUModel`、`PhysicalGPU`）；Rack/Unit 屬性擴充（如 `unit_number`、`bgp_number`、`as_number` 等）
  - `inventory_api/api/models/virtual.py`：移除舊 GPU 定義，改用 `infrastructure` 之模型；`VirtualMachineSpecificationGPU.count` 預設值 0；K8s 關聯調整
  - `inventory_api/api/models/users.py`：移除自定義 `UserGroup`，改用 `django.contrib.auth.models.Group`
  - `inventory_api/api/models/scheduling_strategy.py`：新增 `SchedulingStrategy` 與 `SchedulingStrategyCondition`，並與 K8sCluster 串接
  - `inventory_api/api/models/purchase.py`：`PurchaseOrder`/`PurchaseRequisition`/`Supplier` 關聯與欄位調整，新增金額欄位
- API 層（部分對齊）：
  - `inventory_api/api/v1/serializers.py`：部分序列化器已適配新欄位與關聯，但仍需全面檢視
  - `inventory_api/api/v1/views.py`：部分 ViewSets 已調整 `get_serializer_class` 與查詢排序邏輯，仍需全面驗證
- 測試與資料：
  - `inventory_api/api/tests/**`：測試案例尚未全面更新以符合 `Group` 替換與 `related_name` 變更，以及基礎設施/GPU 模型調整
  - 假資料生成器：需同步 GPU 與採購領域的資料建立流程

#### 影響範圍與破壞性摘要
- 群組/授權：`UserGroup` → `Group`，需同步 serializers、views、權限策略與測試資料
- GPU 領域：模型集中與命名修正，虛擬/裸機/規格之間的關聯調整
- 基礎設施：Rack/Unit 欄位增加（如 `unit_number`、BGP/AS 編號），影響序列化器與 API 輸入/輸出
- 採購領域：`PurchaseOrder` 與 `PurchaseRequisition` 結構調整，金額欄位導入

#### 下一步行動（建議順序）
1. 產生並審閱 migrations（含資料遷移腳本，特別是 M2M/FK 目標替換）
2. 同步更新 `serializers.py` 與 `views.py`，確保 CRUD 與嵌套顯示一致
3. 全量更新 `tests/**` 與假資料生成器，確保測試綠燈
4. 調整路由與文件，標註破壞性變更與升級指南


Timeframe: 2025-08-01 → 2025-08-12

## Highlights
- **Project rename and consolidation**: VirtFlow → Inventory API (docs and configs updated)
- **Dev environment**: VS Code devcontainers, Docker, docker-compose, entrypoint, and APT/pip source management
- **Testing**: Introduced pytest, extensive test suite added, and settings refactored
- **Delivery**: GitLab CI/CD configuration and Helm chart for Kubernetes deployments
- **Platform**: Health check endpoint added; production deployment URL updated

## Detailed changes

### 2025-08-12
- **Refactor**: Rename project from VirtFlow to Inventory API and update related documentation
  - Updated: `.devcontainer/devcontainer.json`, `README.md`
  - Added: `.vscode/launch.json`

### 2025-08-11
- **Feat/Tests**: Introduce pytest config and improve test support
  - Added: `pytest.ini`, multiple tests under `virtflow/api/tests/**`
  - Changed: `virtflow/api/v1/serializers.py`, `virtflow/api/v1/views.py`, `virtflow/settings.py`
- **Chore**: Streamline devcontainer initialization and exposed ports
  - Changed: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`
- **Chore**: Add additional APT sources in devcontainer docker-compose
  - Changed: `.devcontainer/docker-compose.yml`
- **Fix**: Correct env var key in devcontainer compose (APT_SOURCE_CONTENT)
  - Changed: `.devcontainer/docker-compose.yml`

### 2025-08-09
- **Dev**: Container and compose tweaks; entrypoint improvements
  - Changed: `.devcontainer/*`, `docker-compose.yml`, `README.md`, `entrypoint.sh`
- **Data tooling**: Adjust fake data generation command
  - Changed: `virtflow/api/management/commands/generate_fake_data.py`

### 2025-08-06
- **Dev**: Improve Docker configuration for development (APT source management, pip index)
  - Changed: `.devcontainer/Dockerfile`, `.devcontainer/docker-compose.yml`
- **Dev**: Add and refine devcontainer and entrypoint
  - Added: `entrypoint.sh`
  - Changed: `.devcontainer/*`, `Dockerfile`, `docker-compose.yml`

### 2025-08-05
- **Feat**: Initial setup for Inventory API development environment with Docker and PostgreSQL
  - Added: `.devcontainer/` (Dockerfile, compose, env template, init DB SQL, proxy config, setup)

### 2025-08-01
- **Feat**: Health check endpoint for system status monitoring
  - Changed: `virtflow/urls.py`
- **Delivery**: Introduce GitLab CI/CD and Helm deployment scripts
  - Added: `.gitlab-ci.yml`, `helm/deploy.sh`, `helm/virtflow-api/**`
- **Delivery/Refactor**: Migrate Helm chart to `helm/inventory-api/**` and update production URL
  - Renamed/Added: `helm/inventory-api/**`
- **Docs**: Extensive API and design documentation added and reorganized under `docs/**`

## Stats (since 2025-08-01)
- 78 files changed, 5,947 insertions, 812 deletions
- Key areas: `.devcontainer/**`, `helm/inventory-api/**`, `virtflow/api/tests/**`, `virtflow/api/v1/{serializers,views}.py`, `virtflow/settings.py`, `virtflow/urls.py`, CI/CD and entrypoint scripts

## Contributors
- khchiang1121
