import { useEffect, useMemo, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { format } from 'date-fns';

import { SipatColors } from '@/constants/theme';

export function DashboardHeader() {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 60_000);
    return () => clearInterval(interval);
  }, []);

  const dateStr = useMemo(() => format(now, 'MMMM d, yyyy').toUpperCase(), [now]);
  const timeStr = useMemo(() => format(now, 'h:mm a'), [now]);

  return (
    <View style={styles.container}>
      <Text style={styles.date}>{dateStr}</Text>
      <Text style={styles.time}>{timeStr}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: SipatColors.cardBorder,
  },
  date: {
    fontSize: 12,
    fontWeight: '700',
    color: SipatColors.navyLight,
    letterSpacing: 1,
  },
  time: {
    fontSize: 12,
    fontWeight: '500',
    color: SipatColors.textSecondary,
  },
});
