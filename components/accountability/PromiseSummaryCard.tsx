import { StyleSheet, Text, View } from 'react-native';

import { SipatColors, SipatSpacing, SipatRadius } from '@/constants/theme';

interface PromiseSummaryCardProps {
  label: string;
  count: number;
  percentage: number;
  color: string;
}

export function PromiseSummaryCard({ label, count, percentage, color }: PromiseSummaryCardProps) {
  return (
    <View style={styles.card}>
      <View style={[styles.indicator, { backgroundColor: color }]} />
      <View style={styles.content}>
        <Text style={styles.count}>{count}</Text>
        <Text style={styles.label}>{label}</Text>
      </View>
      <Text style={[styles.percentage, { color }]}>{percentage.toFixed(1)}%</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: SipatRadius.md,
    padding: SipatSpacing.md,
    gap: SipatSpacing.md,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  indicator: {
    width: 4,
    height: 40,
    borderRadius: 2,
  },
  content: {
    flex: 1,
  },
  count: {
    fontSize: 22,
    fontWeight: '700',
    color: SipatColors.textPrimary,
  },
  label: {
    fontSize: 13,
    color: SipatColors.textSecondary,
    marginTop: 2,
  },
  percentage: {
    fontSize: 16,
    fontWeight: '600',
  },
});
