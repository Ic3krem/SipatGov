// API request/response type definitions

import type { User } from './models';

// ---------- Pagination ----------

export interface PaginatedParams {
  limit?: number;
  offset?: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
}

// ---------- Auth ----------

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  email?: string;
  phone?: string;
  password: string;
}

export interface RegisterInput {
  email: string;
  password: string;
  display_name: string;
  phone?: string;
}

export interface RegisterRequest {
  email?: string;
  phone?: string;
  password: string;
  display_name?: string;
}

export interface OnboardingRequest {
  home_lgu_id: number;
  home_region_id: number;
}

// ---------- Reports ----------

export interface CreateReportInput {
  title: string;
  description: string;
  report_type: string;
  lgu_id?: number;
  project_id?: number;
  is_anonymous: boolean;
  latitude?: number;
  longitude?: number;
  address?: string;
}

export interface CreateReportRequest {
  lgu_id: number;
  project_id?: number;
  title: string;
  description: string;
  report_type: string;
  latitude?: number;
  longitude?: number;
  address?: string;
  is_anonymous?: boolean;
}

// ---------- Filters ----------

export interface ProjectsFilterParams extends PaginatedParams {
  lgu_id?: number;
  status?: string;
  category?: string;
  fiscal_year?: number;
}

export interface PromisesFilterParams extends PaginatedParams {
  lgu_id?: number;
  official_id?: number;
  status?: string;
  category?: string;
}

export interface ReportsFilterParams extends PaginatedParams {
  lgu_id?: number;
  project_id?: number;
  report_type?: string;
  status?: string;
  sort?: 'newest' | 'popular';
}

export interface SearchParams {
  q: string;
  lgu_id?: number;
  limit?: number;
}

// ---------- Geo ----------

export interface GeoJSONFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number]; // [lng, lat]
  };
  properties: {
    id: number;
    title: string;
    status: string;
    category: string | null;
    budget: number | null;
  };
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection';
  features: GeoJSONFeature[];
}
