# 🧩 Django REST Framework：API 版本管理技術文件

## 🎯 文件目標

本文件旨在探討 Django REST Framework (DRF) 中常見的 **API 版本控制策略**，並說明本專案採用的實作方式：**一個 Django App、以資料夾分隔版本**、**共用資料庫模型**。  
我們將對各種方法進行比較與優劣分析，最後評估並肯定目前實作架構的可行性與擴充性。

## 🧠 為什麼要版本化 API？

- 防止前端或外部使用者因 API 更新而發生相容性問題
- 支援平行開發與漸進式遷移
- 保持舊版穩定，同時推進新版功能

## 📦 API 版本化的常見策略

| 策略 | 範例路徑 | 優點 | 缺點 |
|------|----------|------|------|
| 1️⃣ 路徑版本 (URL Path Versioning) | `/api/v1/resource/` | 簡單明瞭、最常見 | URL 改變，需配合前端調整 |
| 2️⃣ 查詢參數版本 (Query Param) | `/api/resource/?version=1` | 無需更改路徑 | 難以快取，較不常見 |
| 3️⃣ Header 版本 (Accept Header) | `Accept: application/json; version=1.0` | URL 乾淨，彈性高 | 需額外處理 header，前端支援複雜 |
| 4️⃣ Hostname 版本 | `v1.api.example.com` | 完全分離流量 | 運維成本高 |

➡️ **本專案採用**：**URL Path Versioning**


## ✅ 各種 Django 架構實作方式

### 方案 A：多個 Django App（每個版本一個 App）

```
apps/
├── api_v1/
│   ├── views.py
│   ├── urls.py
├── api_v2/
│   ├── views.py
│   ├── urls.py
```

**優點**：
- 完全獨立，互不干擾
- 各版本可定義獨立模型、序列化器

**缺點**：
- 程式碼重複性高
- App 複雜度高，不利於維護

---

### 方案 B：一個 App，使用條件式路由切換版本

```python
# urls.py
if request.version == 'v1':
    return v1_view
else:
    return v2_view
```

**優點**：
- 集中管理

**缺點**：
- 複雜度高，難以模組化
- 不符合 Django routing 模型

---

### ✅ 方案 C：一個 App + 不同資料夾（目錄）管理版本 ← **本專案採用**

```
virtflow/
├── api/
│   ├── apps.py
│   ├── models.py
│   ├── v1/
│   │   ├── urls.py
│   │   ├── views.py
│   ├── v2/
│   │   ├── urls.py
│   │   ├── views.py
```

### 🔧 對應 `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'virtflow.api',
]
```

### 🔧 對應 URLConf

```python
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^api/v1/', include(('virtflow.api.v1.urls', 'v1'), namespace='v1')),
    re_path(r'^api/v2/', include(('virtflow.api.v2.urls', 'v2'), namespace='v2')),
]
```

### 🔧 子版本 urls.py

```python
# virtflow/api/v1/urls.py
from django.urls import path
from .views import HelloV1View

app_name = 'v1'

urlpatterns = [
    path('hello/', HelloV1View.as_view(), name='hello'),
]
```

---

## 🔄 API 各版本是否共用資料模型（Model）

在多版本 API 架構中，我們需要考量：**每個 API 版本是否使用相同的 Django Model。**

### 🧰 本專案策略：共用單一 Model 層

本專案中，**所有版本的 API 均共用相同的資料模型（Model）**，具體做法如下：

- Model 統一定義於 `virtflow.api.models`
- 不隨 API 版本變化而複製或分支
- 各版本的行為差異由 View 和 Serializer 層進行封裝與裁切，而非透過重建 Model 處理

### ✅ 為何推薦共用 Model？（通用原則）

在大多數 Django 專案中，所有 API 版本通常會共用同一套 Model。其主要原因包括：

- Model 是資料庫的核心結構，通常設計為**業務邏輯的單一來源（Single Source of Truth）**
- 避免不同版本分離 Model 所產生的 migration 管理混亂與資料結構衝突
- 降低維護成本與開發風險，確保資料一致性

在實務上，多數 API 的變更都發生在資料輸出格式與行為邏輯層，而非底層資料結構，因此將版本差異限制在更上層的設計（如 Serializer 與 View）更加穩定與彈性。

### 🧱 各層級的版本差異管理建議

| 架構層級 | 是否版本獨立 | 處理策略 |
|----------|----------------|------------|
| **Model** | 否（共用） | 保持資料結構一致，單一維護 |
| **Serializer** | ✅ 是 | 控制欄位顯示、格式轉換、欄位邏輯差異 |
| **View / ViewSet** | ⚠️ 可選擇 | 視需求建立獨立邏輯處理 |
| **Routing** | ✅ 是 | 使用不同路由或 namespace 隔離版本 |
| **Schema（文件）** | ✅ 是 | 為每個版本分別產生 OpenAPI 文件，避免混淆 |

### 📊 共用 Model vs 分開 Model：完整評估比較

| 評估面向 | 共用 Model（本專案做法） | 分開 Model（每版定義一次） |
|----------|---------------------------|-----------------------------|
| ✅ 維護成本 | 低，單一模型管理 | 高，每版變更需同步更新 |
| ✅ 資料一致性 | 高，資料表結構統一 | 易造成版本間結構差異 |
| ✅ 相容性維護 | 較容易維持向前/向後相容 | 高風險造成跨版不一致 |
| ✅ 架構簡潔性 | 簡潔直觀，降低重複邏輯 | 架構複雜、測試難度上升 |
| ⚠️ 客製欄位邏輯 | 需透過 Serializer 或 View 分層處理 | 可直接修改 Model，但不利於共用 |
| ⚠️ 資料表實驗性需求 | 難以做資料結構 A/B 測試 | 易分支結構測試，但需額外控管資料同步 |

### 🔄 模型變更與版本演進策略
若模型本身需要修改（例如欄位移除或新增），應遵循以下策略：
- **優先保持向後相容**：避免直接刪除欄位，可透過 Serializer 控制欄位是否暴露於 API
- **版本內部欄位管理**：可於新版 Serializer 中引入新欄位，但在舊版中保持隱藏
- **明確文件與版本紀錄**：搭配 changelog 或版本說明標示差異，便於開發協作與 API 使用者理解

### 🧠 結論建議

綜合考量維護性、資料一致性與架構穩定性，建議遵循以下實務原則：

- **90% 情況下應共用 Model**，版本差異應透過 Serializer 與 View 層處理
- 僅在**資料表結構有重大變更或行為邏輯無法共存**的情況下，才考慮為新版本建立新 Model
- 建立良好的欄位演進策略與文件版本管理，是維持多版本穩定運作的關鍵

目前本專案採用的「**共用 Model，版本差異透過上層封裝處理**」策略，具備以下優勢：

- ✅ 維護簡單性
- ✅ 資料一致性
- ✅ 架構可預測性與彈性
- ✅ 支援未來版本擴展

## 📌 總結

本專案選擇 **單一 Django App、依資料夾區分版本的 URL Path Versioning** 架構，具有：

- 模組化程度高
- 清晰可擴展的結構
- 支援 DRF 所有功能（如 ViewSet、Router、Versioning 類別）
- 共用 Model 策略，簡化維護、提高一致性
