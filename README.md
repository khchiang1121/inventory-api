# VirtFlow

VirtFlow 是一個基於 Django REST framework 開發的虛擬化資源管理系統，提供完整的 API 介面來管理虛擬化資源。本系統專注於提供高效、靈活且可擴展的資源管理解決方案，支援多租戶環境下的虛擬化資源調度與管理。

## 核心功能

### 1. 資源管理

- **實體機管理**
  - 完整的實體機生命週期管理
  - 詳細的硬體規格追蹤
  - 機架與位置管理
  - 資源使用量監控

- **虛擬機管理**
  - 虛擬機規格定義與管理
  - 自動化資源調度
  - 多類型虛擬機支援（Control Plane、Worker Node、Management Node）
  - 即時狀態監控

- **Kubernetes 叢集管理**
  - 叢集建立與配置
  - 外掛管理系統
  - Service Mesh 整合
  - Bastion Host 關聯設定

### 2. 多租戶支援

- 租戶資源配額管理
- 獨立資源隔離
- 彈性配額調整
- 資源使用追蹤

### 3. 維護管理

- 個人維護者指派
- 維護者群組管理
- 資源維運責任劃分
- 維運記錄追蹤

## 專案架構

```text
virtflow/
├── docs/                  # 專案文件
│   ├── 設計文件/          # 系統設計相關文件
│   ├── 開發日誌/          # 開發過程記錄
│   ├── 系統文件/          # 系統配置和說明文件
│   ├── API說明文件.md     # API 使用說明
│   ├── database.md        # 資料庫設計文件
│   ├── api.md            # API 詳細文件
│   └── structure.md      # 系統結構說明
├── static/                 # 靜態文件
├── staticfiles/           # 收集的靜態文件
├── virtflow/              # Django 專案配置
│   ├── api/              # API 應用程式
│   │   ├── v1/          # API v1 版本
│   │   │   ├── views.py        # 視圖邏輯
│   │   │   ├── serializers.py  # 序列化器
│   │   │   ├── permissions.py  # 權限控制
│   │   │   └── urls.py         # URL 路由
│   │   ├── models.py    # 資料模型
│   │   ├── permissions.py  # 權限定義
│   │   ├── authentication.py  # 認證機制
│   │   └── management/   # 管理命令
│   ├── settings.py      # 專案設置
│   ├── urls.py          # 主 URL 配置
│   ├── schema.py        # API 規範配置
│   └── wsgi.py          # WSGI 配置
├── .env                   # 環境變數配置
├── docker-compose.yml     # Docker 容器配置
├── Dockerfile            # Docker 映像檔配置
├── manage.py             # Django 管理腳本
├── requirements.txt      # Python 依賴包
└── schema.yaml          # API 規範文件
```

### 核心模組說明

1. **API 模組 (virtflow/api/)**
   - 實現核心業務邏輯
   - 包含資料模型定義
   - 權限控制系統
   - 認證機制實現

2. **API v1 版本 (virtflow/api/v1/)**
   - 視圖邏輯處理
   - 資料序列化
   - 權限驗證
   - URL 路由配置

3. **文件系統 (docs/)**
   - 系統設計文件
   - API 使用說明
   - 資料庫設計文件
   - 開發日誌
   - 系統配置說明

4. **專案配置 (virtflow/)**
   - Django 專案設定
   - URL 路由配置
   - API 規範配置
   - WSGI/ASGI 配置

## 使用技術

- **後端框架**: Django 4.2+
- **API 框架**: Django REST framework 3.14+
- **資料庫**: PostgreSQL
- **API 文件**: drf-spectacular
- **認證**: Django Guardian
- **開發工具**:
  - Docker & Docker Compose
  - PgAdmin4 (資料庫管理工具)
  - pytest (測試框架)
  - mypy (型別檢查)

## 主要功能

- RESTful API 介面
- 完整的 API 文件
- 資料庫管理介面
- 權限管理系統
- 虛擬化資源管理

## 開發環境設置

1. 將專案 clone 到本地

```bash
git clone [repository-url]
cd virtflow
```

2. 設置環境變數

```bash
cp .env.example .env
# 編輯 .env 文件以設定必要的環境變數
```

3. 啟動開發環境

```bash
docker compose up -d
```

1. 安裝依賴

```bash
pip install -r requirements.txt
```

1. 執行資料庫遷移

```bash
python manage.py migrate
```

1. 啟動開發伺服器

```bash
python manage.py runserver
```

## API 文件

API 文件可以通過以下方式存取：

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`

## 測試

執行測試：

```bash
pytest
```

## 部署

專案使用 Docker 進行容器化部署，可以通過以下命令啟動：

```bash
docker-compose up -d
```

## 開發指南

1. 遵循 PEP 8 編碼規範
2. 使用 mypy 進行型別檢查
3. 撰寫單元測試
4. 更新 API 文件

## 貢獻指南

1. Fork 專案
2. 創建 Feature Branch
3. 提交變更
4. 發起 Pull Request
