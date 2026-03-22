import apiClient from './api-client';
import { ENDPOINTS } from '@/constants/api';
import type { DashboardData } from '@/types/models';
import { MOCK_DASHBOARD } from '@/utils/mock-data';

export async function getDashboard(lguId?: number): Promise<DashboardData> {
  try {
    const response = await apiClient.get<DashboardData>(ENDPOINTS.DASHBOARD, {
      params: lguId ? { lgu_id: lguId } : undefined,
    });
    return response.data;
  } catch {
    console.warn('API unavailable for dashboard, using mock data');
    return MOCK_DASHBOARD;
  }
}

interface NationalDashboard {
  total_lgus: number;
  total_projects: number;
  total_promises: number;
  total_reports: number;
}

export async function getNationalDashboard(): Promise<NationalDashboard> {
  try {
    const response = await apiClient.get<NationalDashboard>(ENDPOINTS.DASHBOARD_NATIONAL);
    return response.data;
  } catch {
    return {
      total_lgus: 25,
      total_projects: 142,
      total_promises: 47,
      total_reports: 89,
    };
  }
}
