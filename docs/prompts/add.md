I'll help you create a comprehensive prompt for the coding agent to implement all the resource tabs and functionality. First, let me explore the current codebase to understand the structure and what's already implemented.

Ran tool
Ran tool
Ran tool
Read file: frontend/src/App.tsx
Ran tool
Read file: frontend/src/pages/infrastructure/DataCentersPage.tsx
Ran tool
Read file: frontend/src/pages/infrastructure/ServersPage.tsx
Ran tool
Ran tool
Ran tool
Ran tool
Ran tool
Ran tool
Read file: frontend/src/services/api/client.ts
Ran tool
Read file: frontend/src/types/index.ts
Ran tool
Read file: frontend/src/types/api/infrastructure.ts
Ran tool
Ran tool
Read file: frontend/src/components/common/Sidebar.tsx
Ran tool
Ran tool
Ran tool
Read file: virtflow/api/v1/urls.py
Now I have a comprehensive understanding of the current codebase. Let me create a detailed prompt for the coding agent to implement all the resource tabs and functionality.

Based on my analysis of the codebase, here's a comprehensive prompt for the coding agent:

---

# Comprehensive Implementation Prompt for VirtFlow Resource Management System

## Project Overview

You are tasked with implementing the complete functionality for all resource management tabs in the VirtFlow infrastructure management system. The frontend is built with React + TypeScript + Material-UI, and the backend is Django REST Framework. Currently, all pages show placeholder content and need full CRUD functionality, data visualization, and real-time monitoring capabilities.

## Current State Analysis

- **Frontend**: React + TypeScript + Material-UI with React Query for state management
- **Backend**: Django REST Framework with comprehensive API endpoints already defined
- **Authentication**: JWT-based authentication system implemented
- **Navigation**: Sidebar navigation with all resource tabs defined
- **Types**: Comprehensive TypeScript interfaces already defined for all entities

## Implementation Requirements

### 1. Infrastructure Management Pages

#### Data Centers Page (`/infrastructure/data-centers`)

**Required Features:**

- **Data Grid**: Display all data centers with columns: Name, Location, Phase, Capacity, Power Capacity, Cooling Capacity, Status, Created Date
- **CRUD Operations**: Add/Edit/Delete data centers with form validation
- **Filtering & Search**: Filter by status, phase, location; search by name/description
- **Capacity Monitoring**: Real-time charts showing power usage, cooling efficiency, space utilization
- **Room Management**: Nested view of rooms within each data center
- **Status Indicators**: Visual status badges with color coding
- **Bulk Operations**: Bulk status updates, export to CSV/Excel

#### Racks Page (`/infrastructure/racks`)

**Required Features:**

- **Data Grid**: Display racks with columns: Name, Room, Data Center, Position, Height Units, Used/Available Units, Power Capacity, Status
- **Visual Rack Layout**: Interactive rack visualization showing unit allocation
- **Server Assignment**: Drag-and-drop interface for server placement
- **Power Monitoring**: Real-time power consumption charts
- **Capacity Planning**: Available space indicators and warnings
- **BGP Configuration**: Network configuration for each rack

#### Servers Page (`/infrastructure/servers`)

**Required Features:**

- **Data Grid**: Display baremetal servers with columns: Name, Model, Group, Rack, Position, Status, IP Address, Power Status, CPU/Memory Usage
- **Server Details**: Detailed view with specifications, network interfaces, performance metrics
- **Real-time Monitoring**: Live CPU, memory, disk, temperature monitoring with charts
- **Power Management**: Power on/off, reboot, shutdown operations
- **Network Configuration**: IP assignment, VLAN configuration
- **Health Monitoring**: Automated health checks and alerts

#### Network Page (`/infrastructure/network`)

**Required Features:**

- **VLAN Management**: Create, edit, delete VLANs with subnet configuration
- **VRF Management**: Virtual routing and forwarding configuration
- **BGP Configuration**: Border Gateway Protocol setup and monitoring
- **Network Topology**: Visual network diagram showing connections
- **Interface Management**: Network interface configuration and monitoring
- **Traffic Analysis**: Network traffic charts and bandwidth monitoring

### 2. Virtualization Management Pages

#### Virtual Machines Page (`/virtualization/virtual-machines`)

**Required Features:**

