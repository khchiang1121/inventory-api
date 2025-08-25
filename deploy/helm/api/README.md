# Inventory API Helm Chart

這是一個用於部署 Inventory API 到 Kubernetes 集群的 Helm Chart。

## 功能特性

- 🚀 **完整的 Kubernetes 部署** - 包含所有必要的資源
- 🔧 **高度可客製化** - 所有配置都可以通過 values 文件調整
- 🏗️ **多環境支援** - 提供開發、生產和自定義環境的範例
- 📊 **監控就緒** - 內建 ServiceMonitor 支援
- 🔒 **安全配置** - 支援 Pod Security Policy 和 Network Policy
- ⚡ **自動擴展** - 內建 HPA 支援
- 🛡️ **高可用性** - 支援 Pod Disruption Budget
- 🔍 **健康檢查** - 完整的 Liveness 和 Readiness 探針
- 🌐 **Istio 支援** - 內建 Gateway 和 VirtualService 配置
- 🔐 **自動 SSL 證書** - 支援 cert-manager 自動證書管理

## 前置需求

- Kubernetes 1.19+
- Helm 3.0+
- kubectl 配置到目標集群
- NGINX Ingress Controller 或 Traefik (傳統 Ingress 模式)
- Istio (推薦，用於 Gateway 和 VirtualService)
- cert-manager (用於自動 SSL 證書管理)

## 快速開始

### 1. 添加 Helm Repository

```bash
# 如果使用 GitLab Container Registry
helm repo add inventory-api https://gitlab.com/api/v4/projects/YOUR_PROJECT_ID/packages/helm/stable
helm repo update
```

### 2. 安裝 Chart

#### 使用預設配置

```bash
helm install inventory-api ./helm/inventory-api
```

#### 使用開發環境配置

```bash
helm install inventory-api-dev ./helm/inventory-api -f ./helm/inventory-api/values-dev.yaml
```

#### 使用生產環境配置

```bash
helm install inventory-api-prod ./helm/inventory-api -f ./helm/inventory-api/values-prod.yaml
```

#### 使用自定義配置

```bash
helm install my-inventory-api ./helm/inventory-api -f ./helm/inventory-api/values-custom.yaml
```

### 3. 升級部署

```bash
helm upgrade inventory-api ./helm/inventory-api
```

### 4. 卸載部署

```bash
helm uninstall inventory-api
```

## 配置選項

### 主要配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `nameOverride` | 覆蓋應用程式名稱 | `""` |
| `fullnameOverride` | 覆蓋完整應用程式名稱 | `""` |
| `image.registry` | Docker 映像註冊表 | `registry.gitlab.com` |
| `image.repository` | Docker 映像倉庫 | `your-org/inventory-api` |
| `image.tag` | Docker 映像標籤 | `latest` |
| `image.pullPolicy` | 映像拉取策略 | `IfNotPresent` |
| `deployment.replicas` | Pod 副本數量 | `3` |
| `service.type` | 服務類型 | `ClusterIP` |
| `ingress.enabled` | 是否啟用 Ingress | `true` |

### 資源配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `resources.limits.cpu` | CPU 限制 | `500m` |
| `resources.limits.memory` | 記憶體限制 | `512Mi` |
| `resources.requests.cpu` | CPU 請求 | `250m` |
| `resources.requests.memory` | 記憶體請求 | `256Mi` |

### 自動擴展配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `hpa.enabled` | 是否啟用 HPA | `true` |
| `hpa.minReplicas` | 最小副本數 | `2` |
| `hpa.maxReplicas` | 最大副本數 | `10` |
| `hpa.targetCPUUtilizationPercentage` | CPU 使用率目標 | `70` |
| `hpa.targetMemoryUtilizationPercentage` | 記憶體使用率目標 | `80` |

### 環境變數配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `env.DJANGO_SETTINGS_MODULE` | Django 設定模組 | `inventory.settings` |
| `env.DEBUG` | Django 除錯模式 | `False` |
| `env.DB_HOST` | 資料庫主機 | `postgres-service` |
| `env.REDIS_HOST` | Redis 主機 | `redis-service` |

