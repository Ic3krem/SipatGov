import { StyleSheet, View } from 'react-native';

import { SipatColors } from '@/constants/theme';

interface DotIndicatorProps {
  total: number;
  current: number;
}

export function DotIndicator({ total, current }: DotIndicatorProps) {
  return (
    <View style={styles.container}>
      {Array.from({ length: total }, (_, i) => (
        <View
          key={i}
          style={[
            styles.dot,
            i === current ? styles.activeDot : styles.inactiveDot,
          ]}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  activeDot: {
    width: 24,
    backgroundColor: SipatColors.gold,
  },
  inactiveDot: {
    width: 8,
    backgroundColor: SipatColors.navyLight,
    opacity: 0.25,
  },
});
