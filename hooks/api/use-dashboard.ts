import { useQuery } from '@tanstack/react-query';

import { fetchDashboard } from '@/services/api';
import { MOCK_DASHBOARD } from '@/utils/mock-data';
import type { DashboardData } from '@/types/models';
import { queryKeys } from './query-keys';

/**
 * Fetch dashboard data, optionally scoped to an LGU.
 * Falls back to mock data on error.
 */
export function useDashboard(lguId?: number) {
  return useQuery<DashboardData>({
    queryKey: queryKeys.dashboard.detail(lguId),
    queryFn: async () => {
      try {
        return await fetchDashboard(lguId);
      } catch {
        console.warn('API unavailable for dashboard, using mock data');
        return MOCK_DASHBOARD;
      }
    },
    placeholderData: (previousData) => previousData ?? MOCK_DASHBOARD,
    staleTime: 5 * 60 * 1000,
  });
}
