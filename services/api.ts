// Unified API service layer organized by domain.
// Each function calls the typed helpers from api-client and returns unwrapped data.

import { AxiosError } from 'axios';

import { ENDPOINTS } from '@/constants/api';
import type {
  LGU,
  LGUMapMarker,
  PromiseItem,
  PromiseStats,
  Project,
  BudgetSummary,
  CommunityReport,
  DashboardData,
} from '@/types/models';
import type {
  AuthResponse,
  CreateReportInput,
  RegisterInput,
  ProjectsFilterParams,
  PromisesFilterParams,
  ReportsFilterParams,
} from '@/types/api';
import { get, post } from './api-client';

// ──────────────────────────────────────────────
//  Error class
// ──────────────────────────────────────────────

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number = 0,
    public code?: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) return error;
  if (error instanceof AxiosError) {
    return new ApiError(
      error.response?.data?.detail ?? error.message,
      error.response?.status ?? 0,
      error.code,
    );
  }
  if (error instanceof Error) {
    return new ApiError(error.message);
  }
  return new ApiError('An unknown error occurred');
}

// ──────────────────────────────────────────────
//  LGUs
// ──────────────────────────────────────────────

export async function fetchLGUs(regionId?: number): Promise<LGU[]> {
  try {
    return await get<LGU[]>(ENDPOINTS.LGUS, {
      params: regionId ? { region_id: regionId } : undefined,
    });
  } catch (error) {
    throw toApiError(error);
  }
}

export async function fetchLGUDetail(id: number): Promise<LGU> {
  try {
    return await get<LGU>(ENDPOINTS.LGU_DETAIL(id));
  } catch (error) {
    throw toApiError(error);
  }
}

export async function fetchLGUMapMarkers(): Promise<LGUMapMarker[]> {
  try {
    return await get<LGUMapMarker[]>(ENDPOINTS.LGUS_MAP);
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Promises
// ──────────────────────────────────────────────

export async function fetchPromises(lguId?: number, params?: Omit<PromisesFilterParams, 'lgu_id'>): Promise<PromiseItem[]> {
  try {
    return await get<PromiseItem[]>(ENDPOINTS.PROMISES, {
      params: { ...params, lgu_id: lguId },
    });
  } catch (error) {
    throw toApiError(error);
  }
}

export async function fetchPromiseStats(lguId?: number): Promise<PromiseStats> {
  try {
    return await get<PromiseStats>(ENDPOINTS.PROMISES_STATS, {
      params: lguId ? { lgu_id: lguId } : undefined,
    });
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Projects
// ──────────────────────────────────────────────

export async function fetchProjects(params?: ProjectsFilterParams): Promise<Project[]> {
  try {
    return await get<Project[]>(ENDPOINTS.PROJECTS, { params });
  } catch (error) {
    throw toApiError(error);
  }
}

export async function fetchProjectDetail(id: number): Promise<Project> {
  try {
    return await get<Project>(ENDPOINTS.PROJECT_DETAIL(id));
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Budget
// ──────────────────────────────────────────────

export async function fetchBudgetSummary(lguId: number, year?: number): Promise<BudgetSummary[]> {
  try {
    return await get<BudgetSummary[]>(ENDPOINTS.BUDGETS_SUMMARY, {
      params: { lgu_id: lguId, ...(year ? { fiscal_year: year } : {}) },
    });
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Reports
// ──────────────────────────────────────────────

export async function fetchReports(params?: ReportsFilterParams): Promise<CommunityReport[]> {
  try {
    return await get<CommunityReport[]>(ENDPOINTS.REPORTS, { params });
  } catch (error) {
    throw toApiError(error);
  }
}

export async function createReport(data: CreateReportInput): Promise<CommunityReport> {
  try {
    return await post<CommunityReport>(ENDPOINTS.REPORTS, data);
  } catch (error) {
    throw toApiError(error);
  }
}

export async function upvoteReport(reportId: number): Promise<void> {
  try {
    return await post<void>(ENDPOINTS.REPORT_UPVOTE(reportId));
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Dashboard
// ──────────────────────────────────────────────

export async function fetchDashboard(lguId?: number): Promise<DashboardData> {
  try {
    return await get<DashboardData>(ENDPOINTS.DASHBOARD, {
      params: lguId ? { lgu_id: lguId } : undefined,
    });
  } catch (error) {
    throw toApiError(error);
  }
}

// ──────────────────────────────────────────────
//  Auth
// ──────────────────────────────────────────────

export async function login(email: string, password: string): Promise<AuthResponse> {
  try {
    return await post<AuthResponse>(ENDPOINTS.AUTH_LOGIN, { email, password });
  } catch (error) {
    throw toApiError(error);
  }
}

export async function register(data: RegisterInput): Promise<AuthResponse> {
  try {
    return await post<AuthResponse>(ENDPOINTS.AUTH_REGISTER, data);
  } catch (error) {
    throw toApiError(error);
  }
}
