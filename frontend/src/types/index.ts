// ─── Auth ────────────────────────────────────────────────────────────────────

export type UserRole = 'ADMIN' | 'OWNER' | 'RENTER';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// ─── Owner ───────────────────────────────────────────────────────────────────

export interface Owner {
  id: string;
  user_id: string;
  full_name: string;
  cpf: string;
  phone: string;
  address: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

// ─── Vehicle ─────────────────────────────────────────────────────────────────

export type VehicleStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'SUSPENDED';

export interface Vehicle {
  id: string;
  owner_id: string;
  brand: string;
  model: string;
  year: number;
  license_plate: string;
  color: string;
  renavam: string;
  chassis: string;
  status: VehicleStatus;
  daily_rate: number;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface VehicleDocument {
  id: string;
  vehicle_id: string;
  document_type: string;
  file_url: string;
  is_approved: boolean;
  created_at: string;
}

// ─── Renter ──────────────────────────────────────────────────────────────────

export interface Renter {
  id: string;
  user_id: string;
  full_name: string;
  cpf: string;
  cnh: string;
  cnh_category: string;
  cnh_expiry: string;
  phone: string;
  address: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

// ─── Rental ──────────────────────────────────────────────────────────────────

export type RentalStatus = 'PENDING' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface Rental {
  id: string;
  vehicle_id: string;
  renter_id: string;
  start_date: string;
  end_date: string;
  daily_rate: number;
  total_amount: number;
  status: RentalStatus;
  notes: string;
  created_at: string;
  updated_at: string;
}

// ─── Finance ─────────────────────────────────────────────────────────────────

export type CostCategory =
  | 'MAINTENANCE'
  | 'INSURANCE'
  | 'IPVA'
  | 'LICENSING'
  | 'FUEL'
  | 'CLEANING'
  | 'FINE'
  | 'OTHER';

export interface VehicleCost {
  id: string;
  vehicle_id: string;
  category: CostCategory;
  description: string;
  amount: number;
  cost_date: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface FinancialSummary {
  vehicle_id: string;
  total_revenue: number;
  total_costs: number;
  net_result: number;
  period_start: string;
  period_end: string;
}
