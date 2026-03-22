import { StyleSheet, Text, View } from 'react-native';

import { PROMISE_STATUS_LABELS, getPromiseStatusColor } from '@/constants/status';
import type { PromiseStatus } from '@/types/models';

interface StatusBadgeProps {
  status: PromiseStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const color = getPromiseStatusColor(status);
  const label = PROMISE_STATUS_LABELS[status];

  return (
    <View style={[styles.badge, { backgroundColor: color + '1A' }]}>
      <View style={[styles.dot, { backgroundColor: color }]} />
      <Text style={[styles.text, { color }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
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
  text: {
    fontSize: 11,
    fontWeight: '600',
  },
});
