import { StyleSheet, Text, View } from 'react-native';

import { StatusBadge } from './StatusBadge';
import { SipatColors, SipatSpacing, SipatRadius } from '@/constants/theme';
import { formatDate, formatConfidence } from '@/utils/format';
import type { PromiseItem } from '@/types/models';

interface PromiseListItemProps {
  promise: PromiseItem;
}

export function PromiseListItem({ promise }: PromiseListItemProps) {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title} numberOfLines={2}>{promise.title}</Text>
        <StatusBadge status={promise.status} />
      </View>

      {promise.description && (
        <Text style={styles.description} numberOfLines={3}>{promise.description}</Text>
      )}

      {promise.category && (
        <Text style={styles.category}>{promise.category}</Text>
      )}

      <View style={styles.footer}>
        {promise.date_promised && (
          <Text style={styles.meta}>Promised: {formatDate(promise.date_promised)}</Text>
        )}
        {promise.confidence_score != null && (
          <Text style={styles.meta}>Confidence: {formatConfidence(promise.confidence_score)}</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: SipatRadius.md,
    padding: SipatSpacing.md,
    gap: SipatSpacing.sm,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: SipatSpacing.sm,
  },
  title: {
    flex: 1,
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
  category: {
    fontSize: 12,
    color: SipatColors.textSecondary,
    fontWeight: '500',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  meta: {
    fontSize: 11,
    color: SipatColors.textMuted,
  },
});
