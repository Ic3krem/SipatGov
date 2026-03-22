// Query key factories for consistent cache key management across hooks.

export const queryKeys = {
  lgus: {
    all: ['lgus'] as const,
    list: (regionId?: number) => ['lgus', 'list', { regionId }] as const,
    detail: (id: number) => ['lgus', 'detail', id] as const,
    mapMarkers: () => ['lgus', 'map-markers'] as const,
  },
  promises: {
    all: ['promises'] as const,
    list: (lguId?: number) => ['promises', 'list', { lguId }] as const,
    stats: (lguId?: number) => ['promises', 'stats', { lguId }] as const,
  },
  projects: {
    all: ['projects'] as const,
    list: (params?: { lguId?: number; status?: string }) =>
      ['projects', 'list', params ?? {}] as const,
    detail: (id: number) => ['projects', 'detail', id] as const,
  },
  budget: {
    all: ['budget'] as const,
    summary: (lguId: number, year?: number) =>
      ['budget', 'summary', { lguId, year }] as const,
  },
  reports: {
    all: ['reports'] as const,
    list: (params?: { type?: string }) =>
      ['reports', 'list', params ?? {}] as const,
  },
  dashboard: {
    all: ['dashboard'] as const,
    detail: (lguId?: number) => ['dashboard', { lguId }] as const,
  },
} as const;
