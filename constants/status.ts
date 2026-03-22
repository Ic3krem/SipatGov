import { SipatColors } from './theme';
import type { PromiseStatus, ProjectStatus, ReportStatus, ReportType } from '@/types/models';

export const PROMISE_STATUS_LABELS: Record<PromiseStatus, string> = {
  kept: 'Natupad',
  broken: 'Hindi Natupad',
  in_progress: 'Isinasagawa',
  pending: 'Nakabinbin',
  partially_kept: 'Bahagyang Natupad',
  unverifiable: 'Hindi Ma-verify',
};

export const PROMISE_STATUS_COLORS: Record<PromiseStatus, string> = {
  kept: SipatColors.kept,
  broken: SipatColors.broken,
  in_progress: SipatColors.inProgress,
  pending: SipatColors.pending,
  partially_kept: SipatColors.partiallyKept,
  unverifiable: SipatColors.unverifiable,
};

export const PROJECT_STATUS_LABELS: Record<ProjectStatus, string> = {
  planned: 'Pinaplano',
  bidding: 'Nagbi-bidding',
  awarded: 'Nai-award',
  ongoing: 'Kasalukuyan',
  completed: 'Tapos Na',
  delayed: 'Naantala',
  cancelled: 'Kinansela',
  suspended: 'Suspendido',
};

export const PROJECT_STATUS_COLORS: Record<ProjectStatus, string> = {
  planned: SipatColors.planned,
  bidding: SipatColors.bidding,
  awarded: SipatColors.awarded,
  ongoing: SipatColors.ongoing,
  completed: SipatColors.completed,
  delayed: SipatColors.delayed,
  cancelled: SipatColors.cancelled,
  suspended: SipatColors.suspended,
};

export const REPORT_TYPE_LABELS: Record<ReportType, string> = {
  concern: 'Alalahanin',
  feedback: 'Feedback',
  corruption_tip: 'Tip sa Korupsyon',
  progress_update: 'Update sa Progreso',
  delay_report: 'Report ng Pagkaantala',
};

export const REPORT_STATUS_LABELS: Record<ReportStatus, string> = {
  submitted: 'Naisumite',
  under_review: 'Sinusuri',
  verified: 'Na-verify',
  resolved: 'Nalutas',
  dismissed: 'Tinanggihan',
};

export const REPORT_TYPE_COLORS: Record<ReportType, string> = {
  concern: '#E67E22',        // orange
  feedback: SipatColors.blueLight, // blue
  corruption_tip: SipatColors.red,  // red
  progress_update: SipatColors.kept, // green
  delay_report: '#F5A623',   // amber
};

export const REPORT_TYPE_ICONS: Record<ReportType, string> = {
  concern: 'warning',
  feedback: 'chat-bubble',
  corruption_tip: 'gavel',
  progress_update: 'trending-up',
  delay_report: 'schedule',
};

export const REPORT_STATUS_COLORS: Record<ReportStatus, string> = {
  submitted: SipatColors.pending,
  under_review: SipatColors.inProgress,
  verified: SipatColors.kept,
  resolved: SipatColors.completed,
  dismissed: SipatColors.unverifiable,
};

export function getPromiseStatusColor(status: PromiseStatus): string {
  return PROMISE_STATUS_COLORS[status] ?? SipatColors.textMuted;
}

export function getProjectStatusColor(status: ProjectStatus): string {
  return PROJECT_STATUS_COLORS[status] ?? SipatColors.textMuted;
}

export function getReportTypeColor(type: ReportType): string {
  return REPORT_TYPE_COLORS[type] ?? SipatColors.textMuted;
}

export function getReportStatusColor(status: ReportStatus): string {
  return REPORT_STATUS_COLORS[status] ?? SipatColors.textMuted;
}
