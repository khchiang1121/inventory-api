# Inventory API Helm Chart - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Inventory API using the enhanced Helm chart with Istio service mesh and cert-manager integration.

## What's New

### Recent Updates

- ✅ Renamed all "virtflow" references to "inventory-api"
- ✅ Added Istio Gateway and VirtualService support
- ✅ Added cert-manager Certificate integration
- ✅ Updated all environment-specific values files
- ✅ Enhanced documentation with new features

### New Components Added

1. **Istio Gateway** (`templates/gateway.yaml`)
   - Configures ingress traffic management
   - Supports HTTPS termination
   - HTTP to HTTPS redirection

2. **Istio VirtualService** (`templates/virtualservice.yaml`)
   - Advanced traffic routing
   - Timeout and retry policies
   - Header manipulation support

3. **cert-manager Certificate** (`templates/certificate.yaml`)
   - Automated SSL certificate management
   - Let's Encrypt integration
   - Certificate renewal automation

## Deployment Options

### Option 1: Traditional Ingress (Existing)

```bash
# Uses NGINX Ingress Controller
helm install inventory-api ./helm/inventory-api \
  --set istio.gateway.enabled=false \
  --set istio.virtualService.enabled=false \
  --set certificate.enabled=false
```

### Option 2: Istio Service Mesh (Recommended)

```bash
# Uses Istio Gateway and VirtualService
helm install inventory-api ./helm/inventory-api \
  --set ingress.enabled=false
```

### Option 3: Hybrid Approach

```bash
# Uses both Ingress and Istio (for migration)
helm install inventory-api ./helm/inventory-api
```

## Environment-Specific Deployments

### Development Environment

```bash
helm install inventory-api-dev ./helm/inventory-api \
  -f ./helm/inventory-api/values-dev.yaml \
  --namespace dev \
  --create-namespace
```

**Features:**

- Istio Gateway with staging certificates
- No HTTPS redirection for easier development
- Lower resource limits
- Debug mode enabled

### Production Environment

```bash
helm install inventory-api-prod ./helm/inventory-api \
  -f ./helm/inventory-api/values-prod.yaml \
  --namespace production \
  --create-namespace
```

**Features:**

- Production Let's Encrypt certificates
- HTTPS redirection enforced
- High availability configuration
- Strict security policies

### Custom Environment

```bash
helm install my-inventory-api ./helm/inventory-api \
  -f ./helm/inventory-api/values-custom.yaml \
  --namespace custom \
  --create-namespace
```

**Features:**

- Wildcard certificate support
- Advanced routing rules
- Custom timeout and retry policies
- Multiple ingress paths

## Prerequisites

### Required Components

1. **Kubernetes Cluster** (1.19+)
2. **Helm** (3.0+)
3. **Istio** (1.10+) - for service mesh features
4. **cert-manager** (1.5+) - for SSL certificate management

### Installation Commands

#### Install Istio

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Install Istio
istioctl install --set values.defaultRevision=default -y

# Enable sidecar injection
kubectl label namespace default istio-injection=enabled
```

#### Install cert-manager

```bash
# Add cert-manager repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true
```

#### Create ClusterIssuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: istio
```

## Configuration Examples

### Basic Istio Configuration

```yaml
istio:
  gateway:
    enabled: true
    name: "inventory-api-gateway"
    hosts:
      - "api.yourdomain.com"
    tls:
      mode: SIMPLE
      credentialName: "api-tls-cert"
  
  virtualService:
    enabled: true
    hosts:
      - "api.yourdomain.com"
    http:
      - match:
          - uri:
              prefix: "/"
        route:
          - destination:
              host: "inventory-api"
              port:
                number: 80
```

### Advanced Traffic Management

```yaml
istio:
  virtualService:
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
        headers:
          request:
            add:
              x-api-version: "v1"
```

### Certificate Configuration

```yaml
certificate:
  enabled: true
  name: "api-tls-cert"
  namespace: "istio-system"
  issuerRef:
    name: "letsencrypt-prod"
    kind: "ClusterIssuer"
  dnsNames:
    - "api.yourdomain.com"
    - "*.api.yourdomain.com"
  duration: "2160h"  # 90 days
  renewBefore: "360h"  # 15 days
```

## Monitoring and Troubleshooting

### Health Checks

```bash
# Check all components
kubectl get pods,svc,ingress,gateway,vs,cert -A

# Check Istio configuration
istioctl analyze

# Check certificate status
kubectl describe certificate -n istio-system

# Check Gateway status
kubectl describe gateway -n istio-system
```

### Common Issues

1. **Certificate Not Ready**

   ```bash
   kubectl describe certificate inventory-api-tls-cert -n istio-system
   kubectl logs -n cert-manager deployment/cert-manager
   ```

2. **Gateway Not Working**

   ```bash
   kubectl describe gateway inventory-api-gateway -n istio-system
   istioctl proxy-config listeners istio-proxy -n istio-system
   ```

3. **VirtualService Issues**

   ```bash
   kubectl describe virtualservice inventory-api-vs
   istioctl analyze
   ```

## Migration Guide

### From Traditional Ingress to Istio

1. **Phase 1: Deploy with both enabled**

   ```bash
   helm upgrade inventory-api ./helm/inventory-api \
     --set istio.gateway.enabled=true \
     --set istio.virtualService.enabled=true \
     --set ingress.enabled=true
   ```

2. **Phase 2: Test Istio endpoint**

   ```bash
   # Test new Istio endpoint
   curl -H "Host: api.yourdomain.com" http://istio-gateway-ip/health/
   ```

3. **Phase 3: Switch DNS and disable Ingress**

   ```bash
   helm upgrade inventory-api ./helm/inventory-api \
     --set ingress.enabled=false
   ```

## Security Considerations

### Network Policies

The chart includes network policies that work with both traditional Ingress and Istio:

```yaml
networkPolicy:
  enabled: true
  ingressRules:
    - from:
        - namespaceSelector:
            matchLabels:
              name: istio-system
```

### Pod Security

```yaml
podSecurityPolicy:
  enabled: true
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

## Performance Tuning

### Resource Optimization

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

hpa:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Istio Performance

```yaml
istio:
  virtualService:
    http:
      - timeout: 30s
        retries:
          attempts: 3
          perTryTimeout: 10s
```

## Backup and Recovery

### Backup Configuration

```bash
# Backup current configuration
helm get values inventory-api > backup-values.yaml
kubectl get secret inventory-api-tls-cert -o yaml > backup-cert.yaml
```

### Recovery Process

```bash
# Restore from backup
helm upgrade inventory-api ./helm/inventory-api -f backup-values.yaml
kubectl apply -f backup-cert.yaml
```

## Support and Maintenance

### Regular Maintenance Tasks

1. Monitor certificate expiration
2. Update Helm chart versions
3. Review Istio configuration
4. Monitor resource usage

### Getting Help

- Check the main README.md for detailed configuration options
- Review Kubernetes events: `kubectl get events --sort-by=.metadata.creationTimestamp`
- Use Istio troubleshooting: `istioctl analyze`
- Check cert-manager logs: `kubectl logs -n cert-manager deployment/cert-manager`
