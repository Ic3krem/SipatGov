import { StyleSheet, Text, View } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

import { SipatColors, SipatSpacing, SipatRadius } from '@/constants/theme';
import { PROJECT_STATUS_LABELS, getProjectStatusColor } from '@/constants/status';
import { formatPesoCompact, formatDate } from '@/utils/format';
import { useLanguage } from '@/hooks/use-language';
import type { Project } from '@/types/models';

interface ProjectCardProps {
  project: Project;
}

/** Compute a mock progress percentage based on project status and dates. */
function getProgress(project: Project): number {
  if (project.status === 'completed') return 100;
  if (project.status === 'planned' || project.status === 'bidding') return 0;
  if (project.status === 'cancelled') return 0;

  // For ongoing / delayed / awarded / suspended, estimate based on timeline
  if (project.start_date && project.target_end_date) {
    const start = new Date(project.start_date).getTime();
    const end = new Date(project.target_end_date).getTime();
    const now = Date.now();
    const total = end - start;
    if (total <= 0) return 50;
    const elapsed = now - start;
    const pct = Math.round((elapsed / total) * 100);
    // Clamp between 5 and 95 for non-completed projects
    return Math.max(5, Math.min(95, pct));
  }
  return 30; // fallback
}

export function ProjectCard({ project }: ProjectCardProps) {
  const { t } = useLanguage();
  const statusColor = getProjectStatusColor(project.status);
  const statusLabel = PROJECT_STATUS_LABELS[project.status];
  const progress = getProgress(project);

  return (
    <View style={styles.card}>
      {/* Header row: title + status badge */}
      <View style={styles.header}>
        <Text style={styles.title} numberOfLines={2}>{project.title}</Text>
        <View style={[styles.badge, { backgroundColor: statusColor + '1A' }]}>
          <View style={[styles.dot, { backgroundColor: statusColor }]} />
          <Text style={[styles.badgeText, { color: statusColor }]}>{statusLabel}</Text>
        </View>
      </View>

      {/* Description */}
      {project.description ? (
        <Text style={styles.description} numberOfLines={2}>
          {project.description}
        </Text>
      ) : null}

      {/* Progress bar */}
      <View style={styles.progressSection}>
        <View style={styles.progressHeader}>
          <Text style={styles.progressLabel}>{t.projects.progress}</Text>
          <Text style={styles.progressValue}>{progress}%</Text>
        </View>
        <View style={styles.progressTrack}>
          <View style={[styles.progressFill, { width: `${progress}%`, backgroundColor: statusColor }]} />
        </View>
      </View>

      {/* Meta info */}
      <View style={styles.metaContainer}>
        {/* Budget */}
        {project.approved_budget ? (
          <View style={styles.metaRow}>
            <MaterialIcons name="account-balance-wallet" size={14} color={SipatColors.success} />
            <Text style={styles.metaLabel}>{t.projects.budget}:</Text>
            <Text style={styles.budgetValue}>{formatPesoCompact(project.approved_budget)}</Text>
          </View>
        ) : null}

        {/* Contractor */}
        {project.contractor ? (
          <View style={styles.metaRow}>
            <MaterialIcons name="business" size={14} color={SipatColors.textMuted} />
            <Text style={styles.metaLabel}>{t.projects.contractor}:</Text>
            <Text style={styles.metaValue} numberOfLines={1}>{project.contractor}</Text>
          </View>
        ) : null}

        {/* Date range */}
        {(project.start_date || project.target_end_date) ? (
          <View style={styles.metaRow}>
            <MaterialIcons name="date-range" size={14} color={SipatColors.textMuted} />
            <Text style={styles.metaValue}>
              {project.start_date ? formatDate(project.start_date) : 'TBD'}
              {' \u2013 '}
              {project.actual_end_date
                ? formatDate(project.actual_end_date)
                : project.target_end_date
                  ? formatDate(project.target_end_date)
                  : 'TBD'}
            </Text>
          </View>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: SipatColors.cardBg,
    borderRadius: SipatRadius.md,
    padding: SipatSpacing.lg,
    marginBottom: SipatSpacing.lg,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    // Subtle shadow
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: 10,
    marginBottom: 8,
  },
  title: {
    flex: 1,
    fontSize: 15,
    fontWeight: '700',
    color: SipatColors.textPrimary,
    lineHeight: 20,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    gap: 5,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  badgeText: {
    fontSize: 11,
    fontWeight: '600',
  },
  description: {
    fontSize: 13,
    color: SipatColors.textSecondary,
    lineHeight: 18,
    marginBottom: 12,
  },
  progressSection: {
    marginBottom: 12,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  progressLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: SipatColors.textSecondary,
  },
  progressValue: {
    fontSize: 12,
    fontWeight: '700',
    color: SipatColors.textPrimary,
  },
  progressTrack: {
    height: 6,
    backgroundColor: SipatColors.dashboardBg,
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  metaContainer: {
    gap: 6,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  metaLabel: {
    fontSize: 12,
    color: SipatColors.textMuted,
    fontWeight: '500',
  },
  metaValue: {
    fontSize: 12,
    color: SipatColors.textSecondary,
    fontWeight: '500',
    flex: 1,
  },
  budgetValue: {
    fontSize: 13,
    color: SipatColors.success,
    fontWeight: '700',
    flex: 1,
  },
});
