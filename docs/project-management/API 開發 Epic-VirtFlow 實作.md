# API 開發 Epic: VirtFlow 實作

## 🏗️ Story 1：基礎設施搭建與環境設定

### 🧑‍ 使用者故事（User Story）  

作為開發團隊，我們希望能夠快速建立一致且可複製的本地開發環境，並設定好自動化測試與部署流程、確保資料庫等基礎設施正常運作，讓所有人都能輕鬆開發與上線服務。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 透過 Docker / docker-compose 一鍵啟動本地環境（含 DB、API）  
2. 建立 CI/CD 工作流程，能自動進行測試與部署  
3. PostgreSQL 基礎資料庫與測試資料庫可正常連線並進行 Migration  
4. 提供 README 或 Makefile 等常用指令與操作教學  

#### 🛠️ Sub-task 1：開發環境初始化  

- 撰寫 Dockerfile / docker-compose.yml  
- 設定 Makefile（或 README）提供常用指令  
- 調整靜態檔案服務方式（whitenoise / gunicorn 等）

#### 🛠️ Sub-task 2：資料庫與備份/監控  

- 建置 PostgreSQL 並配置開發/測試環境參數  
- 規劃資料庫備份流程（尚未完成，列入後續待辦）  
- 預留監控機制（例如利用 pgAdmin、Prometheus；列入後續待辦）

#### 🛠️ Sub-task 3：CI/CD 流程  

- 撰寫自動化測試腳本與工作流程（pytest、linter）  
- 設定自動部署流程（例如使用 GitHub Actions 或 GitLab CI）  

> **實作狀況**  
>
> - Docker、DB、CI/CD 基本功能已完成  
> - 資料庫備份策略、進階監控尚未實作，應在後續任務中補足

---

## 👤 Story 2：使用者與認證/授權機制

### 🧑‍ 使用者故事（User Story）  

作為平台管理者，我希望能有一套完整的使用者模型與認證/授權機制，支援自訂用戶帳號、群組及物件層級權限，以便區分不同角色與資源維護者，確保系統安全性。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 提供自訂使用者模型（CustomUser）與群組  
2. 支援 Token 認證並可透過 API 獲取 Token  
3. 後續可擴充為更安全的 Knox Token 或 OAuth2 認證機制  
4. 可整合 django-guardian 或類似套件進行物件層級（object-level）授權  

#### 🛠️ Sub-task 1：使用者模型  

- 建立 CustomUser（含帳號、狀態欄位等）  
- 維護者群組（Maintainer Group）模型（若需要細分不同維護角色）  

#### 🛠️ Sub-task 2：認證機制  

- 實作 DRF TokenAuthentication（已完成）  
- 規劃切換至更安全的 Knox / OAuth2（尚未實作，列入待辦）  
- 驗證用戶可透過登入取得 Token  

#### 🛠️ Sub-task 3：物件層級權限  

- 引入 django-guardian 進行 object-level permission  
- 設計給 API View 的權限檢查邏輯  
- 提供對象（使用者/群組）授權與移除授權的 API 介面  
- 針對大量物件的效能測試（尚未執行，列入後續評估）  

#### 🛠️ Sub-task 4：測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - CustomUser 與簡易 Token 登入已完成  
> - Knox / OAuth2 尚未導入；django-guardian 已安裝但尚待進一步整合

---

## 🖥️ Story 3：實體伺服器（Baremetal）與群組管理

### 🧑‍ 使用者故事（User Story）  

作為資源管理者，我希望能定義 BaremetalGroup 與 Baremetal 實體機資料模型，並提供查詢與管理的 API，用以維護每台實體機的資源配置與狀態。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 定義 BaremetalGroup 與 Baremetal 模型，可紀錄 CPU、記憶體、儲存等容量  
2. 提供 CRUD API 與文件  
3. 若有多台實體機歸屬同一群組，可更新群組的可用資源欄位  
4. 綁定維護者（使用者或群組），讓已授權者才能操作對應的 Baremetal  

