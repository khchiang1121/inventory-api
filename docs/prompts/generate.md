# React Frontend Development Prompt for VirtFlow Virtualization Resource Management System

## Project Overview

You are tasked with creating a comprehensive React frontend for **VirtFlow**, a Django REST framework-based virtualization resource management system. This system manages physical infrastructure, virtual machines, Kubernetes clusters, and multi-tenant environments.

## Technical Requirements

### Core Technologies

- **React 18+** with TypeScript
- **React Router v6** for navigation
- **Axios** for API communication
- **React Query/TanStack Query** for state management and caching
- **Material-UI (MUI) v5** or **Ant Design** for UI components
- **React Hook Form** for form handling
- **React Table** or **MUI DataGrid** for data tables
- **Recharts** or **Chart.js** for data visualization
- **React Hot Toast** or **Snackbar** for notifications

### Development Setup

- **Vite** as build tool
- **ESLint** and **Prettier** for code quality
- **Jest** and **React Testing Library** for testing
- **Docker** support for containerization

## API Integration

### Base Configuration

- **Base URL**: `http://localhost:8201/api/v1/`
- **Authentication**: Token-based (endpoint: `/api/token/`)
- **API Documentation**: Available at `/api/v1/swagger-ui` and `/api/v1/redoc`

### Core API Endpoints to Implement

#### 1. Infrastructure Management

- `GET/POST/PUT/DELETE /fab/` - Data center fabrication management
- `GET/POST/PUT/DELETE /phases/` - Phase management
- `GET/POST/PUT/DELETE /data-centers/` - Data center management
- `GET/POST/PUT/DELETE /rooms/` - Room management
- `GET/POST/PUT/DELETE /racks/` - Rack management with BGP/AS configuration

#### 2. Network Management

- `GET/POST/PUT/DELETE /vlans/` - VLAN management
- `GET/POST/PUT/DELETE /vrfs/` - VRF management
- `GET/POST/PUT/DELETE /bgp-configs/` - BGP configuration
- `GET/POST/PUT/DELETE /network-interfaces/` - Network interface management

#### 3. Purchase Management

- `GET/POST/PUT/DELETE /purchase-requisitions/` - Purchase requisition tracking
- `GET/POST/PUT/DELETE /purchase-orders/` - Purchase order management

#### 4. Baremetal Management

- `GET/POST/PUT/DELETE /brands/` - Server brand management
- `GET/POST/PUT/DELETE /baremetal-models/` - Server model specifications
- `GET/POST/PUT/DELETE /baremetal-groups/` - Baremetal group management
- `GET/POST/PUT/DELETE /baremetals/` - Physical server management
- `GET/POST/PUT/DELETE /baremetal-group-tenant-quotas/` - Tenant quota management

#### 5. Virtualization Management

- `GET/POST/PUT/DELETE /tenants/` - Multi-tenant management
- `GET/POST/PUT/DELETE /vm-specifications/` - VM specification templates
- `GET/POST/PUT/DELETE /virtual-machines/` - Virtual machine lifecycle management

#### 6. Kubernetes Management

- `GET/POST/PUT/DELETE /k8s-clusters/` - Kubernetes cluster management
- `GET/POST/PUT/DELETE /k8s-cluster-plugins/` - Cluster plugin management
- `GET/POST/PUT/DELETE /service-meshes/` - Service mesh configuration
- `GET/POST/PUT/DELETE /k8s-cluster-service-meshes/` - Cluster-service mesh associations
- `GET/POST/PUT/DELETE /bastion-cluster-associations/` - Bastion host associations

#### 7. User Management

- `GET/POST/PUT/DELETE /users/` - User management
- `GET/POST/PUT/DELETE /permissions/` - Object-level permissions

## Core Features to Implement

### 1. Dashboard

- **Overview Cards**: Total servers, VMs, clusters, active tenants
- **Resource Utilization Charts**: CPU, memory, storage usage across infrastructure
- **Recent Activity Feed**: Latest VM deployments, cluster changes, maintenance events
- **Quick Actions**: Create VM, deploy cluster, add server
- **Status Indicators**: System health, pending tasks, alerts

### 2. Infrastructure Management

- **Data Center View**: Hierarchical view (Fab → Phase → Data Center → Room → Rack)
- **Rack Management**: Visual rack layout with server positions
- **Network Configuration**: VLAN, VRF, BGP configuration management
- **Physical Server Inventory**: Detailed server specifications and status

### 3. Virtual Machine Management

- **VM Dashboard**: List all VMs with filtering and search
- **VM Creation Wizard**: Step-by-step VM provisioning
- **VM Details**: Resource usage, network configuration, associated services
- **VM Operations**: Start, stop, restart, delete, snapshot
- **VM Templates**: Predefined specifications for quick deployment

### 4. Kubernetes Cluster Management

