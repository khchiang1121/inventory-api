import { BaseEntity } from './common';

// Infrastructure Management Types
export interface Fabrication extends BaseEntity {
  name: string;
  description?: string;
  location: string;
  status: 'active' | 'inactive' | 'maintenance';
}

export interface Phase extends BaseEntity {
  name: string;
  description?: string;
  fabrication: number;
  fabrication_name?: string;
  status: 'planning' | 'construction' | 'operational' | 'decommissioned';
}

export interface DataCenter extends BaseEntity {
  name: string;
  description?: string;
  phase: number;
  phase_name?: string;
  location: string;
  capacity: number;
  power_capacity: number;
  cooling_capacity: number;
  status: 'active' | 'inactive' | 'maintenance';
}

export interface Room extends BaseEntity {
  name: string;
  description?: string;
  data_center: number;
  data_center_name?: string;
  floor: number;
  dimensions: string;
  temperature_range: string;
  humidity_range: string;
  status: 'active' | 'inactive' | 'maintenance';
}

export interface Rack extends BaseEntity {
  name: string;
  description?: string;
  room: number;
  room_name?: string;
  position: string;
  height_units: number;
  power_capacity: number;
  bgp_as_number?: number;
  bgp_router_id?: string;
  status: 'active' | 'inactive' | 'maintenance' | 'full';
  used_units: number;
  available_units: number;
}

// Network Management Types
export interface VLAN extends BaseEntity {
  vlan_id: number;
  name: string;
  description?: string;
  subnet: string;
  gateway: string;
  dhcp_enabled: boolean;
  status: 'active' | 'inactive';
}

export interface VRF extends BaseEntity {
  name: string;
  description?: string;
  rd: string; // Route Distinguisher
  import_targets: string[];
  export_targets: string[];
  status: 'active' | 'inactive';
}

export interface BGPConfig extends BaseEntity {
  as_number: number;
  router_id: string;
  description?: string;
  neighbors: BGPNeighbor[];
  status: 'active' | 'inactive';
}

export interface BGPNeighbor {
  neighbor_ip: string;
  remote_as: number;
  description?: string;
  status: 'established' | 'idle' | 'active' | 'connect';
}

export interface NetworkInterface extends BaseEntity {
  name: string;
  mac_address: string;
  ip_address?: string;
  interface_type: 'ethernet' | 'fiber' | 'wireless';
  speed: string;
  duplex: 'full' | 'half';
  vlan: number | null;
  vrf: number | null;
  status: 'up' | 'down' | 'unknown';
  server: number;
}

// Server Management Types
export interface Brand extends BaseEntity {
  name: string;
  description?: string;
  website?: string;
  support_contact?: string;
}

export interface BaremetalModel extends BaseEntity {
  name: string;
  brand: number;
  brand_name?: string;
  description?: string;
  cpu_model: string;
  cpu_cores: number;
  cpu_threads: number;
  memory_gb: number;
  storage_type: 'HDD' | 'SSD' | 'NVMe' | 'Hybrid';
  storage_capacity: number;
  network_ports: number;
  power_consumption: number;
  height_units: number;
  specifications: Record<string, any>;
}

export interface BaremetalGroup extends BaseEntity {
  name: string;
  description?: string;
  location: string;
  total_servers: number;
  active_servers: number;
  maintenance_servers: number;
  failed_servers: number;
}

export interface Baremetal extends BaseEntity {
  name: string;
  model: number;
  model_name?: string;
  group: number;
  group_name?: string;
  rack: number;
  rack_name?: string;
  position: number;
  serial_number: string;
  asset_tag?: string;
  status: 'active' | 'inactive' | 'maintenance' | 'failed' | 'retired';
  ip_address?: string;
  mac_address: string;
  power_status: 'on' | 'off' | 'unknown';
  cpu_usage?: number;
  memory_usage?: number;
  disk_usage?: number;
  temperature?: number;
  network_interfaces: NetworkInterface[];
  last_seen?: string;
}

export interface BaremetalGroupTenantQuota extends BaseEntity {
  group: number;
  group_name?: string;
  tenant: number;
  tenant_name?: string;
  cpu_quota: number;
  memory_quota: number;
  storage_quota: number;
  network_quota: number;
  used_cpu: number;
  used_memory: number;
  used_storage: number;
  used_network: number;
}

// Purchase Management Types
export interface PurchaseRequisition extends BaseEntity {
  requisition_number: string;
  title: string;
  description: string;
  requestor: number;
  requestor_name?: string;
  department: string;
  total_cost: number;
  currency: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'draft' | 'submitted' | 'approved' | 'rejected' | 'cancelled';
  items: PurchaseRequisitionItem[];
  approval_date?: string;
  approved_by?: number;
  approved_by_name?: string;
}

export interface PurchaseRequisitionItem {
  id: number;
  item_name: string;
  description: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  vendor?: string;
  part_number?: string;
}

export interface PurchaseOrder extends BaseEntity {
  order_number: string;
  requisition: number;
  requisition_number?: string;
  vendor: string;
  vendor_contact: string;
  total_amount: number;
  currency: string;
  status: 'draft' | 'sent' | 'acknowledged' | 'delivered' | 'invoiced' | 'completed' | 'cancelled';
  order_date: string;
  expected_delivery?: string;
  actual_delivery?: string;
  items: PurchaseOrderItem[];
}

export interface PurchaseOrderItem {
  id: number;
  item_name: string;
  description: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  part_number?: string;
  delivery_status: 'pending' | 'partial' | 'delivered';
  delivered_quantity: number;
}