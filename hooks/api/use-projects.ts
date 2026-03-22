import { useQuery } from '@tanstack/react-query';

import { fetchProjects, fetchProjectDetail } from '@/services/api';
import type { Project } from '@/types/models';
import type { ProjectsFilterParams } from '@/types/api';
import { queryKeys } from './query-keys';

/**
 * Fetch a list of projects with optional filters.
 */
export function useProjects(params?: ProjectsFilterParams) {
  return useQuery<Project[]>({
    queryKey: queryKeys.projects.list(
      params ? { lguId: params.lgu_id, status: params.status } : undefined,
    ),
    queryFn: () => fetchProjects(params),
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