- **Data Grid**: Display VMs with columns: Name, Tenant, Specification, Host Server, Status, IP Address, CPU/Memory Usage
- **VM Operations**: Start, stop, pause, resume, reboot, snapshot operations
- **Resource Monitoring**: Real-time CPU, memory, disk, network usage
- **Console Access**: Web-based console access to VMs
- **Migration Tools**: Live migration between hosts
- **Backup Management**: Automated backup scheduling and restoration

#### VM Specifications Page (`/virtualization/vm-specifications`)

**Required Features:**

- **Specification Templates**: Predefined VM configurations
- **Resource Allocation**: CPU, memory, storage, network allocation
- **OS Templates**: Operating system image management
- **Performance Profiles**: High-performance, balanced, cost-optimized profiles
- **Validation Rules**: Resource constraint validation

#### Tenants Page (`/virtualization/tenants`)

**Required Features:**

- **Tenant Management**: Create, edit, delete tenant organizations
- **Resource Quotas**: CPU, memory, storage, network quota management
- **Usage Tracking**: Real-time resource usage monitoring
- **Billing Integration**: Resource consumption billing
- **Access Control**: User assignment and permission management

### 3. Kubernetes Management Pages

#### Clusters Page (`/kubernetes/clusters`)

**Required Features:**

- **Cluster Overview**: Display all K8s clusters with health status
- **Node Management**: Worker node configuration and monitoring
- **Cluster Operations**: Scale, upgrade, backup operations
- **Resource Monitoring**: Pod, service, deployment monitoring
- **Log Management**: Centralized logging and log analysis
- **Security**: RBAC, network policies, security contexts

#### Plugins Page (`/kubernetes/plugins`)

**Required Features:**

- **Plugin Catalog**: Available plugins with descriptions and versions
- **Installation Management**: Install, update, uninstall plugins
- **Configuration**: Plugin-specific configuration management
- **Health Monitoring**: Plugin status and performance monitoring
- **Dependency Management**: Plugin dependencies and conflicts

#### Service Mesh Page (`/kubernetes/service-mesh`)

**Required Features:**

- **Service Mesh Overview**: Istio/Linkerd deployment status
- **Traffic Management**: Load balancing, routing, circuit breaking
- **Security**: mTLS, authorization policies
- **Observability**: Metrics, tracing, logging integration
- **Gateway Management**: Ingress/egress gateway configuration

### 4. Maintenance Management Pages

#### Maintenance Schedule Page (`/maintenance/schedule`)

**Required Features:**

- **Calendar View**: Interactive calendar showing scheduled maintenance
- **Schedule Management**: Create, edit, delete maintenance windows
- **Resource Impact**: Show affected resources during maintenance
- **Notification System**: Automated notifications for stakeholders
- **Approval Workflow**: Maintenance approval process
- **Conflict Detection**: Detect scheduling conflicts

#### Maintenance History Page (`/maintenance/history`)

**Required Features:**

- **Historical Records**: Complete maintenance history
- **Performance Metrics**: Maintenance impact on system performance
- **Cost Tracking**: Maintenance cost analysis
- **Documentation**: Maintenance procedures and outcomes
- **Trend Analysis**: Maintenance pattern analysis

### 5. Administration Pages

#### Users Page (`/admin/users`)

**Required Features:**

- **User Management**: Create, edit, delete user accounts
- **Role Assignment**: Role-based access control
- **Permission Management**: Granular permission assignment
- **Activity Logging**: User activity tracking
- **Authentication**: Multi-factor authentication setup

#### Permissions Page (`/admin/permissions`)

**Required Features:**

- **Permission Matrix**: Visual permission matrix
- **Role Templates**: Predefined role templates
- **Permission Auditing**: Permission change tracking
- **Access Reviews**: Periodic access reviews

#### Settings Page (`/admin/settings`)

**Required Features:**

- **System Configuration**: Global system settings
- **Notification Settings**: Email, SMS, webhook configurations
- **Security Settings**: Password policies, session management
- **Backup Configuration**: Automated backup settings
- **Integration Settings**: Third-party integrations

## Technical Implementation Requirements

### Frontend Components to Create

1. **Data Grid Component** (`components/common/DataGrid.tsx`)
   - Sortable columns
   - Filtering capabilities
   - Pagination
   - Bulk selection
   - Export functionality
   - Row actions menu

2. **Form Components** (`components/forms/`)
   - Generic form builder
   - Validation system
   - Field components (text, select, multiselect, date, etc.)
   - Wizard forms for complex operations

3. **Modal Components** (`components/modals/`)
   - Confirmation dialogs
   - Form modals
   - Detail view modals
   - Bulk operation modals

