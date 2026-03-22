import apiClient from './api-client';
import { ENDPOINTS } from '@/constants/api';
import type { PromiseItem, PromiseStats } from '@/types/models';
import { MOCK_PROMISE_STATS, MOCK_PROMISES } from '@/utils/mock-data';

export async function getPromiseStats(lguId: number): Promise<PromiseStats> {
  try {
    const response = await apiClient.get<PromiseStats>(ENDPOINTS.PROMISES_STATS, {
      params: { lgu_id: lguId },
    });
    return response.data;
  } catch {
    console.warn('API unavailable for promise stats, using mock data');
    return { ...MOCK_PROMISE_STATS, lgu_id: lguId };
  }
}

export async function listPromises(params?: {
  lgu_id?: number;
  status?: string;
  category?: string;
  limit?: number;
  offset?: number;
}): Promise<PromiseItem[]> {
  try {
    const response = await apiClient.get<PromiseItem[]>(ENDPOINTS.PROMISES, { params });
    return response.data;
  } catch {
    console.warn('API unavailable for promises, using mock data');
    return MOCK_PROMISES;
  }
}

export async function getPromiseDetail(id: number): Promise<PromiseItem | null> {
  try {
    const response = await apiClient.get<PromiseItem>(ENDPOINTS.PROMISE_DETAIL(id));
    return response.data;
  } catch {
    return MOCK_PROMISES.find((p) => p.id === id) ?? null;
  }
}
