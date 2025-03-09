# 資料庫設計文件

**版本：** 1.0.0  
**更新日期：** 2025-03-09

本文件描述系統中各主要資源（例如實體機、虛擬機、群組、租戶、k8s 叢集等）的資料表設計，並詳細說明各表之間的關聯與使用方式。

## 1. 維護者與維護者群組管理

### ① 個人維護者（Maintainer）
**用途：**  
記錄每個以個人身分出現的維護者資訊，供其他資源指定維護負責人時參考。  
**使用方式：**  
- 當系統中需要指派一個人來負責維護某資源時，會在此表中查詢相應的個人維護者資料。  
- 欄位說明如下：

| 欄位名稱   | 型態       | 說明                                   |
|------------|------------|----------------------------------------|
| id         | UUID (PK)  | 唯一識別碼，作為每位維護者的主鍵       |
| name       | String     | 維護者名稱                             |
| email      | String     | 聯絡信箱（選填）                       |
| status     | String     | 狀態（例如：active/inactive）          |
| created_at | DateTime   | 建立時間                               |
| updated_at | DateTime   | 更新時間                               |

---

### ② 維護者群組（MaintainerGroup）
**用途：**  
記錄由多位個人維護者組成的群組，並可指定一位群組管理者，方便集中管理或批次指派維護任務。  
**使用方式：**  
- 當一組維護者需要以群組的形式出現（例如跨部門的資源維護團隊）時，將在此表中建立群組，並透過 `group_manager_id` 指定負責該群組的管理者。  
- 欄位說明如下：

| 欄位名稱         | 型態       | 說明                                          |
|------------------|------------|-----------------------------------------------|
| id               | UUID (PK)  | 唯一識別碼                                    |
| name             | String     | 群組名稱                                      |
| group_manager_id | UUID       | 指派的群組管理者（FK → Maintainer.id）         |
| description      | Text       | 群組用途說明（選填）                           |
| status           | String     | 狀態（例如：active/inactive）                 |
| created_at       | DateTime   | 建立時間                                      |
| updated_at       | DateTime   | 更新時間                                      |

---

### ③ 維護者群組成員（MaintainerGroupMember）
**用途：**  
記錄個人維護者與其所屬維護者群組之間的關係。  
**使用方式：**  
- 當一位個人維護者屬於一個或多個維護者群組時，會在此表中分別建立記錄。這讓系統能夠查詢某個群組內所有成員，也能反向查詢某個維護者所屬的所有群組。  
- 欄位說明如下：

| 欄位名稱      | 型態       | 說明                                           |
|---------------|------------|------------------------------------------------|
| id            | UUID (PK)  | 唯一識別碼                                     |
| group_id      | UUID       | 維護者群組 ID（FK → MaintainerGroup.id）         |
| maintainer_id | UUID       | 個人維護者 ID（FK → Maintainer.id）              |
| created_at    | DateTime   | 建立時間                                       |
| updated_at    | DateTime   | 更新時間                                       |

---

### ④ 資源維護者關聯（ResourceMaintainer）
**用途：**  
由於各資源（如 Host、VirtualMachine、HostGroup、Tenant、K8sCluster 等）都可能同時配置個人或維護者群組作為維護者，此表使用多型關聯（Polymorphic Association）來統一管理。  
**使用方式：**  
- 當需要查詢某個資源的維護者（或反向查詢某個維護者負責哪些資源）時，可透過此表查詢。  
- `resource_type` 用來指明資源種類，而 `resource_id` 則對應各資源的主鍵；  
- 同理，`maintainer_type` 及 `maintainer_id` 分別記錄該維護者是個人還是群組以及其對應的 ID。  
- 欄位說明如下：

| 欄位名稱        | 型態          | 說明                                                                                   |
|-----------------|---------------|----------------------------------------------------------------------------------------|
| id              | UUID (PK)     | 唯一識別碼                                                                             |
| resource_type   | String        | 資源類型（例如："Host", "VirtualMachine", "HostGroup", "Tenant", "K8sCluster"）         |
| resource_id     | UUID/Integer  | 資源的識別碼（依各資源 PK 型態而定）                                                    |
| maintainer_type | String        | 維護者類型： "individual" 或 "group"                                                   |
| maintainer_id   | UUID          | 若 `maintainer_type` 為 "individual"，參考 Maintainer.id；若為 "group"，參考 MaintainerGroup.id |
| created_at      | DateTime      | 建立時間                                                                               |
| updated_at      | DateTime      | 更新時間                                                                               |

---