4. **Chart Components** (`components/charts/`)
   - Line charts for time series data
   - Bar charts for comparisons
   - Pie charts for distributions
   - Gauge charts for metrics
   - Real-time updating capabilities

5. **Status Components** (`components/common/`)
   - Status badges
   - Progress indicators
   - Health indicators
   - Alert components

### API Service Layer

Create service files for each resource type:

- `services/api/infrastructure.ts` - Data centers, racks, servers, network
- `services/api/virtualization.ts` - VMs, specifications, tenants
- `services/api/kubernetes.ts` - Clusters, plugins, service mesh
- `services/api/maintenance.ts` - Schedule, history
- `services/api/admin.ts` - Users, permissions, settings

### State Management

Use React Query for:

- Data fetching and caching
- Optimistic updates
- Background refetching
- Error handling
- Loading states

### Real-time Features

Implement WebSocket connections for:

- Real-time monitoring data
- Status updates
- Alert notifications
- Live charts

### Error Handling

- Global error boundary
- API error handling
- User-friendly error messages
- Retry mechanisms
- Offline support

### Performance Optimization

- Lazy loading of components
- Virtual scrolling for large datasets
- Image optimization
- Bundle splitting
- Caching strategies

## Implementation Priority

### Phase 1 (Core CRUD - Week 1)

1. Data Centers page with full CRUD
2. Racks page with basic functionality
3. Servers page with basic monitoring
4. Basic form components and data grid

### Phase 2 (Advanced Features - Week 2)

1. Real-time monitoring and charts
2. Network management
3. VM management
4. Advanced filtering and search

### Phase 3 (Kubernetes & Maintenance - Week 3)

1. Kubernetes cluster management
2. Maintenance scheduling
3. User and permission management
4. Advanced analytics

### Phase 4 (Polish & Optimization - Week 4)

1. Performance optimization
2. Real-time notifications
3. Advanced visualizations
4. Comprehensive testing

## Code Quality Requirements

- **TypeScript**: Strict type checking, no `any` types
- **Testing**: Unit tests for components, integration tests for API calls
- **Documentation**: JSDoc comments for all functions and components
- **Accessibility**: WCAG 2.1 AA compliance
- **Responsive Design**: Mobile-first approach
- **Performance**: Lighthouse score > 90
- **Security**: Input validation, XSS prevention, CSRF protection

## File Structure to Follow

```
frontend/src/
├── components/
│   ├── common/
│   │   ├── DataGrid.tsx
│   │   ├── StatusBadge.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorBoundary.tsx
│   ├── forms/
│   │   ├── FormBuilder.tsx
│   │   ├── fields/
│   │   └── validation/
│   ├── modals/
│   │   ├── ConfirmationModal.tsx
│   │   ├── FormModal.tsx
│   │   └── DetailModal.tsx
│   ├── charts/
│   │   ├── LineChart.tsx
│   │   ├── BarChart.tsx
│   │   └── GaugeChart.tsx
│   └── infrastructure/
│       ├── DataCenterCard.tsx
│       ├── RackVisualization.tsx
│       └── ServerMonitor.tsx
├── services/
│   └── api/
│       ├── infrastructure.ts
│       ├── virtualization.ts
│       ├── kubernetes.ts
│       ├── maintenance.ts
│       └── admin.ts
├── hooks/
│   ├── useApi.ts
│   ├── useRealTime.ts
│   └── useWebSocket.ts
└── utils/
    ├── formatters.ts
    ├── validators.ts
    └── constants.ts
```

## Success Criteria

1. **Functionality**: All CRUD operations work correctly
2. **Performance**: Page load times < 2 seconds
3. **User Experience**: Intuitive navigation and clear feedback
4. **Data Accuracy**: Real-time data synchronization
5. **Error Handling**: Graceful error handling with user feedback
6. **Accessibility**: Screen reader compatible
7. **Mobile Responsive**: Works on all device sizes
8. **Security**: Secure data handling and user authentication

## Additional Notes

- Follow Material-UI design system consistently
- Implement proper loading states and skeleton screens
- Use React Query for efficient data fetching and caching
- Implement proper error boundaries and fallback UI
- Add comprehensive logging for debugging
- Ensure all forms have proper validation
- Implement proper keyboard navigation
- Add tooltips and help text for complex features

This implementation should transform the placeholder pages into a fully functional infrastructure management system with modern UI/UX, real-time monitoring, and comprehensive resource management capabilities.
