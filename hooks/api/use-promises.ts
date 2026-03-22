import { useQuery } from '@tanstack/react-query';

import { fetchPromises, fetchPromiseStats } from '@/services/api';
import { MOCK_PROMISES, MOCK_PROMISE_STATS } from '@/utils/mock-data';
import type { PromiseItem, PromiseStats } from '@/types/models';
import { queryKeys } from './query-keys';

/**
 * Fetch promise list, optionally filtered by LGU.
 * Falls back to mock data on error.
 */
export function usePromises(lguId?: number) {
  return useQuery<PromiseItem[]>({
    queryKey: queryKeys.promises.list(lguId),
    queryFn: async () => {
      try {
        return await fetchPromises(lguId);
      } catch {
        console.warn('API unavailable for promises, using mock data');
        return MOCK_PROMISES;
      }
    },
    placeholderData: (previousData) => previousData ?? MOCK_PROMISES,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch promise stats, optionally filtered by LGU.
 * Falls back to mock data on error.
 */
export function usePromiseStats(lguId?: number) {
  return useQuery<PromiseStats>({
    queryKey: queryKeys.promises.stats(lguId),
    queryFn: async () => {
      try {
        return await fetchPromiseStats(lguId);
      } catch {
        console.warn('API unavailable for promise stats, using mock data');
        return lguId
          ? { ...MOCK_PROMISE_STATS, lgu_id: lguId }
          : MOCK_PROMISE_STATS;
      }
    },
    placeholderData: (previousData) =>
      previousData ?? (lguId
        ? { ...MOCK_PROMISE_STATS, lgu_id: lguId }
        : MOCK_PROMISE_STATS),
    staleTime: 5 * 60 * 1000,
  });
}