#### 🛠️ Sub-task 1: 基本資料結構  

- BaremetalGroup（名稱、總 CPU/記憶體/儲存及可用量）  
- Baremetal（名稱、序號、可用 CPU/記憶體/儲存等）  
- BaremetalGroup 與 Baremetal 間的關聯（已完成）  

#### 🛠️ Sub-task 2: 資源統計與 API  

- 提供 CRUD API  
- 撰寫 API 文件  
- 新增/更新 Baremetal 時，可同步更新群組可用量  

#### 🛠️ Sub-task 3: 權限整合  

- 僅擁有權限的使用者可管理對應 Baremetal 或 Group  
- 在查詢或操作時做物件層級權限判斷  

#### 🛠️ Sub-task 4：測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - 模型與基本 API 已完成，可成功 CRUD  
> - 機房、採購相關欄位已新增但仍需更多測試與資料填充

---

## 🧾 Story 4：虛擬機規格管理與租戶指定 (Story Points: 3)

### 🧑‍ 使用者故事（User Story）  

作為平台操作人員，我希望能定義虛擬機的標準化規格，以利租戶申請虛擬機時能夠選擇適當的資源配置。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 設計 VirtualMachineSpecification 資料模型  
2. 提供 CRUD API 與文件  
3. 支援版本與 generation 設定  
4. 支援與租戶間的關聯綁定（非強制）  

#### 🛠️ Sub-task 1: VM 規格資料模型設計  

- 定義 VM 規格模型結構  
- 欄位包括 CPU、記憶體、儲存容量等基本資源資訊  

#### 🛠️ Sub-task 2: CRUD API 與驗證機制  

- 提供 CRUD API  
- 撰寫 API 文件  
- 保留與租戶 VM 建立時的整合欄位  

#### 🛠️ Sub-task 3：測試案例  

- 撰寫測試案例  

---

## ☁️ Story 5：虛擬機（VM）建立與管理

### 🧑‍ 使用者故事（User Story）  

作為租戶或操作人員，我希望根據給定虛擬機規格（CPU、記憶體、儲存）建立虛擬機，並在建立 VM 時檢查可用實體資源，以便部署在對應的 Baremetal 上。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 提供虛擬機清單與詳細資訊 API  
2. 顯示租戶、群組、實體機、Cluster 等欄位摘要  
3. 顯示關聯的 NetworkInterface 資訊  
4. 提供過濾條件（如租戶、群組、狀態等）  
5. VirtualMachine 建立 API，可帶入租戶、群組、規格等參數  
6. 建立 VM 時能檢查 BaremetalGroup / Baremetal 是否有足夠資源  
7. 若資源不足，回傳錯誤並終止建立（列入待辦）  

#### 🛠️ Sub-task 1: VM 模型與 API  

- VirtualMachine 模型（含 CPU、記憶體、儲存等欄位）  
- 提供 CRUD API  
- 撰寫 API 文件  
- 提供版本或 generation 以供未來擴充  

#### 🛠️ Sub-task 2: VM 詳細查詢介面開發  

- 設計含嵌套欄位的詳細 View 與 Serializer  
- 顯示 Resource 層級摘要資訊  
- 排程器或簡易邏輯：從可用 Baremetal 中選擇一台（尚未實作複雜演算法）  
- 建立後更新 Baremetal 剩餘資源  

#### 🛠️ Sub-task 3: 擴充與待辦  

- 若 VM 要與 Kubernetes 或網路模型整合，需在後續 Story 中擴充  
- 錯誤處理與資源回收機制（如調度失敗時的 rollback）尚未完成  

#### 🛠️ Sub-task 4: 關聯資源整合顯示  

- 顯示所屬群組、Baremetal、Cluster、租戶資訊  
- 顯示掛載的 NetworkInterface 詳細資料  

#### 🛠️ Sub-task 5: 條件過濾與搜尋支援  

- 支援 filterset 過濾（例如狀態、租戶 ID）  
- 撰寫 API 文件與查詢說明  

