import { useCallback, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

import { ReportCard } from '@/components/reports/ReportCard';
import { ReportForm } from '@/components/reports/ReportForm';
import { SipatColors, SipatSpacing, SipatRadius, SipatTypography } from '@/constants/theme';
import { useReports, useCreateReport, useUpvoteReport } from '@/hooks/api';
import { useLanguage } from '@/hooks/use-language';
import type { CommunityReport, ReportType } from '@/types/models';

// -- Filter tab definitions --
type FilterKey = 'all' | 'concerns' | 'tips' | 'updates';

const FILTER_TYPE_MAP: Record<FilterKey, ReportType[] | null> = {
  all: null,
  concerns: ['concern', 'feedback'],
  tips: ['corruption_tip'],
  updates: ['progress_update', 'delay_report'],
};

export default function ReportsScreen() {
  const { t } = useLanguage();
  const [activeFilter, setActiveFilter] = useState<FilterKey>('all');
  const [formVisible, setFormVisible] = useState(false);

  // Fetch reports from the API
  const {
    data: reports = [],
    isLoading,
    isError,
    refetch,
    isRefetching,
  } = useReports();

  // Mutations
  const createReportMutation = useCreateReport();
  const upvoteReportMutation = useUpvoteReport();

  // Filter reports based on selected tab
  const filteredReports = useMemo(() => {
    const types = FILTER_TYPE_MAP[activeFilter];
    if (!types) return reports;
    return reports.filter((r) => types.includes(r.report_type));
  }, [reports, activeFilter]);

  const onRefresh = useCallback(() => {
    refetch();
  }, [refetch]);

  // Upvote handler
  const handleUpvote = useCallback(
    (reportId: number) => {
      upvoteReportMutation.mutate(reportId);
    },
    [upvoteReportMutation]
  );

  // Form submit handler
  const handleFormSubmit = useCallback(
    (data: {
      title: string;
      description: string;
      report_type: ReportType;
      is_anonymous: boolean;
    }) => {
      createReportMutation.mutate(
        {
          title: data.title,
          description: data.description,
          report_type: data.report_type,
          is_anonymous: data.is_anonymous,
          lgu_id: 1, // default LGU for now
        },
        {
          onSuccess: () => {
            setFormVisible(false);
          },
        }
      );
    },
    [createReportMutation]
  );

  // Filter tab labels
  const FILTER_TABS: { key: FilterKey; label: string }[] = [
    { key: 'all', label: t.reports.all },
    { key: 'concerns', label: t.reports.concerns },
    { key: 'tips', label: t.reports.tips },
    { key: 'updates', label: t.reports.updates },
  ];

  // Render a single report card
  const renderItem = useCallback(
    ({ item }: { item: CommunityReport }) => (
      <ReportCard
        report={item}
        onUpvote={() => handleUpvote(item.id)}
      />
    ),
    [handleUpvote]
  );

  const keyExtractor = useCallback(
    (item: CommunityReport) => item.id.toString(),
    []
  );

  // Empty state
  const ListEmptyComponent = useMemo(
    () => {
      if (isLoading) {
        return (
          <View style={styles.emptyState}>
            <ActivityIndicator size="large" color={SipatColors.gold} />
            <Text style={styles.emptyTitle}>Loading reports...</Text>
          </View>
        );
      }

      if (isError) {
        return (
          <View style={styles.emptyState}>
            <MaterialIcons name="error-outline" size={56} color={SipatColors.textMuted} />
            <Text style={styles.emptyTitle}>Failed to load reports</Text>
            <Text style={styles.emptyBody}>Pull down to try again.</Text>
          </View>
        );
      }

      return (
        <View style={styles.emptyState}>
          <MaterialIcons name="campaign" size={56} color={SipatColors.textMuted} />
          <Text style={styles.emptyTitle}>{t.reports.noReports}</Text>
          <Text style={styles.emptyBody}>{t.reports.noReportsBody}</Text>
        </View>
      );
    },
    [t, isLoading, isError]
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.pageTitle}>{t.reports.title}</Text>
          <Text style={styles.reportCount}>
            {filteredReports.length} {t.reports.reportCount}
          </Text>
        </View>
      </View>

      {/* Filter Tabs */}
      <View style={styles.filterRow}>
        {FILTER_TABS.map((tab) => {
          const isActive = activeFilter === tab.key;
          return (
            <Pressable
              key={tab.key}
              style={[styles.filterTab, isActive && styles.filterTabActive]}
              onPress={() => setActiveFilter(tab.key)}
            >
              <Text
                style={[
                  styles.filterTabText,
                  isActive && styles.filterTabTextActive,
                ]}
              >
                {tab.label}
              </Text>
            </Pressable>
          );
        })}
      </View>

      {/* Report List */}
      <FlatList
        data={filteredReports}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
        ListEmptyComponent={ListEmptyComponent}
        refreshControl={
          <RefreshControl
            refreshing={isRefetching}
            onRefresh={onRefresh}
            tintColor={SipatColors.gold}
            colors={[SipatColors.gold]}
          />
        }
      />

      {/* FAB — bottom-right */}
      <Pressable
        style={styles.fab}
        onPress={() => setFormVisible(true)}
        hitSlop={4}
      >
        <MaterialIcons name="add" size={26} color="#FFFFFF" />
      </Pressable>

      {/* Report Form Modal */}
      <ReportForm
        visible={formVisible}
        onClose={() => setFormVisible(false)}
        onSubmit={handleFormSubmit}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SipatSpacing.xl,
    paddingTop: SipatSpacing.sm,
    paddingBottom: SipatSpacing.md,
  },
  pageTitle: {
    ...SipatTypography.h2,
    color: SipatColors.textPrimary,
  },
  reportCount: {
    ...SipatTypography.bodySmall,
    color: SipatColors.textMuted,
    marginTop: 2,
  },
  fab: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    width: 56,
    height: 56,
    borderRadius: SipatRadius.pill,
    backgroundColor: SipatColors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 8,
    elevation: 6,
    zIndex: 10,
  },
  filterRow: {
    flexDirection: 'row',
    paddingHorizontal: SipatSpacing.xl,
    gap: SipatSpacing.sm,
    marginBottom: SipatSpacing.sm,
  },
  filterTab: {
    paddingHorizontal: SipatSpacing.lg,
    paddingVertical: SipatSpacing.sm,
    borderRadius: SipatSpacing.xl,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
  },
  filterTabActive: {
    backgroundColor: SipatColors.navy,
    borderColor: SipatColors.navy,
  },
  filterTabText: {
    ...SipatTypography.bodySmall,
    fontWeight: '500',
    color: SipatColors.textSecondary,
  },
  filterTabTextActive: {
    color: '#FFFFFF',
    fontWeight: '600',
  },
  listContent: {
    padding: SipatSpacing.xl,
    paddingTop: SipatSpacing.md,
    paddingBottom: 40,
    flexGrow: 1,
  },
  separator: {
    height: SipatSpacing.md,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 80,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: SipatColors.textPrimary,
    marginTop: SipatSpacing.lg,
  },
  emptyBody: {
    fontSize: 14,
    color: SipatColors.textSecondary,
    textAlign: 'center',
    marginTop: SipatSpacing.sm,
    paddingHorizontal: 40,
  },
});
