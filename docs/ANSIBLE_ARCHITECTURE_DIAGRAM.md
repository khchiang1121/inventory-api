# Ansible Inventory 資料庫架構圖

## 核心架構概覽

```mermaid
graph TB
    subgraph "Ansible Inventory 核心"
        INV[AnsibleInventory<br/>📁 多個 Inventory 管理]
        INV_VAR[AnsibleInventoryVariable<br/>🔧 Inventory 層級變數]
    end
    
    subgraph "群組系統"
        GROUP[AnsibleGroup<br/>📂 群組管理]
        GROUP_VAR[AnsibleGroupVariable<br/>🔧 群組變數]
        GROUP_REL[AnsibleGroupRelationship<br/>🔗 父子群組關係]
    end
    
    subgraph "主機系統"
        HOST[AnsibleHost<br/>🖥️ 主機管理]
        HOST_VAR[AnsibleHostVariable<br/>🔧 主機變數]
    end
    
    subgraph "實體資源"
        VM[VirtualMachine<br/>💻 虛擬機]
        BM[Baremetal<br/>🖥️ 實體機]
        CLUSTER[K8sCluster<br/>☸️ Kubernetes 集群]
    end
    
    subgraph "動態與模板"
        PLUGIN[AnsibleInventoryPlugin<br/>🔌 動態插件]
        TEMPLATE[AnsibleInventoryTemplate<br/>📄 模板系統]
    end
    
    %% 核心關聯
    INV --> INV_VAR
    INV --> GROUP
    INV --> HOST
    INV --> PLUGIN
    
    %% 群組關聯
    GROUP --> GROUP_VAR
    GROUP --> GROUP_REL
    GROUP_REL --> GROUP
    
    %% 主機關聯
    HOST --> HOST_VAR
    GROUP --> HOST
    
    %% 實體資源關聯
    VM -.-> HOST
    BM -.-> HOST
    CLUSTER --> VM
    
    %% 模板關聯
    TEMPLATE -.-> INV
```

## 詳細關聯說明

### 1. Inventory 層級 (最上層)
- **AnsibleInventory**: 管理多個 inventory 文件
- **AnsibleInventoryVariable**: inventory 層級的變數，所有群組和主機都會繼承

### 2. 群組層級 (中間層)
- **AnsibleGroup**: 群組管理，支援層次結構
- **AnsibleGroupVariable**: 群組變數，會覆蓋 inventory 變數
- **AnsibleGroupRelationship**: 父子群組關係，支援變數繼承

### 3. 主機層級 (最下層)
- **AnsibleHost**: 主機管理，支援別名和狀態
- **AnsibleHostVariable**: 主機變數，優先級最高

### 4. 實體資源關聯
- **VirtualMachine** 和 **Baremetal** 透過 Generic Foreign Key 關聯到 **AnsibleHost**
- **K8sCluster** 關聯到 **VirtualMachine**，形成 cluster → VM → AnsibleHost 的鏈路

### 5. 擴展功能
- **AnsibleInventoryPlugin**: 動態 inventory 插件配置
- **AnsibleInventoryTemplate**: 支援生成不同格式的 inventory 文件

## 變數繼承優先級

```mermaid
graph TD
    A[AnsibleInventoryVariable<br/>🔧 Inventory 變數<br/>優先級: 最低] 
    B[AnsibleGroupVariable<br/>🔧 群組變數<br/>優先級: 中等]
    C[AnsibleHostVariable<br/>🔧 主機變數<br/>優先級: 最高]
    
    A --> B
    B --> C
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
```

## 使用流程圖