#### 🛠️ Sub-task 6：測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - VM 規格與基礎 VM CRUD 已完成  
> - 資源調度僅初步實作；進階排程邏輯、異常處理尚待擴充

---

## ☸️ Story 6：Kubernetes Cluster 與外掛/網格管理

### 🧑‍ 使用者故事（User Story）  

作為資源平台的開發者，我希望能夠管理 K8sCluster 及其相關外掛、服務網格（ServiceMesh），並在必要時綁定跳板機（Bastion）以實現更靈活的集群維護與監控。

### ✔️ 驗收標準（Acceptance Criteria）  

1. K8sCluster 模型可紀錄版本、狀態、租戶歸屬等資訊  
2. 支援外掛 (K8sClusterPlugin) 與服務網格 (ServiceMesh) 的多對多關聯  
3. BastionClusterAssociation：可將跳板機（某 VM）與 K8sCluster 做綁定  
4. 提供 CRUD API 與簡易狀態管理  

#### 🛠️ Sub-task 1: Cluster 模型與 API 設計  

- 建立 K8sCluster 模型與關聯欄位  
- 支援多種調度模式設定與狀態欄位  
- 提供 CRUD API  
- 撰寫 API 文件  

#### 🛠️ Sub-task 2: Plugin / ServiceMesh 整合  

- 插件 (K8sClusterPlugin) 提供 CRUD API  
- ServiceMesh（如 cilium、istio）與 K8sCluster 的多對多關聯  
- BastionClusterAssociation 用於管理跳板機  

#### 🛠️ Sub-task 3: 擴充與後續  

- 與虛擬機建置流程的深度整合（尚未完成）  
- ServiceMesh 升級與滾動更新流程設計  
- 叢集狀態監控、故障報警（後續需要完整機制）  

#### 🛠️ Sub-task 4：測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - K8sCluster、Plugin、Bastion 基本 CRUD 已完成  
> - 真實 K8s API 的整合與監控尚未進行

---

## 👥 Story 7：多租戶管理與資源配額 (Quota)

### 🧑‍ 使用者故事（User Story）  

作為平台設計者，我希望能夠支援多租戶（Tenant），並設定各租戶在特定 BaremetalGroup 上的配額（如 CPU 百分比、記憶體上限），以避免資源搶奪並提供一定的隔離度。

### ✔️ 驗收標準（Acceptance Criteria）  

1. Tenant 模型與 CRUD API  
2. BaremetalGroupTenantQuota：可為每個 (Tenant, Group) 設置 CPU、記憶體、儲存等上限  
3. 在建立 VM 或 K8sCluster 時檢查對應租戶的配額  
4. 若配額不足，回傳錯誤並拒絕建立  
5. 支援 API 管理配額設定與查詢  
6. 限制租戶僅能使用自身 quota 內的資源  

#### 🛠️ Sub-task 1: 租戶模型  

- 定義 Tenant（名稱、描述、狀態）  
- 與 VM、K8sCluster、BaremetalGroup 建立關聯  

#### 🛠️ Sub-task 2: 配額模型與 API 實作  

- 設計 BaremetalGroupTenantQuota 模型  
- 提供 CRUD API  
- 建立或更新配額時即時同步可用值（尚未完成，需要計算邏輯）  

#### 🛠️ Sub-task 3: 配額檢查  

- VM / K8sCluster 建立流程中，檢查租戶是否還有配額可用  
- 若超出則回傳錯誤訊息  

#### 🛠️ Sub-task 4: 權限與文件  

- 整合 django-guardian 進行權限控制  
- 驗證租戶與群組關聯正確性  

#### 🛠️ Sub-task 5: 測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - Tenant 與 BaremetalGroupTenantQuota 已完成 CRUD  
> - 建立 VM / Cluster 的配額檢查僅部分整合，需要更嚴謹的檢查流程

---

## 🌐 Story 8：網路模型與介面管理

### 🧑‍ 使用者故事（User Story）  

