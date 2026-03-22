import { useCallback } from 'react';
import { ActivityIndicator, Pressable, RefreshControl, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

import { PromiseListItem } from '@/components/accountability/PromiseListItem';
import { PromiseSummaryCard } from '@/components/accountability/PromiseSummaryCard';
import { SipatColors } from '@/constants/theme';
import { usePromises, usePromiseStats } from '@/hooks/api';
import { useLanguage } from '@/hooks/use-language';

export default function AccountabilityScreen() {
  const { t } = useLanguage();

  // Fetch promises and stats from the API (falls back to mock data)
  const {
    data: promises = [],
    isLoading: promisesLoading,
    isError: promisesError,
    refetch: refetchPromises,
    isRefetching: promisesRefetching,
  } = usePromises();

  const {
    data: stats,
    isLoading: statsLoading,
    refetch: refetchStats,
    isRefetching: statsRefetching,
  } = usePromiseStats();

  const isLoading = promisesLoading && promises.length === 0;
  const isError = promisesError && promises.length === 0;
  const isRefreshing = promisesRefetching || statsRefetching;

  const onRefresh = useCallback(() => {
    refetchPromises();
    refetchStats();
  }, [refetchPromises, refetchStats]);

  const summaryCards = stats
    ? [
        { label: t.dashboard.promisesKept, count: stats.counts.kept, percentage: stats.percentages.kept, color: SipatColors.kept },
        { label: t.dashboard.promisesBroken, count: stats.counts.broken, percentage: stats.percentages.broken, color: SipatColors.broken },
        { label: t.dashboard.promisesInProgress, count: stats.counts.in_progress, percentage: stats.percentages.in_progress, color: SipatColors.inProgress },
        { label: t.dashboard.promisesPending, count: stats.counts.pending, percentage: stats.percentages.pending, color: SipatColors.pending },
      ]
    : [];

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.centered}>
          <ActivityIndicator size="large" color={SipatColors.gold} />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.centered}>
          <MaterialIcons name="error-outline" size={56} color={SipatColors.error} />
          <Text style={styles.errorText}>Failed to load accountability data. Please try again.</Text>
          <Pressable style={styles.retryButton} onPress={onRefresh}>
            <Text style={styles.retryText}>Retry</Text>
          </Pressable>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={isRefreshing}
            onRefresh={onRefresh}
            colors={[SipatColors.gold]}
            tintColor={SipatColors.gold}
          />
        }
      >
        <Text style={styles.pageTitle}>{t.accountability.title}</Text>

        {/* Promise Summary Cards */}
        <Text style={styles.sectionTitle}>{t.accountability.promiseSummary}</Text>
        {statsLoading && !stats ? (
          <View style={styles.statsLoadingRow}>
            <ActivityIndicator size="small" color={SipatColors.gold} />
          </View>
        ) : (
          <View style={styles.summaryGrid}>
            {summaryCards.map((card) => (
              <View key={card.label} style={styles.summaryCardWrapper}>
                <PromiseSummaryCard {...card} />
              </View>
            ))}
          </View>
        )}

        {/* Recent Promises */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>{t.accountability.recentPromises}</Text>
          <Text style={styles.viewAll}>{t.accountability.viewAll}</Text>
        </View>
        <View style={styles.promiseList}>
          {promises.map((promise) => (
            <PromiseListItem key={promise.id} promise={promise} />
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: SipatColors.textPrimary,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: SipatColors.sectionTitle,
    marginBottom: 12,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 24,
    marginBottom: 12,
  },
  viewAll: {
    fontSize: 14,
    color: SipatColors.accent,
    fontWeight: '600',
  },
  summaryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  summaryCardWrapper: {
    width: '47%',
  },
  promiseList: {
    gap: 12,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  loadingText: {
    fontSize: 14,
    color: SipatColors.textSecondary,
    marginTop: 12,
  },
  errorText: {
    fontSize: 15,
    color: SipatColors.textSecondary,
    textAlign: 'center',
    marginTop: 12,
    lineHeight: 22,
  },
  retryButton: {
    marginTop: 20,
    paddingHorizontal: 24,
    paddingVertical: 10,
    borderRadius: 8,
    backgroundColor: SipatColors.gold,
  },
  retryText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  statsLoadingRow: {
    paddingVertical: 20,
    alignItems: 'center',
  },
});