## 2. 實體機器表（Host）
**用途：**  
儲存所有實體機器的硬體資源、狀態以及所在位置資訊，並與實體機群組（HostGroup）建立關聯。  
**使用方式：**  
- 當需要根據資源狀況（CPU、記憶體、儲存空間）或物理位置（region、dc、room、rack）進行虛擬機部署決策時，系統會查詢此表。  
- 此外，`old_system_id` 用於對應舊系統中的實體機資訊，方便資料遷移與整合。  
- 欄位說明如下：

| 欄位名稱          | 型態                  | 說明                                                        |
|-------------------|-----------------------|-------------------------------------------------------------|
| id                | UUID (PK)             | 實體機唯一識別碼                                             |
| name              | String                | 實體機名稱                                                  |
| status            | String                | 實體機狀態（例如：running, maintenance, offline 等）       |
| total_cpu         | Integer               | 總 CPU 核心數                                               |
| total_memory      | Integer               | 總記憶體（MB）                                               |
| total_storage     | Integer               | 總儲存空間（GB）                                             |
| available_cpu     | Integer               | 可用 CPU 核心數                                             |
| available_memory  | Integer               | 可用記憶體（MB）                                             |
| available_storage | Integer               | 可用儲存空間（GB）                                           |
| group_id          | ForeignKey (HostGroup)| 所屬資源群組（每台 Host 只能屬於一個群組）                   |
| region            | String                | 工廠區域（例如：北區、南區等）                                |
| dc                | String                | 資料中心名稱                                               |
| room              | String                | 資料中心內的房間                                             |
| rack              | String                | 機櫃編號                                                   |
| unit              | String                | 機架單位                                                   |
| old_system_id     | String                | 舊系統中該實體機的識別碼                                       |
| created_at        | DateTime              | 紀錄建立時間                                                |
| updated_at        | DateTime              | 紀錄最後更新時間                                            |

---

### 實體機群組表（HostGroup）
**用途：**  
用來將實體機分組，便於依群組進行資源調度與管理。  
**使用方式：**  
- 當需要根據資源負載、維護需求或地理分佈進行分組管理時，會在此表中記錄各群組的資訊。  
- 欄位說明如下：

| 欄位名稱   | 型態         | 說明                                |
|------------|--------------|----------------------------------|
| id         | UUID (PK)    | 群組唯一 ID                        |
| name       | String       | 群組名稱                            |
| description| Text         | 群組用途說明（選填）                  |
| status     | String       | 群組狀態（例如：active/inactive）     |
| created_at | DateTime     | 紀錄建立時間                        |
| updated_at | DateTime     | 紀錄最後更新時間                    |

---

### 租戶表（Tenant）
**用途：**  
記錄系統中不同的使用者或單位，其資源使用管理及權限配置皆以租戶為單位。  
**使用方式：**  
- 每個租戶可以對應到一個或多個 k8s 叢集，同時也在 HostGroupTenantQuota 表中配置資源配額。  
- 欄位說明如下：

| 欄位名稱   | 型態         | 說明                                |
|------------|--------------|-------------------------------------|
| id         | UUID (PK) | 租戶唯一識別碼                       |
| name       | String       | 租戶名稱                            |
| description| Text         | 租戶說明（選填）                     |
| status     | String       | 租戶狀態（例如：active/inactive）    |
| created_at | DateTime     | 紀錄建立時間                        |
| updated_at | DateTime     | 紀錄最後更新時間                    |

---

## 3. 虛擬機（VirtualMachine）
**用途：**  
記錄所有虛擬機的狀態與配置，並記錄其所屬租戶、所在實體機，以及可能隸屬的 k8s 叢集。  
**使用方式：**  
- 在建立虛擬機時，必須指定所屬的租戶與實體機（Host）；若該虛擬機將加入 k8s 叢集，則可選填 `k8s_cluster_id`。  
- 欄位說明如下：

| 欄位名稱           | 型態                           | 說明                                         |
|--------------------|--------------------------------|----------------------------------------------|
| id                 | UUID (PK)                      | 唯一識別碼                                   |
| name               | String                         | 虛擬機名稱                                   |
| tenant_id          | ForeignKey (Tenant)            | 關聯租戶                                     |
| host_id            | ForeignKey (Host)              | 所屬實體機器                                 |
| specification_id   | ForeignKey (VMSpecification)   | VM 規格                                      |
| k8s_cluster_id     | ForeignKey (K8sCluster)        | 所屬 k8s 叢集（選填）                         |
| status             | String                         | 虛擬機狀態（例如：建立中、運行中、錯誤）       |
| created_at         | DateTime                       | 建立時間                                     |
| updated_at         | DateTime                       | 更新時間                                     |

