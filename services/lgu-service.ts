import apiClient from './api-client';
import { ENDPOINTS } from '@/constants/api';
import type { LGUMapMarker, LGU } from '@/types/models';
import { MOCK_MAP_MARKERS } from '@/utils/mock-data';

export async function getLGUsForMap(): Promise<LGUMapMarker[]> {
  try {
    const response = await apiClient.get<LGUMapMarker[]>(ENDPOINTS.LGUS_MAP);
    return response.data;
  } catch {
    console.warn('API unavailable for map markers, using mock data');
    return MOCK_MAP_MARKERS;
  }
}

export async function getLGUDetail(id: number): Promise<LGU | null> {
  try {
    const response = await apiClient.get<LGU>(ENDPOINTS.LGU_DETAIL(id));
    return response.data;
  } catch {
    // Return mock match if available
    const mock = MOCK_MAP_MARKERS.find((m) => m.id === id);
    if (mock) {
      return {
        id: mock.id,
        psgc_code: '',
        name: mock.name,
        lgu_type: mock.type as LGU['lgu_type'],
        latitude: mock.lat,
        longitude: mock.lng,
        population: null,
        income_class: null,
        transparency_score: mock.score,
      };
    }
    return null;
  }
}

export async function listLGUs(params?: {
  region_id?: number;
  search?: string;
  limit?: number;
}): Promise<LGU[]> {
  try {
    const response = await apiClient.get<LGU[]>(ENDPOINTS.LGUS, { params });
    return response.data;
  } catch {
    return [];
  }
}
