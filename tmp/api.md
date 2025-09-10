# Backend API Specification

**版本：** 1.0.0  
**更新日期：** 2025-03-09

## 1. 概述

本 API 提供系統中所有資源（例如：個人維護者、維護者群組、維護者群組成員、資源維護者、實體機、實體機群組、租戶、虛擬機、虛擬機規格、k8s 叢集、群組租戶授權）之存取與管理功能。所有請求均需附上授權認證，並使用 JSON 格式傳遞資料。

## 2. 認證與授權

- **認證機制：** 所有 API 請求必須於 HTTP Header 中帶入有效的 API Token。
- **Header 格式：**
  ```json
  {
    "Authorization": "Bearer <token>"
  }
  ```

## 3. 全域錯誤回應格式

當發生錯誤時，回應將依下列格式返回：
```json
{
  "error": "錯誤訊息",
  "code": "錯誤代碼"
}
```

## 4. API 端點

以下依照資源類型列出所有完整端點，包括建立、查詢（列表與單筆）、更新與刪除。


### 4.1 個人維護者（Maintainer）

#### 4.1.1 建立個人維護者
- **HTTP 方法：** POST  
- **URL：** `/maintainers`  
- **Request：**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "status": "active",
    "created_at": "2025-03-09T10:00:00Z",
    "updated_at": "2025-03-09T10:00:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.1.2 查詢個人維護者列表
- **HTTP 方法：** GET  
- **URL：** `/maintainers`  
- **Query Parameters（可選）：** `page`、`per_page`  
- **Response：**
  ```json
    [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "status": "active",
        "created_at": "2025-03-09T10:00:00Z",
        "updated_at": "2025-03-09T10:00:00Z"
      },
    ]
 
  ```
- **狀態碼：** 200 OK