```mermaid
flowchart TD
    START[開始使用] --> CREATE_INV[1. 創建 AnsibleInventory]
    CREATE_INV --> CREATE_GROUP[2. 創建 AnsibleGroup]
    CREATE_GROUP --> CREATE_REL[3. 建立群組關係<br/>AnsibleGroupRelationship]
    CREATE_REL --> ADD_VARS[4. 添加變數<br/>Inventory/Group/Host Variables]
    ADD_VARS --> LINK_HOST[5. 關聯主機<br/>VM/Baremetal → AnsibleHost]
    LINK_HOST --> GENERATE[6. 生成 Inventory 文件]
    GENERATE --> END[完成]
    
    style START fill:#e8f5e8
    style END fill:#ffebee
    style CREATE_INV fill:#e3f2fd
    style CREATE_GROUP fill:#f3e5f5
    style CREATE_REL fill:#fff3e0
    style ADD_VARS fill:#fce4ec
    style LINK_HOST fill:#e0f2f1
    style GENERATE fill:#f1f8e9
```

## Cluster Inventory 特殊流程

```mermaid
graph LR
    subgraph "Cluster 環境"
        CLUSTER[K8sCluster<br/>☸️ Kubernetes 集群]
        VM1[VirtualMachine<br/>💻 Control Plane]
        VM2[VirtualMachine<br/>💻 Worker Node]
        VM3[VirtualMachine<br/>💻 Management]
    end
    
    subgraph "Ansible Inventory"
        INV[AnsibleInventory<br/>📁 Cluster Inventory]
        GROUP1[AnsibleGroup<br/>📂 control_plane]
        GROUP2[AnsibleGroup<br/>📂 worker_nodes]
        GROUP3[AnsibleGroup<br/>📂 management]
        HOST1[AnsibleHost<br/>🖥️ Master-01]
        HOST2[AnsibleHost<br/>🖥️ Worker-01]
        HOST3[AnsibleHost<br/>🖥️ Bastion]
    end
    
    CLUSTER --> VM1
    CLUSTER --> VM2
    CLUSTER --> VM3
    
    VM1 -.-> HOST1
    VM2 -.-> HOST2
    VM3 -.-> HOST3
    
    INV --> GROUP1
    INV --> GROUP2
    INV --> GROUP3
    
    GROUP1 --> HOST1
    GROUP2 --> HOST2
    GROUP3 --> HOST3
    
    style CLUSTER fill:#e3f2fd
    style INV fill:#f3e5f5
    style GROUP1 fill:#e8f5e8
    style GROUP2 fill:#e8f5e8
    style GROUP3 fill:#e8f5e8
```

## 實際使用場景

### 場景 1: 環境分層管理
```
Production Inventory
├── webservers (群組)
│   ├── web-01 (主機)
│   └── web-02 (主機)
├── databases (群組)
│   ├── db-01 (主機)
│   └── db-02 (主機)
└── monitoring (群組)
    └── monitor-01 (主機)
```

### 場景 2: Cluster 管理
```
K8s Cluster Inventory
├── control_plane (群組)
│   ├── master-01 (主機)
│   └── master-02 (主機)
├── worker_nodes (群組)
│   ├── worker-01 (主機)
│   └── worker-02 (主機)
└── management (群組)
    └── bastion (主機)
```

### 場景 3: 多環境管理
```
Multi-Environment Inventory
├── production (群組)
│   ├── webservers (子群組)
│   └── databases (子群組)
├── staging (群組)
│   ├── webservers (子群組)
│   └── databases (子群組)
└── development (群組)
    ├── webservers (子群組)
    └── databases (子群組)
```

## 關鍵設計原則

1. **層次化結構**: Inventory → Group → Host
2. **變數繼承**: Inventory 變數 → Group 變數 → Host 變數
3. **靈活關聯**: 透過 Generic Foreign Key 支援 VM 和 Baremetal
4. **擴展性**: 支援動態插件和模板系統
5. **狀態管理**: 支援主機和群組的啟用/停用狀態
6. **別名支援**: 主機可以有多個別名

這個架構讓您可以靈活地管理各種複雜的 Ansible inventory 需求，從簡單的單一環境到複雜的多 cluster 多環境管理都能輕鬆應對！