作為網路管理者，我希望能設定 VLAN、VRF、BGPConfig 等網路參數，並讓任意資源（虛擬機、實體機等）都能掛載網卡並接上特定 VLAN / VRF / BGP。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 提供 VLAN 與 VRF 的資料模型與 CRUD API  
2. NetworkInterface 提供 content_type + object_id 進行泛型關聯  
3. 可在 API 中為 Baremetal / VM / K8sCluster 增加網卡並設定 IP、Gateway、DNS  
4. 若需要多個 BGP Peer，也能於同一介面上配置  
5. API 提供綁定與解除綁定功能  

#### 🛠️ Sub-task 1: VLAN, VRF, BGPConfig  

- 設計 VLAN 與 VRF 模型  
- 基本欄位：vlan_id, name, route_distinguisher, asn, peer_ip 等  
- 提供前端可查詢及綁定的 API  

#### 🛠️ Sub-task 2: NetworkInterface 關聯整合  

- NetworkInterface 可指定 VLAN 或 VRF  
- Serializer 中顯示 VLAN/VRF 概要  
- GenericForeignKey 用於指向任何資源  
- IPv4 / IPv6 / VLAN / VRF 欄位  
- BGPConfig 可 OneToOne 或多對多（尚未完全實作）  

#### 🛠️ Sub-task 3: 待辦 / 擴充  

- 進階網路管理（VXLAN、Bonding 等）  
- 整合 K8s CNI / ServiceMesh 的網路拓撲資訊  

#### 🛠️ Sub-task 4: 測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - VLAN / VRF / BGPConfig / NetworkInterface 已完成基本 API  
> - 多 BGP Peer / 動態路由設計尚待補強

---

## 🧾 Story 9：BGP 設定管理與展示功能 (Story Points: 3)

### 🧑‍ 使用者故事（User Story）  

作為資深網路工程師，我希望能夠定義 BGP 設定，並將其關聯至網路介面，以支援進階的路由需求與對接實體網路。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 設計 BGPConfig 模型，支援 ASN、Neighbor、Password 等欄位  
2. 可透過 NetworkInterface 綁定 BGP 設定  
3. 支援單一介面多對多的 BGP 邏輯  
4. API 可建立、查詢、變更 BGP 設定  

#### 🛠️ Sub-task 1: 模型與欄位設計  

- 定義 BGPConfig 模型欄位（ASN、RouterID、Password 等）  
- 支援與 NetworkInterface 的關聯模型  

#### 🛠️ Sub-task 2: API 與驗證邏輯  

- 建立 BGP 設定 CRUD API  
- 驗證與 VLAN、VRF 的關聯性  

#### 🛠️ Sub-task 3: 展示與綁定邏輯  

- 在 NetworkInterface 顯示 BGP 設定摘要  
- 支援設定多個 BGP peer 並輸入多筆資料  

#### 🛠️ Sub-task 5: 測試案例  

- 撰寫測試案例  

---

## 🏬 Story 10：品牌與採購相關資料

### 🧑‍ 使用者故事（User Story）  

作為運維負責人，我希望能記錄硬體品牌、型號，以及採購單資訊（請購單與採購單），以追蹤設備來源與採購流程。

### ✔️ 驗收標準（Acceptance Criteria）  

1. Brand, BaremetalModel：可紀錄廠牌與型號關係  
2. PurchaseRequisition, PurchaseOrder：可紀錄請購、採購的基本資訊  
3. Baremetal 可關聯對應的品牌/型號、採購單資訊  

#### 🛠️ Sub-task 1: 主要模型  

- Brand：廠牌（Dell, HPE 等）  
- BaremetalModel（名稱、brand、CPU/記憶體/儲存等預設值）  
- Baremetal 關聯 Brand 與 BaremetalModel  

#### 🛠️ Sub-task 2: 採購單模型  

- PurchaseRequisition（pr_number, requested_by 等）  
- PurchaseOrder（po_number, vendor_name 等）  
- Baremetal 關聯請購與採購資訊  

