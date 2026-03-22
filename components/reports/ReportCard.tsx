import { Pressable, StyleSheet, Text, View } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

import { ReportTypeChip } from './ReportTypeChip';
import { SipatColors } from '@/constants/theme';
import { REPORT_STATUS_COLORS, REPORT_STATUS_LABELS } from '@/constants/status';
import { formatRelativeDate } from '@/utils/format';
import { useLanguage } from '@/hooks/use-language';
import type { CommunityReport } from '@/types/models';

interface ReportCardProps {
  report: CommunityReport;
  onUpvote?: () => void;
}

export function ReportCard({ report, onUpvote }: ReportCardProps) {
  const { t } = useLanguage();
  const statusColor = REPORT_STATUS_COLORS[report.status] ?? SipatColors.textMuted;
  const statusLabel = REPORT_STATUS_LABELS[report.status] ?? report.status;

  return (
    <View style={styles.container}>
      {/* Header: Type badge + Status badge */}
      <View style={styles.header}>
        <ReportTypeChip type={report.report_type} />
        <View style={[styles.statusBadge, { backgroundColor: statusColor + '1A' }]}>
          <View style={[styles.statusDot, { backgroundColor: statusColor }]} />
          <Text style={[styles.statusText, { color: statusColor }]}>
            {statusLabel}
          </Text>
        </View>
      </View>

      {/* Title */}
      <Text style={styles.title} numberOfLines={2}>
        {report.title}
      </Text>

      {/* Description */}
      <Text style={styles.description} numberOfLines={3}>
        {report.description}
      </Text>

      {/* Footer: meta info + upvote button */}
      <View style={styles.footer}>
        <View style={styles.metaRow}>
          {/* Time ago */}
          <View style={styles.metaItem}>
            <MaterialIcons name="access-time" size={12} color={SipatColors.textMuted} />
            <Text style={styles.metaText}>
              {formatRelativeDate(report.created_at)}
            </Text>
          </View>

          {/* Anonymous indicator */}
          {report.is_anonymous && (
            <View style={styles.metaItem}>
              <MaterialIcons name="visibility-off" size={12} color={SipatColors.textMuted} />
              <Text style={styles.metaText}>{t.reports.anonymousUser}</Text>
            </View>
          )}
        </View>

        {/* Upvote button */}
        <Pressable
          style={styles.upvoteButton}
          onPress={onUpvote}
          hitSlop={8}
        >
          <MaterialIcons name="thumb-up" size={14} color={SipatColors.textSecondary} />
          <Text style={styles.upvoteCount}>{report.upvote_count}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    gap: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    gap: 5,
  },
  statusDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  statusText: {
    fontSize: 11,
    fontWeight: '600',
  },
  title: {
    fontSize: 15,
    fontWeight: '600',
    color: SipatColors.textPrimary,
    lineHeight: 20,
  },
  description: {
    fontSize: 13,
    color: SipatColors.textSecondary,
    lineHeight: 19,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  metaText: {
    fontSize: 11,
    color: SipatColors.textMuted,
  },
  upvoteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: SipatColors.dashboardBg,
  },
  upvoteCount: {
    fontSize: 12,
    fontWeight: '600',
    color: SipatColors.textSecondary,
  },
});