- **Cluster Overview**: Multi-cluster dashboard with health status
- **Cluster Creation Wizard**: Guided cluster deployment
- **Node Management**: Add/remove worker nodes, scaling
- **Plugin Management**: Install, configure, update cluster plugins
- **Service Mesh Integration**: Istio, Cilium configuration
- **Bastion Host Management**: Secure cluster access configuration

### 5. Multi-Tenant Management

- **Tenant Dashboard**: Resource allocation and usage per tenant
- **Quota Management**: CPU, memory, storage quotas per tenant
- **Resource Isolation**: Visual representation of tenant boundaries
- **Billing/Usage Tracking**: Resource consumption metrics

### 6. Maintenance Management

- **Maintenance Scheduling**: Plan and track maintenance windows
- **Maintainer Assignment**: Assign maintenance responsibilities
- **Maintenance History**: Track past maintenance activities
- **Impact Assessment**: Show affected services during maintenance

## UI/UX Requirements

### Design System

- **Modern, Clean Interface**: Professional enterprise-grade design
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Toggle between themes
- **Accessibility**: WCAG 2.1 AA compliance
- **Internationalization**: Support for multiple languages (English primary)

### Navigation Structure

```
Dashboard
├── Infrastructure
│   ├── Data Centers
│   ├── Racks
│   ├── Physical Servers
│   └── Network
├── Virtualization
│   ├── Virtual Machines
│   ├── VM Specifications
│   └── Tenants
├── Kubernetes
│   ├── Clusters
│   ├── Plugins
│   └── Service Mesh
├── Maintenance
│   ├── Schedule
│   ├── Assignments
│   └── History
└── Administration
    ├── Users
    ├── Permissions
    └── Settings
```

### Key UI Components

- **Data Tables**: Sortable, filterable, paginated tables with bulk actions
- **Forms**: Multi-step wizards for complex operations
- **Charts**: Resource utilization, capacity planning, performance metrics
- **Modals**: Quick actions, confirmations, detailed views
- **Notifications**: Success, error, warning messages
- **Loading States**: Skeleton loaders, progress indicators

## Advanced Features

### 1. Real-time Monitoring

- **WebSocket Integration**: Real-time status updates
- **Live Metrics**: CPU, memory, network usage
- **Alert System**: Critical events and notifications

### 2. Advanced Filtering and Search

- **Global Search**: Search across all resources
- **Advanced Filters**: Multi-criteria filtering
- **Saved Views**: User-specific filter presets

### 3. Bulk Operations

- **Batch VM Management**: Start/stop multiple VMs
- **Mass Configuration**: Apply settings to multiple resources
- **Bulk Import/Export**: CSV/JSON data import/export

### 4. Reporting and Analytics

- **Resource Reports**: Capacity planning, utilization trends
- **Cost Analysis**: Resource cost tracking per tenant
- **Performance Metrics**: Response times, throughput

## Security Requirements

### Authentication & Authorization

- **JWT Token Management**: Secure token storage and refresh
- **Role-based Access Control**: Different views based on user permissions
- **Session Management**: Secure session handling
- **API Security**: CSRF protection, input validation

### Data Protection

- **Sensitive Data Masking**: Hide sensitive information in UI
- **Audit Logging**: Track user actions and changes
- **Data Encryption**: Secure transmission and storage

## Performance Requirements

### Optimization

- **Code Splitting**: Lazy loading for routes and components
- **Image Optimization**: Compressed images and icons
- **Caching Strategy**: API response caching, local storage
- **Bundle Size**: Optimized bundle under 2MB initial load

### Monitoring

- **Error Tracking**: Sentry or similar error monitoring
- **Performance Monitoring**: Core Web Vitals tracking
- **User Analytics**: Usage patterns and feature adoption

## Testing Strategy

### Test Coverage

- **Unit Tests**: Component testing with React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: Critical user workflows with Playwright
- **Visual Regression**: UI component testing

### Quality Assurance

- **TypeScript**: Strict type checking
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Husky**: Pre-commit hooks

## Deployment and DevOps

### Build Configuration

- **Environment Variables**: Separate configs for dev/staging/prod
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Health Checks**: Application health monitoring

### Documentation

- **Component Documentation**: Storybook for UI components
- **API Documentation**: Integration guides
- **User Manual**: Feature documentation and tutorials

## Deliverables

1. **Complete React Application** with all core features
2. **Comprehensive Test Suite** with >80% coverage
3. **Documentation** including setup, API integration, and user guides
4. **Docker Configuration** for easy deployment
5. **Performance Optimization** with bundle analysis
6. **Accessibility Compliance** with audit report

## Success Criteria

- **Functional Completeness**: All API endpoints integrated and functional
- **User Experience**: Intuitive, responsive, and accessible interface
- **Performance**: Fast loading times and smooth interactions
- **Security**: Secure authentication and data handling
- **Maintainability**: Clean, well-documented, and testable code
- **Scalability**: Architecture supports future feature additions

This frontend should provide a comprehensive, enterprise-grade interface for managing the entire VirtFlow virtualization infrastructure, enabling efficient resource management, monitoring, and operations for both administrators and end users.
