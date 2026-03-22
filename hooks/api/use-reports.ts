import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { fetchReports, createReport, upvoteReport } from '@/services/api';
import type { CommunityReport } from '@/types/models';
import type { CreateReportInput, ReportsFilterParams } from '@/types/api';
import { queryKeys } from './query-keys';

interface ReportsMutationContext {
  previous: CommunityReport[] | undefined;
}

/**
 * Fetch community reports with optional filters.
 */
export function useReports(params?: ReportsFilterParams) {
  return useQuery<CommunityReport[]>({
    queryKey: queryKeys.reports.list(
      params ? { type: params.report_type } : undefined,
    ),
    queryFn: () => fetchReports(params),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Create a new community report (mutation).
 * Optimistically prepends the new report to the cached list.
 */
export function useCreateReport() {
  const queryClient = useQueryClient();

  return useMutation<CommunityReport, Error, CreateReportInput, ReportsMutationContext>({
    mutationFn: (data) => createReport(data),

    onMutate: async (newReport) => {
      // Cancel any outgoing refetches so they don't overwrite our optimistic update
      await queryClient.cancelQueries({ queryKey: queryKeys.reports.all });

      // Snapshot the previous value
      const previous = queryClient.getQueryData<CommunityReport[]>(
        queryKeys.reports.list(),
      );

      // Optimistically prepend a placeholder
      if (previous) {
        const optimistic: CommunityReport = {
          id: Date.now(), // temporary ID
          user_id: null,
          lgu_id: newReport.lgu_id ?? 0,
          project_id: newReport.project_id ?? null,
          title: newReport.title,
          description: newReport.description,
          report_type: newReport.report_type as CommunityReport['report_type'],
          status: 'submitted',
          latitude: newReport.latitude ?? null,
          longitude: newReport.longitude ?? null,
          address: newReport.address ?? null,
          upvote_count: 0,
          is_anonymous: newReport.is_anonymous,
          created_at: new Date().toISOString(),
        };
        queryClient.setQueryData<CommunityReport[]>(
          queryKeys.reports.list(),
          [optimistic, ...previous],
        );
      }

      return { previous };
    },

    onError: (_err, _newReport, context) => {
      // Roll back to the previous value on error
      if (context?.previous) {
        queryClient.setQueryData<CommunityReport[]>(
          queryKeys.reports.list(),
          context.previous,
        );
      }
    },

    onSettled: () => {
      // Refetch to sync with server state
      queryClient.invalidateQueries({ queryKey: queryKeys.reports.all });
    },
  });
}

/**
 * Upvote a community report (mutation).
 * Optimistically increments the upvote_count.
 */
export function useUpvoteReport() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, number, ReportsMutationContext>({
    mutationFn: (reportId) => upvoteReport(reportId),

    onMutate: async (reportId) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.reports.all });

      const previous = queryClient.getQueryData<CommunityReport[]>(
        queryKeys.reports.list(),
      );

      if (previous) {
        queryClient.setQueryData<CommunityReport[]>(
          queryKeys.reports.list(),
          previous.map((r) =>
            r.id === reportId
              ? { ...r, upvote_count: r.upvote_count + 1 }
              : r,
          ),
        );
      }

      return { previous };
    },

    onError: (_err, _reportId, context) => {
      if (context?.previous) {
        queryClient.setQueryData<CommunityReport[]>(
          queryKeys.reports.list(),
          context.previous,
        );
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.reports.all });
    },
  });
}
