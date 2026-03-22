// Domain model interfaces matching backend API responses

export interface Region {
  id: number;
  psgc_code: string;
  name: string;
  region_code: string;
}

export interface Province {
  id: number;
  psgc_code: string;
  name: string;
  region_id: number;
}

export interface LGU {
  id: number;
  psgc_code: string;
  name: string;
  lgu_type: 'municipality' | 'city' | 'province' | 'barangay';
  latitude: number | null;
  longitude: number | null;
  population: number | null;
  income_class: string | null;
  transparency_score: number;
}

export interface LGUMapMarker {
  id: number;
  name: string;
  lat: number;
  lng: number;
  score: number;
  type: string;
}

export interface Official {
  id: number;
  lgu_id: number;
  full_name: string;
  position: string;
  party: string | null;
  term_start: string | null;
  term_end: string | null;
  is_current: boolean;
}

export interface BudgetAllocation {
  id: number;
  lgu_id: number;
  fiscal_year: number;
  category: string;
  subcategory: string | null;
  allocated_amount: number;
  released_amount: number;
  utilized_amount: number;
}

export interface BudgetSummary {
  category: string;
  allocated: number;
  released: number;
  utilized: number;
}

export type ProjectStatus =
  | 'planned' | 'bidding' | 'awarded' | 'ongoing'
  | 'completed' | 'delayed' | 'cancelled' | 'suspended';

export interface Project {
  id: number;
  lgu_id: number;
  title: string;
  description: string | null;
  category: string | null;
  status: ProjectStatus;
  contractor: string | null;
  approved_budget: number | null;
  contract_amount: number | null;
  actual_cost: number | null;
  start_date: string | null;
  target_end_date: string | null;
  actual_end_date: string | null;
  latitude: number | null;
  longitude: number | null;
  address: string | null;
  philgeps_ref: string | null;
  fiscal_year: number | null;
}

export type PromiseStatus =
  | 'kept' | 'broken' | 'in_progress' | 'pending'
  | 'partially_kept' | 'unverifiable';

export interface PromiseItem {
  id: number;
  official_id: number | null;
  lgu_id: number;
  title: string;
  description: string | null;
  category: string | null;
  status: PromiseStatus;
  evidence_summary: string | null;
  date_promised: string | null;
  deadline: string | null;
  verified_at: string | null;
  verified_by: string | null;
  confidence_score: number | null;
}

export interface PromiseStats {
  lgu_id: number;
  total: number;
  counts: Record<PromiseStatus, number>;
  percentages: Record<PromiseStatus, number>;
}

export type ReportType =
  | 'concern' | 'feedback' | 'corruption_tip'
  | 'progress_update' | 'delay_report';

export type ReportStatus =
  | 'submitted' | 'under_review' | 'verified' | 'resolved' | 'dismissed';

export interface CommunityReport {
  id: number;
  user_id: number | null;
  lgu_id: number;
  project_id: number | null;
  title: string;
  description: string;
  report_type: ReportType;
  status: ReportStatus;
  latitude: number | null;
  longitude: number | null;
  address: string | null;
  upvote_count: number;
  is_anonymous: boolean;
  created_at: string;
}

export interface User {
  id: number;
  email: string | null;
  phone: string | null;
  display_name: string | null;
  avatar_url: string | null;
  home_lgu_id: number | null;
  home_region_id: number | null;
  role: 'citizen' | 'moderator' | 'admin';
  is_verified: boolean;
  onboarding_completed: boolean;
}

export interface DashboardData {
  lgu: { id: number; name: string; transparency_score: number };
  budget: { total_allocated: number; total_utilized: number };
  total_projects: number;
  promises: Record<PromiseStatus, number>;
  total_reports: number;
}

export interface SearchResult {
  type: 'lgu' | 'project' | 'promise';
  id: number;
  title: string;
}
