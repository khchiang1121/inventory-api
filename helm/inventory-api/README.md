# VirtFlow API Helm Chart

這是一個用於部署 VirtFlow API 到 Kubernetes 集群的 Helm Chart。

## 功能特性

- 🚀 **完整的 Kubernetes 部署** - 包含所有必要的資源
- 🔧 **高度可客製化** - 所有配置都可以通過 values 文件調整
- 🏗️ **多環境支援** - 提供開發、生產和自定義環境的範例
- 📊 **監控就緒** - 內建 ServiceMonitor 支援
- 🔒 **安全配置** - 支援 Pod Security Policy 和 Network Policy
- ⚡ **自動擴展** - 內建 HPA 支援
- 🛡️ **高可用性** - 支援 Pod Disruption Budget
- 🔍 **健康檢查** - 完整的 Liveness 和 Readiness 探針

## 前置需求

- Kubernetes 1.19+
- Helm 3.0+
- kubectl 配置到目標集群
- NGINX Ingress Controller 或 Traefik
- cert-manager (可選，用於 SSL 證書)

## 快速開始

### 1. 添加 Helm Repository

```bash
# 如果使用 GitLab Container Registry
helm repo add virtflow https://gitlab.com/api/v4/projects/YOUR_PROJECT_ID/packages/helm/stable
helm repo update
```

### 2. 安裝 Chart

#### 使用預設配置

```bash
helm install virtflow-api ./helm/virtflow-api
```

#### 使用開發環境配置

```bash
helm install virtflow-api-dev ./helm/virtflow-api -f ./helm/virtflow-api/values-dev.yaml
```

#### 使用生產環境配置

```bash
helm install virtflow-api-prod ./helm/virtflow-api -f ./helm/virtflow-api/values-prod.yaml
```

#### 使用自定義配置

```bash
helm install my-virtflow-api ./helm/virtflow-api -f ./helm/virtflow-api/values-custom.yaml
```

### 3. 升級部署

```bash
helm upgrade virtflow-api ./helm/virtflow-api
```

### 4. 卸載部署

```bash
helm uninstall virtflow-api
```

## 配置選項

### 主要配置

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `nameOverride` | 覆蓋應用程式名稱 | `""` |
| `fullnameOverride` | 覆蓋完整應用程式名稱 | `""` |
| `image.registry` | Docker 映像註冊表 | `registry.gitlab.com` |
| `image.repository` | Docker 映像倉庫 | `your-org/virtflow-api` |
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
| `env.DJANGO_SETTINGS_MODULE` | Django 設定模組 | `virtflow.settings` |
| `env.DEBUG` | Django 除錯模式 | `False` |
| `env.DB_HOST` | 資料庫主機 | `postgres-service` |
| `env.REDIS_HOST` | Redis 主機 | `redis-service` |

## 環境範例

### 開發環境

```bash
helm install virtflow-dev ./helm/virtflow-api -f values-dev.yaml
```

特點：

- 較少的資源配置
- 啟用除錯模式
- 較寬鬆的安全設定
- 較少的副本數

### 生產環境

```bash
helm install virtflow-prod ./helm/virtflow-api -f values-prod.yaml
```

特點：

- 較高的資源配置
- 禁用除錯模式
- 嚴格的安全設定
- 較多的副本數和高可用性

### 自定義環境

```bash
helm install my-virtflow ./helm/virtflow-api -f values-custom.yaml
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
  repository: my-org/virtflow-api
  tag: "v1.2.3"
  pullPolicy: IfNotPresent
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

```yaml
secrets:
  SECRET_KEY: "my-custom-secret-key"
  DB_PASSWORD: "my-secure-password"
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
helm status virtflow-api

# 查看生成的 YAML
helm template virtflow-api ./helm/virtflow-api

# 驗證 Chart
helm lint ./helm/virtflow-api

# 查看歷史
helm history virtflow-api

# 回滾到上一個版本
helm rollback virtflow-api
```

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個 Helm Chart。

## 授權

此專案採用 MIT 授權條款。
