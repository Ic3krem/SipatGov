import { ScrollView, StyleSheet, Text, TouchableOpacity } from 'react-native';

import { SipatColors, SipatSpacing } from '@/constants/theme';
import { useLanguage } from '@/hooks/use-language';
import type { ProjectStatus } from '@/types/models';

/** The filter value: null means "All", otherwise a specific ProjectStatus. */
export type ProjectFilterValue = ProjectStatus | null;

interface FilterChip {
  label: string;
  value: ProjectFilterValue;
}

interface ProjectFiltersProps {
  activeFilter: ProjectFilterValue;
  onFilterChange: (filter: ProjectFilterValue) => void;
}

export function ProjectFilters({ activeFilter, onFilterChange }: ProjectFiltersProps) {
  const { t } = useLanguage();

  const filters: FilterChip[] = [
    { label: t.projects.allFilter, value: null },
    { label: t.projects.ongoing, value: 'ongoing' },
    { label: t.projects.completed, value: 'completed' },
    { label: t.projects.bidding, value: 'bidding' },
    { label: t.projects.delayed, value: 'delayed' },
    { label: t.projects.planned, value: 'planned' },
  ];

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.container}
      style={styles.scroll}
    >
      {filters.map((chip) => {
        const isActive = activeFilter === chip.value;
        return (
          <TouchableOpacity
            key={chip.label}
            style={[styles.chip, isActive ? styles.chipActive : styles.chipInactive]}
            onPress={() => onFilterChange(chip.value)}
            activeOpacity={0.7}
          >
            <Text style={[styles.chipText, isActive ? styles.chipTextActive : styles.chipTextInactive]}>
              {chip.label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: {
    flexGrow: 0,
    marginBottom: SipatSpacing.lg,
  },
  container: {
    paddingHorizontal: SipatSpacing.xl,
    gap: SipatSpacing.sm,
  },
  chip: {
    height: 36,
    paddingHorizontal: 14,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  chipActive: {
    backgroundColor: SipatColors.gold,
  },
  chipInactive: {
    backgroundColor: SipatColors.cardBorder,
  },
  chipText: {
    fontSize: 13,
    fontWeight: '600',
  },
  chipTextActive: {
    color: SipatColors.navy,
  },
  chipTextInactive: {
    color: SipatColors.textSecondary,
  },
});