#### 🛠️ Sub-task 5: 測試案例  

- 撰寫測試案例  

> **實作狀況**  
>
> - 基本模型與欄位已建立，CRUD 可用

---

## 🏬 Story 11：實體位置相關資料

### 🧑‍ 使用者故事（User Story）  

作為運維負責人，我希望能記錄設備所在機房位置，以協助設備生命週期的管理。

### ✔️ 驗收標準（Acceptance Criteria）  

1. Fabrication / Phase / DataCenter / Room / Rack：可標示實體機所在位置  

#### 🛠️ Sub-task 1: 主要模型  

- Fabrication / Phase / DataCenter / Room / Rack：對應各級機房結構  

#### 🛠️ Sub-task 2: 與 Baremetal 的整合  

- Baremetal 連上機房位置（Fabrication, DataCenter, Room, Rack 等）

#### 🛠️ Sub-task 5: 測試案例  

- 撰寫測試案例  

---

## 📝 Story 12：API 版本管理與多版本維護

### 🧑‍ 使用者故事（User Story）  

作為 API 設計者，我希望能針對不同開發階段或客戶需求提供多個版本的 API，以利平行開發並確保相容性。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 使用 URL Path Versioning（如 /api/v1/…、/api/v2/…）  
2. 不同版本可對應不同 Serializer / ViewSet  
3. 共用同一套資料庫模型（避免重複定義 Model）  
4. 能同時產生多版本的 OpenAPI 文件  

#### 🛠️ Sub-task 1: 路由與目錄結構  

- 在 urls.py 建立 /v1 及 /v2 等路由  
- 保持 Model 一致，僅在序列化層與 API 層做區分  

#### 🛠️ Sub-task 2: OpenAPI 文件  

- 使用 drf-spectacular 或 drf-yasg 產生 schema  
- /api/v1/docs、/api/v2/docs 分別顯示  

> **實作狀況**  
>
> - 已建置初步版本化路由 /v1  
> - 尚未啟動 /v2；多版本文件功能可在正式上線前再度完善  

---

## 🔐 Story 13：物件層級權限控制

### 🧑‍ 使用者故事（User Story）  

作為系統架構師，我需要在多租戶與多資源情境下，能夠限制使用者只能操作自己擁有或獲授權的物件，確保系統安全與資源隔離。

### ✔️ 驗收標準（Acceptance Criteria）  

1. 權限可透過群組或單人方式設定  
2. 支援所有主要模型的 object-level permission（查詢、編輯、刪除、授權）  
3. 可區分擁有者（Owner）、維護者（Maintainer）、僅查看者（Viewer）  
4. 所有操作行為可記錄並追蹤  
5. 未經授權的操作需被拒絕  
6. API 或管理介面可指派 / 收回權限  
7. 權限查詢需具備效能優化與錯誤處理  

#### 🛠️ Sub-task 1: 權限架構  

- 整合 Django 原生與 django-guardian 權限機制  
- 建立共用 decorator / mixin 進行權限檢查  

#### 🛠️ Sub-task 2: 權限賦予與驗證  

- 建立資源時自動授權建立者  
- 支援透過 API 指派或變更權限  
- 支援 view、change、delete 等操作層級  

#### 🛠️ Sub-task 3: Audit Log  

- 利用 Django signals 或 django-auditlog 記錄操作行為  
- 包含 VM 建立、Baremetal 更新、資源刪除等行為  

#### 🛠️ Sub-task 4: 擴充設計  

- 支援角色與 object-level permission 並存  
- 若需 Deny 優先，設計自訂規則流程  
- 快取與效能優化設計  

#### 🛠️ Sub-task 5: 測試案例與文件  

- 撰寫權限測試案例與例外處理  
- 文件說明權限授權方式與角色行為  

> **實作狀況**  
>
> - django-guardian 已配置，部分 API 已整合  
> - Audit Log 尚在規劃，預計擴充至所有核心模型與前端介面  

---
