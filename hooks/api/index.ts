// Barrel file — re-export all React Query hooks from a single entry point.

export { queryKeys } from './query-keys';

export { useLGUs, useLGUDetail, useLGUMapMarkers } from './use-lgus';
export { usePromises, usePromiseStats } from './use-promises';
export { useProjects, useProjectDetail } from './use-projects';
export { useReports, useCreateReport, useUpvoteReport } from './use-reports';
export { useDashboard } from './use-dashboard';