### Istio 配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `istio.gateway.enabled` | 是否啟用 Istio Gateway | `true` |
| `istio.gateway.name` | Gateway 名稱 | `inventory-api-gateway` |
| `istio.gateway.namespace` | Gateway 命名空間 | `istio-system` |
| `istio.gateway.hosts` | Gateway 主機列表 | `["inventory-api.your-domain.com"]` |
| `istio.virtualService.enabled` | 是否啟用 VirtualService | `true` |
| `istio.virtualService.name` | VirtualService 名稱 | `inventory-api-vs` |

### cert-manager 配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `certificate.enabled` | 是否啟用證書管理 | `true` |
| `certificate.name` | 證書名稱 | `inventory-api-tls-cert` |
| `certificate.namespace` | 證書命名空間 | `istio-system` |
| `certificate.issuerRef.name` | 證書發行者 | `letsencrypt-prod` |
| `certificate.dnsNames` | 證書域名列表 | `["inventory-api.your-domain.com"]` |

## 環境範例

### 開發環境

```bash
helm install inventory-dev ./helm/inventory-api -f values-dev.yaml
```

特點：

- 較少的資源配置
- 啟用除錯模式
- 較寬鬆的安全設定
- 較少的副本數
- 禁用 HTTPS 重定向 (開發環境)
- 使用 staging 證書發行者

### 生產環境

```bash
helm install inventory-prod ./helm/inventory-api -f values-prod.yaml
```

特點：

- 較高的資源配置
- 禁用除錯模式
- 嚴格的安全設定
- 較多的副本數和高可用性
- 啟用 HTTPS 重定向
- 使用生產證書發行者

### 自定義環境

```bash
helm install my-inventory ./helm/inventory-api -f values-custom.yaml
```

特點：

- 完全可客製化的配置
- 支援自定義映像註冊表
- 支援自定義 Ingress 控制器
- 支援自定義監控配置

## 進階配置

### 自定義映像

```yaml
image:
  registry: my-registry.com
  repository: my-org/inventory-api
  tag: "v1.2.3"
  pullPolicy: IfNotPresent
```

### 自定義 Istio Gateway

```yaml
istio:
  gateway:
    enabled: true
    name: "my-custom-gateway"
    namespace: "istio-system"
    hosts:
      - "api.example.com"
      - "*.api.example.com"
    tls:
      mode: SIMPLE
      credentialName: "my-tls-secret"
    http:
      redirectToHttps: true
```

### 自定義 Istio VirtualService

```yaml
istio:
  virtualService:
    enabled: true
    name: "my-custom-vs"
    hosts:
      - "api.example.com"
    gateways:
      - "istio-system/my-custom-gateway"
    http:
      - match:
          - uri:
              prefix: "/api/v1"
        route:
          - destination:
              host: "inventory-api"
              port:
                number: 80
        timeout: 30s
        retries:
          attempts: 3
          perTryTimeout: 10s
```

### 自定義 cert-manager 證書

```yaml
certificate:
  enabled: true
  name: "my-custom-cert"
  namespace: "istio-system"
  secretName: "my-tls-secret"
  issuerRef:
    name: "letsencrypt-prod"
    kind: "ClusterIssuer"
  dnsNames:
    - "api.example.com"
    - "*.api.example.com"
  duration: "2160h"  # 90 days
  renewBefore: "360h"  # 15 days
```

### 自定義 Ingress

```yaml
ingress:
  enabled: true
  className: "traefik"
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: "websecure"
  hosts:
    - host: api.mycompany.com
      paths:
        - path: /
          pathType: Prefix
```

### 自定義資源限制

```yaml
resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 1000m
    memory: 1Gi
```

### 自定義環境變數

```yaml
env:
  CUSTOM_SETTING: "custom-value"
  LOG_LEVEL: "DEBUG"
  CACHE_TIMEOUT: "300"
```

### 自定義 ConfigMap

```yaml
configMap:
  additionalData:
    ENVIRONMENT: "custom"
    FEATURE_FLAGS: "feature1,feature2"
```

### 自定義 Secrets

Chart 支援自動生成安全的密碼和密鑰。當 `secrets.create` 設為 `true` 時，以下欄位會自動生成：