---

## 4. 虛擬機規格表（VMSpecification）
**用途：**  
定義虛擬機的各種硬體資源需求選項，供使用者在建立虛擬機時選擇。  
**使用方式：**  
- 每筆虛擬機建立請求將根據此表中定義的資源規格（CPU、記憶體、儲存空間）來分配相應的資源。  
- 欄位說明如下：

| 欄位名稱         | 型態     | 說明                        |
|------------------|----------|-----------------------------|
| id               | UUID     | 規格唯一識別碼              |
| name             | String   | 規格名稱                    |
| required_cpu     | Integer  | CPU 需求（核心數）          |
| required_memory  | Integer  | 記憶體需求（MB）            |
| required_storage | Integer  | 儲存空間需求（GB）          |
| created_at       | DateTime | 建立時間                    |
| updated_at       | DateTime | 最後更新時間                |

---

## 5. k8s 叢集管理

### K8sCluster 表
**用途：**  
記錄 k8s 叢集的資訊。初期設計時可視為每個租戶對應一個叢集，但考慮未來一個租戶可能管理多個叢集，因此使用多對一關聯。  
**使用方式：**  
- k8s 叢集的資源狀態、描述等由此表管理；同時，其維護者管理可透過前述 ResourceMaintainer 表來設定（resource_type 設為 "K8sCluster"）。  
- 欄位說明如下：

| 欄位名稱   | 型態                           | 說明                                                      |
|------------|--------------------------------|-----------------------------------------------------------|
| id         | UUID (PK)                      | k8s 叢集唯一識別碼                                        |
| name       | String                         | 叢集名稱                                                  |
| tenant_id  | ForeignKey (Tenant)            | 關聯租戶                                                  |
| description| Text                           | 叢集描述（選填）                                           |
| status     | String                         | 叢集狀態（例如：active, maintenance, offline）           |
| created_at | DateTime                       | 建立時間                                                  |
| updated_at | DateTime                       | 更新時間                                                  |

---

## 6. 群組租戶授權表（HostGroupTenantQuota）
**用途：**  
記錄每個租戶在各個實體機群組中的資源使用權限或配額比例，用於控制各租戶在群組內能夠使用的資源上限。  
**使用方式：**  
- 當租戶發起虛擬機建立請求時，系統會根據此表中記錄的配額（CPU、記憶體、儲存空間）及該群組內的資源剩餘情況進行調度。  
- 欄位說明如下：

| 欄位名稱             | 型態                    | 說明                                |
|----------------------|-------------------------|-------------------------------------|
| id                   | UUID                    | 唯一識別碼                          |
| group_id             | ForeignKey (HostGroup)  | 關聯群組                            |
| tenant_id            | ForeignKey (Tenant)     | 關聯租戶                            |
| cpu_quota_percentage | Float                   | CPU 資源配額百分比（例如 40%）        |
| memory_quota         | Integer                 | 記憶體上限（MB）                    |
| storage_quota        | Integer                 | 儲存空間上限（GB）                  |
| created_at           | DateTime                | 紀錄建立時間                        |
| updated_at           | DateTime                | 紀錄最後更新時間                    |

---

# 小結

1. **維護者相關：**  
   - **Maintainer、MaintainerGroup、MaintainerGroupMember 與 ResourceMaintainer** 這四個表負責管理所有資源的維護者資訊。系統中任何資源（例如 Host、VirtualMachine、HostGroup、Tenant、K8sCluster）均可透過 ResourceMaintainer 與相應的維護者（個人或群組）建立關聯。

2. **實體機管理：**  
   - **Host** 表記錄所有實體機資訊，包括硬體資源、目前狀態、物理位置（region、dc、room、rack）與舊系統對應 ID。  
   - **HostGroup** 用於將實體機按需求分組，便於根據資源負載與地理分佈進行管理與調度。

3. **租戶與授權：**  
   - **Tenant** 表記錄各使用者或單位資訊；  
   - **HostGroupTenantQuota** 則記錄每個租戶在各群組中的資源使用配額，支援資源調度與權限控管。

4. **虛擬機與規格：**  
   - **VirtualMachine** 表記錄虛擬機的基本資訊及其關聯（租戶、實體機、VM 規格、k8s 叢集）；  
   - **VMSpecification** 表定義虛擬機的各種配置選項，供租戶在建立虛擬機時選擇。

5. **k8s 叢集管理：**  
   - **K8sCluster** 表記錄 k8s 叢集資訊，並與租戶建立關聯。叢集相關的維護者資訊同樣透過 ResourceMaintainer 管理。

