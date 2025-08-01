# Django 靜態檔案處理

## 1. 概述

本文件探討 Django 中靜態檔案（static files）的各種處理方式，包括開發與部署階段的差異、可用工具（如 WhiteNoise）、以及離線環境部署時的最佳實踐。最終將選出一個可長期維護、效能良好且可支援離線部署的方案。

---

## 2. 靜態檔案處理的基本概念

| 名稱                | 目的與用途                                                             |
|---------------------|------------------------------------------------------------------------|
| `STATIC_URL`        | 瀏覽器請求靜態資源時的 URL 前綴，例如 `/static/`                     |
| `STATICFILES_DIRS`  | Django 開發階段從哪裡找原始 static 檔案（如 favicon、JS、CSS）        |
| `STATIC_ROOT`       | `collectstatic` 收集完所有 static 後的輸出位置，供部署用              |
| `collectstatic`     | Django 指令，用來把 `STATICFILES_DIRS` 和 app 的 `static/` 統一收集    |
| `WhiteNoise`        | 可在 `DEBUG=False` 下由 Django 自行提供靜態檔案的 Middleware           |

---

## 3. 開發階段 vs 正式部署的需求差異

| 環境       | 需求                                           | 建議處理方式                                  |
|------------|------------------------------------------------|-----------------------------------------------|
| 開發環境   | 開發者能即時修改與預覽 static 資源             | 使用 `STATICFILES_DIRS` 搭配 `runserver`      |
| 正式部署   | 效能、安全、可控、離線執行                     | 使用 `collectstatic` → 配置 Web Server 或 WhiteNoise |

---

## 4. 可能方案比較

### 方案 A：使用 `runserver` + STATICFILES_DIRS 提供 static  
- ✅ 開發階段簡單好用  
- ❌ 正式環境不可用（`DEBUG=False` 無效）
- ❌ 無壓縮、無快取策略、效能低

---

### 方案 B：使用 Nginx 或 Apache 提供 STATIC_ROOT  
- ✅ 效能最佳、業界標準  
- ✅ 可整合 CDN 或硬體快取  
- ❌ 需安裝額外伺服器  
- ❌ 對小型部署或離線環境較繁瑣

---

### 方案 C：使用 WhiteNoise + `CompressedManifestStaticFilesStorage`  
- ✅ 不需 Nginx，部署簡單  
- ✅ 自動 gzip 壓縮 + hashed 檔名快取破壞  
- ✅ 適合 Docker / 離線部署 / 單機部署  
- ⚠️ 仍需 `collectstatic`，產出結果才能使用

---

## 5. 離線環境的特殊考量

- collectstatic **完全不需網路**
- 所有 static 檔案需預先準備於 `STATICFILES_DIRS` 或 app static 中
- 建議將 `STATIC_ROOT` 打包後佈署到目標環境（tarball）

---

## 6. 最終選擇的方案：方案 C — WhiteNoise + collectstatic

### 🎯 選擇理由：

- ✔ 無需外部 Web Server，降低部署門檻
- ✔ 支援 `DEBUG=False` 的正式環境
- ✔ 預壓縮、自動版本控管、適合 immutable 檔案部署策略
- ✔ 完全支援離線部署，只需打包 `STATIC_ROOT`

---

### ✅ 最終設定：

```python
# settings.py

STATIC_URL = '/static/'

# 靜態原始檔案來源（開發用）
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# collectstatic 的輸出位置（部署用）
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 使用 WhiteNoise 提供壓縮 + 哈希命名
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

### ✅ 執行部署流程：

```bash
python manage.py collectstatic
```

然後即可使用 `gunicorn` + WhiteNoise 啟動應用程式：

```bash
gunicorn your_project.wsgi:application
```

---

## 7. 總結

| 項目                 | 選擇                      |
|----------------------|---------------------------|
| static 資源來源       | `static/`（開發用）        |
| static 資源輸出       | `staticfiles/`（部署用）   |
| 提供靜態檔案的方式   | WhiteNoise Middleware     |
| 是否支援離線部署     | ✅ 完全支援                 |
| 是否需搭配 Nginx     | ❌ 無需                     |

---
