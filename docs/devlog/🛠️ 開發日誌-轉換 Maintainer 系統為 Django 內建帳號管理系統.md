# 🛠️ 開發日誌：轉換 Maintainer 系統為 Django 內建帳號管理系統

## 🗓️ 日期

2025-03-30

## 📘 背景

原專案中，我們設計了一組自訂模型 `Maintainer` 與 `MaintainerGroup`，分別對應使用者與群組的基本功能，並以 `ManyToMany` 管理成員關係。

然而，在實作使用者認證、權限管理等功能時，發現 Django 已內建 `User` 與 `Group` 模型，且整合了認證、授權、後台管理、API token 等功能。為了未來擴充性與維護效率，我們決定重構這一部分的邏輯，改為使用 Django 內建模型，並透過 `AbstractUser` 擴充我們原本在 `Maintainer` 中的欄位。

---

## 🎯 轉換目標

1. 使用 Django 內建的 `User` 替代 `Maintainer`
2. 使用 Django 內建的 `Group` 替代 `MaintainerGroup`
3. 將原有欄位遷移為 `CustomUser` 模型擴充屬性
4. 保留「群組管理員」、「成員」等關聯邏輯

---

## 🔍 問題分析

### 為什麼要放棄自訂的 `Maintainer` 模型？

| 問題點 | 說明 |
|--------|------|
| 認證整合困難 | 若用自訂模型，需自行整合 Django 的登入/註冊/Auth 機制 |
| 權限系統重複造輪子 | Django 的 `User` + `Permission` + `Group` 已內建 RBAC 架構 |
| 無法使用 Django Admin 原生支援 | 自訂模型需要額外註冊與自定義表單，維護成本高 |
| 第三方套件不易整合 | DRF、django-allauth、simplejwt 等套件都預設依賴 `auth.User` |

---

## ✅ 解決方案

### Step 1️⃣：使用 `AbstractUser` 自訂使用者

我們定義一個 `CustomUser`，並補上 `Maintainer` 原有欄位：

```python
# virtflow/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, help_text="Full name of the maintainer")
    account = models.CharField(max_length=32, unique=True, help_text="Unique account identifier")
    status = models.CharField(
        max_length=32,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active',
        help_text="Account status"
    )
```

```python
# settings.py
AUTH_USER_MODEL = 'inventory_api.CustomUser'
```

---

### Step 2️⃣：使用 `Group` 與中介模型，補足原 `MaintainerGroup` 欄位

原先 `MaintainerGroup` 模型有額外欄位如 `description`, `status`, `group_manager`，這些不是 Django 預設的 `Group` 欄位。

因此我們建立一個擴充關聯模型 `GroupProfile` 來補充這些資訊。

```python
# accounts/models.py
from django.contrib.auth.models import Group
from django.conf import settings

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='profile')
    group_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_groups')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
```

這樣一來，群組的管理員與狀態資訊就能與 `Group` 綁定，同時保有 Django 原有的群組權限機制。

---

## 🚀 轉換效益

| 效益項目 | 說明 |
|----------|------|
| 更簡潔的登入/註冊流程 | 可直接使用 Django 提供的認證系統與 view |
| 內建權限整合 | 使用 `permissions`, `groups`, `is_staff` 等欄位更方便做 RBAC 控管 |
| Django Admin 支援良好 | 可無縫管理使用者與群組 |
| 易於與 DRF 和其他套件整合 | 例如 `SimpleJWT`, `django-allauth`, `drf-nested-routers` 等 |
| 可擴展性高 | 若未來需支援 OAuth2、LDAP、SSO，更容易整合 |

---

## 📝 未來待辦

- [ ] 將原資料轉移到新的 CustomUser 表
- [ ] 補上對應的 serializer 和 viewset
- [ ] 單元測試驗證使用者登入、權限分派與群組管理
- [ ] 管理員後台調整 admin 註冊欄位展示

---

## 👋 結語

這次的轉換雖然需要調整部分資料模型與程式邏輯，但換來的是更穩定、更可擴充的使用者管理系統。原本自行設計的 `Maintainer` 模型其實與 Django 內建的 `User` 概念幾乎一致，未來遇到類似需求可直接從 Django 內建模組延伸與擴充，避免重複造輪子。

---