#### 4.1.3 查詢單一個人維護者
- **HTTP 方法：** GET  
- **URL：** `/maintainers/{id}`  
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "status": "active",
    "created_at": "2025-03-09T10:00:00Z",
    "updated_at": "2025-03-09T10:00:00Z"
  }
  ```
- **狀態碼：** 200 OK（若無此資源則返回 404 Not Found）

#### 4.1.4 更新個人維護者
- **HTTP 方法：** PUT  
- **URL：** `/maintainers/{id}`  
- **Request：**
  ```json
  {
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "status": "active",
    "created_at": "2025-03-09T10:00:00Z",
    "updated_at": "2025-03-09T11:00:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.1.5 刪除個人維護者
- **HTTP 方法：** DELETE  
- **URL：** `/maintainers/{id}`  
- **Response：**
  ```json
  {
    "message": "Maintainer deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.2 維護者群組（MaintainerGroup）

#### 4.2.1 建立維護者群組
- **HTTP 方法：** POST  
- **URL：** `/maintainer-groups`  
- **Request：**
  ```json
  {
    "name": "Ops Team",
    "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "跨部門運維團隊",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "name": "Ops Team",
    "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "跨部門運維團隊",
    "status": "active",
    "created_at": "2025-03-09T10:05:00Z",
    "updated_at": "2025-03-09T10:05:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.2.2 查詢維護者群組列表
- **HTTP 方法：** GET  
- **URL：** `/maintainer-groups`  
- **Response：**
  ```json
  {
    "maintainer_groups": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440111",
        "name": "Ops Team",
        "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
        "description": "跨部門運維團隊",
        "status": "active",
        "created_at": "2025-03-09T10:05:00Z",
        "updated_at": "2025-03-09T10:05:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.2.3 查詢單一維護者群組
- **HTTP 方法：** GET  
- **URL：** `/maintainer-groups/{id}`  
- **Response：**
  ```json
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "name": "Ops Team",
    "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "跨部門運維團隊",
    "status": "active",
    "created_at": "2025-03-09T10:05:00Z",
    "updated_at": "2025-03-09T10:05:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.2.4 更新維護者群組
- **HTTP 方法：** PUT  
- **URL：** `/maintainer-groups/{id}`  
- **Request：**
  ```json
  {
    "name": "Ops Team Updated",
    "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "更新後的跨部門運維團隊說明",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "name": "Ops Team Updated",
    "group_manager_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "更新後的跨部門運維團隊說明",
    "status": "active",
    "created_at": "2025-03-09T10:05:00Z",
    "updated_at": "2025-03-09T11:05:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.2.5 刪除維護者群組
- **HTTP 方法：** DELETE  
- **URL：** `/maintainer-groups/{id}`  
- **Response：**
  ```json
  {
    "message": "Maintainer group deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.3 維護者群組成員（MaintainerGroupMember）

#### 4.3.1 建立維護者群組成員關聯
- **HTTP 方法：** POST  
- **URL：** `/maintainer-group-members`  
- **Request：**
  ```json
  {
    "group_id": "660e8400-e29b-41d4-a716-446655440111",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response：**
  ```json
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "group_id": "660e8400-e29b-41d4-a716-446655440111",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:10:00Z",
    "updated_at": "2025-03-09T10:10:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.3.2 查詢維護者群組成員列表
- **HTTP 方法：** GET  
- **URL：** `/maintainer-group-members`  
- **Response：**
  ```json
  {
    "maintainer_group_members": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440222",
        "group_id": "660e8400-e29b-41d4-a716-446655440111",
        "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_at": "2025-03-09T10:10:00Z",
        "updated_at": "2025-03-09T10:10:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.3.3 查詢單一維護者群組成員
- **HTTP 方法：** GET  
- **URL：** `/maintainer-group-members/{id}`  
- **Response：**
  ```json
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "group_id": "660e8400-e29b-41d4-a716-446655440111",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:10:00Z",
    "updated_at": "2025-03-09T10:10:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.3.4 更新維護者群組成員關聯
- **HTTP 方法：** PUT  
- **URL：** `/maintainer-group-members/{id}`  
- **Request：**
  ```json
  {
    "group_id": "660e8400-e29b-41d4-a716-446655440111",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response：**
  ```json
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "group_id": "660e8400-e29b-41d4-a716-446655440111",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:10:00Z",
    "updated_at": "2025-03-09T11:10:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.3.5 刪除維護者群組成員關聯
- **HTTP 方法：** DELETE  
- **URL：** `/maintainer-group-members/{id}`  
- **Response：**
  ```json
  {
    "message": "Maintainer group member deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.4 資源維護者關聯（ResourceMaintainer）

#### 4.4.1 建立資源維護者關聯
- **HTTP 方法：** POST  
- **URL：** `/resource-maintainers`  
- **Request：**
  ```json
  {
    "resource_type": "Baremetal",
    "resource_id": "550e8400-e29b-41d4-a716-446655440333",
    "maintainer_type": "individual",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response：**
  ```json
  {
    "id": "880e8400-e29b-41d4-a716-446655440444",
    "resource_type": "Baremetal",
    "resource_id": "550e8400-e29b-41d4-a716-446655440333",
    "maintainer_type": "individual",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:15:00Z",
    "updated_at": "2025-03-09T10:15:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.4.2 查詢資源維護者關聯列表
- **HTTP 方法：** GET  
- **URL：** `/resource-maintainers`  
- **Response：**
  ```json
  {
    "resource_maintainers": [
      {
        "id": "880e8400-e29b-41d4-a716-446655440444",
        "resource_type": "Baremetal",
        "resource_id": "550e8400-e29b-41d4-a716-446655440333",
        "maintainer_type": "individual",
        "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_at": "2025-03-09T10:15:00Z",
        "updated_at": "2025-03-09T10:15:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.4.3 查詢單一資源維護者關聯
- **HTTP 方法：** GET  
- **URL：** `/resource-maintainers/{id}`  
- **Response：**
  ```json
  {
    "id": "880e8400-e29b-41d4-a716-446655440444",
    "resource_type": "Baremetal",
    "resource_id": "550e8400-e29b-41d4-a716-446655440333",
    "maintainer_type": "individual",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:15:00Z",
    "updated_at": "2025-03-09T10:15:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.4.4 更新資源維護者關聯
- **HTTP 方法：** PUT  
- **URL：** `/resource-maintainers/{id}`  
- **Request：**
  ```json
  {
    "resource_type": "Baremetal",
    "resource_id": "550e8400-e29b-41d4-a716-446655440333",
    "maintainer_type": "individual",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response：**
  ```json
  {
    "id": "880e8400-e29b-41d4-a716-446655440444",
    "resource_type": "Baremetal",
    "resource_id": "550e8400-e29b-41d4-a716-446655440333",
    "maintainer_type": "individual",
    "maintainer_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-03-09T10:15:00Z",
    "updated_at": "2025-03-09T11:15:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.4.5 刪除資源維護者關聯
- **HTTP 方法：** DELETE  
- **URL：** `/resource-maintainers/{id}`  
- **Response：**
  ```json
  {
    "message": "Resource maintainer association deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.5 實體機（Baremetal）

#### 4.5.1 建立實體機
- **HTTP 方法：** POST  
- **URL：** `/hosts`  
- **Request：**
  ```json
  {
    "name": "Server A",
    "status": "running",
    "total_cpu": 16,
    "total_memory": 32768,
    "total_storage": 1024,
    "available_cpu": 16,
    "available_memory": 32768,
    "available_storage": 1024,
    "group_id": 1,
    "region": "北區",
    "dc": "DC1",
    "room": "Room 101",
    "rack": "Rack 5",
    "external_system_id": "OLD-1234"
  }
  ```
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440333",
    "name": "Server A",
    "status": "running",
    "total_cpu": 16,
    "total_memory": 32768,
    "total_storage": 1024,
    "available_cpu": 16,
    "available_memory": 32768,
    "available_storage": 1024,
    "group_id": 1,
    "region": "北區",
    "dc": "DC1",
    "room": "Room 101",
    "rack": "Rack 5",
    "external_system_id": "OLD-1234",
    "created_at": "2025-03-09T10:20:00Z",
    "updated_at": "2025-03-09T10:20:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.5.2 查詢實體機列表
- **HTTP 方法：** GET  
- **URL：** `/hosts`  
- **Response：**
  ```json
  {
    "hosts": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440333",
        "name": "Server A",
        "status": "running",
        "total_cpu": 16,
        "total_memory": 32768,
        "total_storage": 1024,
        "available_cpu": 16,
        "available_memory": 32768,
        "available_storage": 1024,
        "group_id": 1,
        "region": "北區",
        "dc": "DC1",
        "room": "Room 101",
        "rack": "Rack 5",
        "external_system_id": "OLD-1234",
        "created_at": "2025-03-09T10:20:00Z",
        "updated_at": "2025-03-09T10:20:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.5.3 查詢單一實體機
- **HTTP 方法：** GET  
- **URL：** `/hosts/{id}`  
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440333",
    "name": "Server A",
    "status": "running",
    "total_cpu": 16,
    "total_memory": 32768,
    "total_storage": 1024,
    "available_cpu": 16,
    "available_memory": 32768,
    "available_storage": 1024,
    "group_id": 1,
    "region": "北區",
    "dc": "DC1",
    "room": "Room 101",
    "rack": "Rack 5",
    "external_system_id": "OLD-1234",
    "created_at": "2025-03-09T10:20:00Z",
    "updated_at": "2025-03-09T10:20:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.5.4 更新實體機
- **HTTP 方法：** PUT  
- **URL：** `/hosts/{id}`  
- **Request：**
  ```json
  {
    "name": "Server A Updated",
    "status": "maintenance",
    "total_cpu": 16,
    "total_memory": 32768,
    "total_storage": 1024,
    "available_cpu": 14,
    "available_memory": 30000,
    "available_storage": 900,
    "group_id": 1,
    "region": "北區",
    "dc": "DC1",
    "room": "Room 101",
    "rack": "Rack 5",
    "external_system_id": "OLD-1234"
  }
  ```
- **Response：**
  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440333",
    "name": "Server A Updated",
    "status": "maintenance",
    "total_cpu": 16,
    "total_memory": 32768,
    "total_storage": 1024,
    "available_cpu": 14,
    "available_memory": 30000,
    "available_storage": 900,
    "group_id": 1,
    "region": "北區",
    "dc": "DC1",
    "room": "Room 101",
    "rack": "Rack 5",
    "external_system_id": "OLD-1234",
    "created_at": "2025-03-09T10:20:00Z",
    "updated_at": "2025-03-09T11:20:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.5.5 刪除實體機
- **HTTP 方法：** DELETE  
- **URL：** `/hosts/{id}`  
- **Response：**
  ```json
  {
    "message": "Baremetal deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.6 實體機群組（BaremetalGroup）

#### 4.6.1 建立實體機群組
- **HTTP 方法：** POST  
- **URL：** `/host-groups`  
- **Request：**
  ```json
  {
    "name": "Group 1",
    "description": "主機分組說明",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Group 1",
    "description": "主機分組說明",
    "status": "active",
    "created_at": "2025-03-09T10:25:00Z",
    "updated_at": "2025-03-09T10:25:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.6.2 查詢實體機群組列表
- **HTTP 方法：** GET  
- **URL：** `/host-groups`  
- **Response：**
  ```json
  {
    "host_groups": [
      {
        "id": 1,
        "name": "Group 1",
        "description": "主機分組說明",
        "status": "active",
        "created_at": "2025-03-09T10:25:00Z",
        "updated_at": "2025-03-09T10:25:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.6.3 查詢單一實體機群組
- **HTTP 方法：** GET  
- **URL：** `/host-groups/{id}`  
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Group 1",
    "description": "主機分組說明",
    "status": "active",
    "created_at": "2025-03-09T10:25:00Z",
    "updated_at": "2025-03-09T10:25:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.6.4 更新實體機群組
- **HTTP 方法：** PUT  
- **URL：** `/host-groups/{id}`  
- **Request：**
  ```json
  {
    "name": "Group 1 Updated",
    "description": "更新後的分組說明",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Group 1 Updated",
    "description": "更新後的分組說明",
    "status": "active",
    "created_at": "2025-03-09T10:25:00Z",
    "updated_at": "2025-03-09T11:25:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.6.5 刪除實體機群組
- **HTTP 方法：** DELETE  
- **URL：** `/host-groups/{id}`  
- **Response：**
  ```json
  {
    "message": "Baremetal group deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.7 租戶（Tenant）

#### 4.7.1 建立租戶
- **HTTP 方法：** POST  
- **URL：** `/tenants`  
- **Request：**
  ```json
  {
    "name": "Tenant A",
    "description": "租戶說明",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Tenant A",
    "description": "租戶說明",
    "status": "active",
    "created_at": "2025-03-09T10:30:00Z",
    "updated_at": "2025-03-09T10:30:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.7.2 查詢租戶列表
- **HTTP 方法：** GET  
- **URL：** `/tenants`  
- **Response：**
  ```json
  {
    "tenants": [
      {
        "id": 1,
        "name": "Tenant A",
        "description": "租戶說明",
        "status": "active",
        "created_at": "2025-03-09T10:30:00Z",
        "updated_at": "2025-03-09T10:30:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.7.3 查詢單一租戶
- **HTTP 方法：** GET  
- **URL：** `/tenants/{id}`  
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Tenant A",
    "description": "租戶說明",
    "status": "active",
    "created_at": "2025-03-09T10:30:00Z",
    "updated_at": "2025-03-09T10:30:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.7.4 更新租戶
- **HTTP 方法：** PUT  
- **URL：** `/tenants/{id}`  
- **Request：**
  ```json
  {
    "name": "Tenant A Updated",
    "description": "更新後的租戶說明",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": 1,
    "name": "Tenant A Updated",
    "description": "更新後的租戶說明",
    "status": "active",
    "created_at": "2025-03-09T10:30:00Z",
    "updated_at": "2025-03-09T11:30:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.7.5 刪除租戶
- **HTTP 方法：** DELETE  
- **URL：** `/tenants/{id}`  
- **Response：**
  ```json
  {
    "message": "Tenant deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.8 虛擬機（VirtualMachine）

#### 4.8.1 建立虛擬機
- **HTTP 方法：** POST  
- **URL：** `/virtual-machines`  
- **Request：**
  ```json
  {
    "name": "VM-01",
    "tenant_id": 1,
    "host_id": "550e8400-e29b-41d4-a716-446655440333",
    "specification_id": "990e8400-e29b-41d4-a716-446655440555",
    "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
    "status": "creating"
  }
  ```
- **Response：**
  ```json
  {
    "id": "bb0e8400-e29b-41d4-a716-446655440777",
    "name": "VM-01",
    "tenant_id": 1,
    "host_id": "550e8400-e29b-41d4-a716-446655440333",
    "specification_id": "990e8400-e29b-41d4-a716-446655440555",
    "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
    "status": "creating",
    "created_at": "2025-03-09T10:35:00Z",
    "updated_at": "2025-03-09T10:35:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.8.2 查詢虛擬機列表
- **HTTP 方法：** GET  
- **URL：** `/virtual-machines`  
- **Response：**
  ```json
  {
    "virtual_machines": [
      {
        "id": "bb0e8400-e29b-41d4-a716-446655440777",
        "name": "VM-01",
        "tenant_id": 1,
        "host_id": "550e8400-e29b-41d4-a716-446655440333",
        "specification_id": "990e8400-e29b-41d4-a716-446655440555",
        "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
        "status": "creating",
        "created_at": "2025-03-09T10:35:00Z",
        "updated_at": "2025-03-09T10:35:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.8.3 查詢單一虛擬機
- **HTTP 方法：** GET  
- **URL：** `/virtual-machines/{id}`  
- **Response：**
  ```json
  {
    "id": "bb0e8400-e29b-41d4-a716-446655440777",
    "name": "VM-01",
    "tenant_id": 1,
    "host_id": "550e8400-e29b-41d4-a716-446655440333",
    "specification_id": "990e8400-e29b-41d4-a716-446655440555",
    "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
    "status": "creating",
    "created_at": "2025-03-09T10:35:00Z",
    "updated_at": "2025-03-09T10:35:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.8.4 更新虛擬機
- **HTTP 方法：** PUT  
- **URL：** `/virtual-machines/{id}`  
- **Request：**
  ```json
  {
    "name": "VM-01 Updated",
    "tenant_id": 1,
    "host_id": "550e8400-e29b-41d4-a716-446655440333",
    "specification_id": "990e8400-e29b-41d4-a716-446655440555",
    "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
    "status": "running"
  }
  ```
- **Response：**
  ```json
  {
    "id": "bb0e8400-e29b-41d4-a716-446655440777",
    "name": "VM-01 Updated",
    "tenant_id": 1,
    "host_id": "550e8400-e29b-41d4-a716-446655440333",
    "specification_id": "990e8400-e29b-41d4-a716-446655440555",
    "k8s_cluster_id": "aa0e8400-e29b-41d4-a716-446655440666",
    "status": "running",
    "created_at": "2025-03-09T10:35:00Z",
    "updated_at": "2025-03-09T11:35:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.8.5 刪除虛擬機
- **HTTP 方法：** DELETE  
- **URL：** `/virtual-machines/{id}`  
- **Response：**
  ```json
  {
    "message": "Virtual machine deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.9 虛擬機規格（VMSpecification）

#### 4.9.1 建立虛擬機規格
- **HTTP 方法：** POST  
- **URL：** `/vm-specifications`  
- **Request：**
  ```json
  {
    "name": "Standard Spec",
    "required_cpu": 4,
    "required_memory": 8192,
    "required_storage": 100
  }
  ```
- **Response：**
  ```json
  {
    "id": "990e8400-e29b-41d4-a716-446655440555",
    "name": "Standard Spec",
    "required_cpu": 4,
    "required_memory": 8192,
    "required_storage": 100,
    "created_at": "2025-03-09T10:40:00Z",
    "updated_at": "2025-03-09T10:40:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.9.2 查詢虛擬機規格列表
- **HTTP 方法：** GET  
- **URL：** `/vm-specifications`  
- **Response：**
  ```json
  {
    "vm_specifications": [
      {
        "id": "990e8400-e29b-41d4-a716-446655440555",
        "name": "Standard Spec",
        "required_cpu": 4,
        "required_memory": 8192,
        "required_storage": 100,
        "created_at": "2025-03-09T10:40:00Z",
        "updated_at": "2025-03-09T10:40:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.9.3 查詢單一虛擬機規格
- **HTTP 方法：** GET  
- **URL：** `/vm-specifications/{id}`  
- **Response：**
  ```json
  {
    "id": "990e8400-e29b-41d4-a716-446655440555",
    "name": "Standard Spec",
    "required_cpu": 4,
    "required_memory": 8192,
    "required_storage": 100,
    "created_at": "2025-03-09T10:40:00Z",
    "updated_at": "2025-03-09T10:40:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.9.4 更新虛擬機規格
- **HTTP 方法：** PUT  
- **URL：** `/vm-specifications/{id}`  
- **Request：**
  ```json
  {
    "name": "Standard Spec Updated",
    "required_cpu": 4,
    "required_memory": 8192,
    "required_storage": 120
  }
  ```
- **Response：**
  ```json
  {
    "id": "990e8400-e29b-41d4-a716-446655440555",
    "name": "Standard Spec Updated",
    "required_cpu": 4,
    "required_memory": 8192,
    "required_storage": 120,
    "created_at": "2025-03-09T10:40:00Z",
    "updated_at": "2025-03-09T11:40:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.9.5 刪除虛擬機規格
- **HTTP 方法：** DELETE  
- **URL：** `/vm-specifications/{id}`  
- **Response：**
  ```json
  {
    "message": "VM specification deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.10 k8s 叢集（K8sCluster）

#### 4.10.1 建立 k8s 叢集
- **HTTP 方法：** POST  
- **URL：** `/k8s-clusters`  
- **Request：**
  ```json
  {
    "name": "Cluster A",
    "tenant_id": 1,
    "description": "k8s 叢集描述",
    "status": "active"
  }
  ```
- **Response：**
  ```json
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440666",
    "name": "Cluster A",
    "tenant_id": 1,
    "description": "k8s 叢集描述",
    "status": "active",
    "created_at": "2025-03-09T10:45:00Z",
    "updated_at": "2025-03-09T10:45:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.10.2 查詢 k8s 叢集列表
- **HTTP 方法：** GET  
- **URL：** `/k8s-clusters`  
- **Response：**
  ```json
  {
    "k8s_clusters": [
      {
        "id": "aa0e8400-e29b-41d4-a716-446655440666",
        "name": "Cluster A",
        "tenant_id": 1,
        "description": "k8s 叢集描述",
        "status": "active",
        "created_at": "2025-03-09T10:45:00Z",
        "updated_at": "2025-03-09T10:45:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.10.3 查詢單一 k8s 叢集
- **HTTP 方法：** GET  
- **URL：** `/k8s-clusters/{id}`  
- **Response：**
  ```json
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440666",
    "name": "Cluster A",
    "tenant_id": 1,
    "description": "k8s 叢集描述",
    "status": "active",
    "created_at": "2025-03-09T10:45:00Z",
    "updated_at": "2025-03-09T10:45:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.10.4 更新 k8s 叢集
- **HTTP 方法：** PUT  
- **URL：** `/k8s-clusters/{id}`  
- **Request：**
  ```json
  {
    "name": "Cluster A Updated",
    "tenant_id": 1,
    "description": "更新後的 k8s 叢集描述",
    "status": "maintenance"
  }
  ```
- **Response：**
  ```json
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440666",
    "name": "Cluster A Updated",
    "tenant_id": 1,
    "description": "更新後的 k8s 叢集描述",
    "status": "maintenance",
    "created_at": "2025-03-09T10:45:00Z",
    "updated_at": "2025-03-09T11:45:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.10.5 刪除 k8s 叢集
- **HTTP 方法：** DELETE  
- **URL：** `/k8s-clusters/{id}`  
- **Response：**
  ```json
  {
    "message": "K8s cluster deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

### 4.11 群組租戶授權（BaremetalGroupTenantQuota）

#### 4.11.1 建立群組租戶授權
- **HTTP 方法：** POST  
- **URL：** `/host-group-tenant-quotas`  
- **Request：**
  ```json
  {
    "group_id": 1,
    "tenant_id": 1,
    "cpu_quota_percentage": 40.0,
    "memory_quota": 16384,
    "storage_quota": 500
  }
  ```
- **Response：**
  ```json
  {
    "id": "cc0e8400-e29b-41d4-a716-446655440888",
    "group_id": 1,
    "tenant_id": 1,
    "cpu_quota_percentage": 40.0,
    "memory_quota": 16384,
    "storage_quota": 500,
    "created_at": "2025-03-09T10:50:00Z",
    "updated_at": "2025-03-09T10:50:00Z"
  }
  ```
- **狀態碼：** 201 Created

#### 4.11.2 查詢群組租戶授權列表
- **HTTP 方法：** GET  
- **URL：** `/host-group-tenant-quotas`  
- **Response：**
  ```json
  {
    "host_group_tenant_quotas": [
      {
        "id": "cc0e8400-e29b-41d4-a716-446655440888",
        "group_id": 1,
        "tenant_id": 1,
        "cpu_quota_percentage": 40.0,
        "memory_quota": 16384,
        "storage_quota": 500,
        "created_at": "2025-03-09T10:50:00Z",
        "updated_at": "2025-03-09T10:50:00Z"
      }
    ]
  }
  ```
- **狀態碼：** 200 OK

#### 4.11.3 查詢單一群組租戶授權
- **HTTP 方法：** GET  
- **URL：** `/host-group-tenant-quotas/{id}`  
- **Response：**
  ```json
  {
    "id": "cc0e8400-e29b-41d4-a716-446655440888",
    "group_id": 1,
    "tenant_id": 1,
    "cpu_quota_percentage": 40.0,
    "memory_quota": 16384,
    "storage_quota": 500,
    "created_at": "2025-03-09T10:50:00Z",
    "updated_at": "2025-03-09T10:50:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.11.4 更新群組租戶授權
- **HTTP 方法：** PUT  
- **URL：** `/host-group-tenant-quotas/{id}`  
- **Request：**
  ```json
  {
    "group_id": 1,
    "tenant_id": 1,
    "cpu_quota_percentage": 50.0,
    "memory_quota": 16384,
    "storage_quota": 600
  }
  ```
- **Response：**
  ```json
  {
    "id": "cc0e8400-e29b-41d4-a716-446655440888",
    "group_id": 1,
    "tenant_id": 1,
    "cpu_quota_percentage": 50.0,
    "memory_quota": 16384,
    "storage_quota": 600,
    "created_at": "2025-03-09T10:50:00Z",
    "updated_at": "2025-03-09T11:50:00Z"
  }
  ```
- **狀態碼：** 200 OK

#### 4.11.5 刪除群組租戶授權
- **HTTP 方法：** DELETE  
- **URL：** `/host-group-tenant-quotas/{id}`  
- **Response：**
  ```json
  {
    "message": "Baremetal group tenant quota deleted successfully"
  }
  ```
- **狀態碼：** 200 OK 或 204 No Content

---

## 5. 注意事項

- **日期與時間：** 所有時間均採用 ISO8601 格式。  
- **資料格式：** 所有請求與回應皆以 JSON 格式傳遞。  
- **驗證失敗或例外情況：** 回應將依照全域錯誤格式返回錯誤訊息與錯誤代碼。  
- **資源關聯：** 各關聯資料（例如 ResourceMaintainer 多型關聯）皆以完整端點管理，確保單筆資源可依據對應關聯進行查詢與管理。

---