#### 自動生成欄位

| 欄位 | 描述 | 生成規則 |
|------|------|----------|
| `POSTGRES_PASSWORD` | PostgreSQL 資料庫密碼 | 32 字元隨機字母數字組合 |
| `DJANGO_SUPERUSER_PASSWORD` | Django 超級使用者密碼 | 32 字元隨機字母數字組合 |
| `DJANGO_SECRET_KEY` | Django 密鑰 | 50 字元隨機字母數字組合 |
| `DJANGO_BACKDOOR_API_TOKEN` | 後門 API 令牌 | 32 字元隨機字母數字組合 |
| `PGADMIN_DEFAULT_PASSWORD` | PGAdmin 密碼 | 32 字元隨機字母數字組合 |

#### 使用方式

```yaml
secrets:
  create: true
  data:
    # 留空以自動生成
    POSTGRES_PASSWORD: ""
    DJANGO_SUPERUSER_PASSWORD: ""
    DJANGO_SECRET_KEY: ""
    DJANGO_BACKDOOR_API_TOKEN: ""
    PGADMIN_DEFAULT_PASSWORD: ""
    
    # 或提供自定義值
    POSTGRES_USER: "myuser"
    DJANGO_SUPERUSER_USERNAME: "admin"
```

#### 手動設定密碼

如果您想使用預設密碼，可以在 values 文件中設定：

```yaml
secrets:
  create: true
  data:
    POSTGRES_PASSWORD: ""
    DJANGO_SUPERUSER_PASSWORD: ""
    DJANGO_SECRET_KEY: ""
```

### 自定義節點選擇器

```yaml
nodeSelector:
  node-type: "high-performance"
  environment: "production"
```

### 自定義親和性

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app.kubernetes.io/name
          operator: In
          values:
          - virtflow-api
      topologyKey: topology.kubernetes.io/zone
```

### 自定義 Init Containers

```yaml
initContainers:
  - name: init-db
    image: postgres:13
    command: ['sh', '-c', 'until pg_isready -h my-postgres; do sleep 2; done;']
```

### 自定義 Sidecar Containers

```yaml
sidecars:
  - name: nginx-sidecar
    image: nginx:alpine
    ports:
      - name: nginx
        containerPort: 80
```

## 監控和日誌

### ServiceMonitor

```yaml
serviceMonitor:
  enabled: true
  interval: 30s
  scrapeTimeout: 10s
  path: /metrics
  port: http
```

### 日誌配置

```yaml
volumes:
  - name: logs-volume
    persistentVolumeClaim:
      claimName: virtflow-logs-pvc

volumeMounts:
  - name: logs-volume
    mountPath: /app/logs
```

## 安全配置

### Network Policy

```yaml
networkPolicy:
  enabled: true
  ingressRules:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egressRules:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
```

### Pod Security Policy

```yaml
podSecurityPolicy:
  enabled: true
  privileged: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
```

## 故障排除

### 常見問題

1. **Pod 無法啟動**

   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. **映像拉取失敗**

   ```bash
   kubectl describe pod <pod-name>
   # 檢查 imagePullSecrets 配置
   ```

3. **Ingress 無法訪問**

   ```bash
   kubectl get ingress
   kubectl describe ingress <ingress-name>
   ```

4. **HPA 不工作**

   ```bash
   kubectl get hpa
   kubectl describe hpa <hpa-name>
   # 檢查 Metrics Server 是否安裝
   ```

### 有用的命令

```bash
# 檢查部署狀態
helm status inventory-api

# 查看生成的 YAML
helm template inventory-api ./helm/inventory-api

# 驗證 Chart
helm lint ./helm/inventory-api

# 查看歷史
helm history inventory-api

# 回滾到上一個版本
helm rollback inventory-api

# 檢查 Istio Gateway 狀態
kubectl get gateway -n istio-system

# 檢查 Istio VirtualService 狀態
kubectl get virtualservice

# 檢查 cert-manager 證書狀態
kubectl get certificate -n istio-system

# 檢查證書詳細信息
kubectl describe certificate inventory-api-tls-cert -n istio-system
```

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個 Helm Chart。

## 授權

此專案採用 MIT 授權條款。
