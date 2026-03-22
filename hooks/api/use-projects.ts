import { useQuery } from '@tanstack/react-query';

import { fetchProjects, fetchProjectDetail } from '@/services/api';
import { MOCK_PROJECTS } from '@/utils/mock-data';
import type { Project } from '@/types/models';
import type { ProjectsFilterParams } from '@/types/api';
import { queryKeys } from './query-keys';

/**
 * Fetch a list of projects with optional filters.
 * Falls back to mock data on error.
 */
export function useProjects(params?: ProjectsFilterParams) {
  return useQuery<Project[]>({
    queryKey: queryKeys.projects.list(
      params ? { lguId: params.lgu_id, status: params.status } : undefined,
    ),
    queryFn: async () => {
      try {
        return await fetchProjects(params);
      } catch {
        console.warn('API unavailable for projects, using mock data');
        const projects = MOCK_PROJECTS;
        if (params?.status) {
          return projects.filter((p) => p.status === params.status);
        }
        return projects;
      }
    },
    placeholderData: (previousData) => previousData ?? MOCK_PROJECTS,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Fetch a single project by ID.
 * Disabled until a valid id is provided.
 */
export function useProjectDetail(id: number | undefined) {
  return useQuery<Project>({
    queryKey: queryKeys.projects.detail(id!),
    queryFn: () => fetchProjectDetail(id!),
    enabled: id !== undefined,
    staleTime: 5 * 60 * 1000,
  });
}
