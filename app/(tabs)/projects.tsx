import { useCallback, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  RefreshControl,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

import { ProjectCard } from '@/components/projects/ProjectCard';
import { ProjectFilters, type ProjectFilterValue } from '@/components/projects/ProjectFilters';
import { SipatColors } from '@/constants/theme';
import { useProjects } from '@/hooks/api';
import { useLanguage } from '@/hooks/use-language';
import type { Project } from '@/types/models';
import type { ProjectsFilterParams } from '@/types/api';

export default function ProjectsScreen() {
  const { t } = useLanguage();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<ProjectFilterValue>(null);

  // Build filter params for the API hook
  const filterParams: ProjectsFilterParams | undefined = useMemo(() => {
    if (activeFilter === null) return undefined;
    return { status: activeFilter };
  }, [activeFilter]);

  // Fetch projects from the API
  const {
    data: projects = [],
    isLoading,
    isError,
    refetch,
    isRefetching,
  } = useProjects(filterParams);

  // Apply client-side search filter on top of API-filtered data
  const filteredProjects = useMemo(() => {
    if (!searchQuery.trim()) return projects;

    const query = searchQuery.toLowerCase().trim();
    return projects.filter(
      (p) =>
        p.title.toLowerCase().includes(query) ||
        (p.description && p.description.toLowerCase().includes(query)) ||
        (p.contractor && p.contractor.toLowerCase().includes(query)) ||
        (p.category && p.category.toLowerCase().includes(query))
    );
  }, [projects, searchQuery]);

  const onRefresh = useCallback(() => {
    refetch();
  }, [refetch]);

  const renderItem = useCallback(
    ({ item }: { item: Project }) => <ProjectCard project={item} />,
    []
  );

  const keyExtractor = useCallback((item: Project) => item.id.toString(), []);

  const ListHeaderComponent = useMemo(
    () => (
      <View style={styles.listHeader}>
        <Text style={styles.projectCount}>
          {filteredProjects.length} {t.projects.projectCount}
        </Text>
      </View>
    ),
    [filteredProjects.length, t.projects.projectCount]
  );

  const ListEmptyComponent = useMemo(
    () => {
      // Still loading initial data
      if (isLoading) {
        return (
          <View style={styles.emptyState}>
            <ActivityIndicator size="large" color={SipatColors.gold} />
            <Text style={styles.emptyTitle}>Loading projects...</Text>
          </View>
        );
      }

      // Error state with no data
      if (isError) {
        return (
          <View style={styles.emptyState}>
            <MaterialIcons name="error-outline" size={56} color={SipatColors.textMuted} />
            <Text style={styles.emptyTitle}>Failed to load projects</Text>
            <Text style={styles.emptySubtitle}>Pull down to try again.</Text>
          </View>
        );
      }

      // No active search/filter: show "no data" state
      if (!searchQuery.trim() && activeFilter === null) {
        return (
          <View style={styles.emptyState}>
            <MaterialIcons name="folder-open" size={56} color={SipatColors.textMuted} />
            <Text style={styles.emptyTitle}>{t.projects.noResults}</Text>
            <Text style={styles.emptySubtitle}>No project data available. Pull down to refresh.</Text>
          </View>
        );
      }

      // Active search/filter with no matches
      return (
        <View style={styles.emptyState}>
          <MaterialIcons name="search-off" size={56} color={SipatColors.textMuted} />
          <Text style={styles.emptyTitle}>{t.projects.noResults}</Text>
        </View>
      );
    },
    [t.projects.noResults, searchQuery, activeFilter, isLoading, isError]
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Page title */}
      <Text style={styles.pageTitle}>{t.projects.title}</Text>

      {/* Search bar */}
      <View style={styles.searchContainer}>
        <MaterialIcons name="search" size={20} color={SipatColors.textMuted} style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder={t.projects.searchPlaceholder}
          placeholderTextColor={SipatColors.textMuted}
          value={searchQuery}
          onChangeText={setSearchQuery}
          autoCorrect={false}
          returnKeyType="search"
        />
        {searchQuery.length > 0 ? (
          <MaterialIcons
            name="close"
            size={18}
            color={SipatColors.textMuted}
            onPress={() => setSearchQuery('')}
            style={styles.clearIcon}
          />
        ) : null}
      </View>

      {/* Filter chips */}
      <ProjectFilters activeFilter={activeFilter} onFilterChange={setActiveFilter} />

      {/* Project list */}
      <FlatList
        data={filteredProjects}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        ListHeaderComponent={ListHeaderComponent}
        ListEmptyComponent={ListEmptyComponent}
        refreshControl={
          <RefreshControl
            refreshing={isRefetching}
            onRefresh={onRefresh}
            colors={[SipatColors.gold]}
            tintColor={SipatColors.gold}
          />
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: SipatColors.textPrimary,
    paddingHorizontal: 20,
    marginTop: 8,
    marginBottom: 16,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: SipatColors.cardBg,
    marginHorizontal: 20,
    marginBottom: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    paddingHorizontal: 12,
    height: 44,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 14,
    color: SipatColors.textPrimary,
    paddingVertical: 0,
  },
  clearIcon: {
    padding: 4,
  },
  listContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  listHeader: {
    marginBottom: 12,
  },
  projectCount: {
    fontSize: 14,
    fontWeight: '600',
    color: SipatColors.textSecondary,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 60,
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 15,
    color: SipatColors.textMuted,
    textAlign: 'center',
    marginTop: 12,
    lineHeight: 22,
  },
  emptySubtitle: {
    fontSize: 13,
    color: SipatColors.textMuted,
    textAlign: 'center',
    marginTop: 8,
  },
});
