import { useQuery } from '@tanstack/react-query';

import { fetchLGUs, fetchLGUDetail, fetchLGUMapMarkers } from '@/services/api';
import { MOCK_MAP_MARKERS } from '@/utils/mock-data';
import type { LGU, LGUMapMarker } from '@/types/models';
import { queryKeys } from './query-keys';

/**
 * Fetch a list of LGUs, optionally filtered by region.
 */
export function useLGUs(regionId?: number) {
  return useQuery<LGU[]>({
    queryKey: queryKeys.lgus.list(regionId),
    queryFn: () => fetchLGUs(regionId),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch a single LGU by ID.
 * Disabled until a valid id is provided.
 */
export function useLGUDetail(id: number | undefined) {
  return useQuery<LGU>({
    queryKey: queryKeys.lgus.detail(id!),
    queryFn: () => fetchLGUDetail(id!),
    enabled: id !== undefined,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch LGU map markers. Falls back to mock data on error.
 */
export function useLGUMapMarkers() {
  return useQuery<LGUMapMarker[]>({
    queryKey: queryKeys.lgus.mapMarkers(),
    queryFn: async () => {
      try {
        return await fetchLGUMapMarkers();
      } catch {
        console.warn('API unavailable for map markers, using mock data');
        return MOCK_MAP_MARKERS;
      }
    },
    placeholderData: (previousData) => previousData ?? MOCK_MAP_MARKERS,
    staleTime: 5 * 60 * 1000,
  });
}
