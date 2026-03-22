import React, { useMemo } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Svg, { Circle as SvgCircle } from 'react-native-svg';

import { SipatColors, SipatSpacing } from '@/constants/theme';

interface StatItem {
  label: string;
  value: number;
  total: number;
  color: string;
}

interface QuickStatsProps {
  stats: StatItem[];
}

const SIZE = 56;
const STROKE_WIDTH = 4;
const RADIUS = (SIZE - STROKE_WIDTH) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

const CircularIndicator = React.memo(function CircularIndicator({ value, total, color, label }: StatItem) {
  const strokeDashoffset = useMemo(() => {
    const progress = total > 0 ? value / total : 0;
    return CIRCUMFERENCE * (1 - progress);
  }, [value, total]);

  return (
    <View style={styles.statItem}>
      <View style={styles.circleContainer}>
        <Svg width={SIZE} height={SIZE}>
          {/* Background track */}
          <SvgCircle
            cx={SIZE / 2}
            cy={SIZE / 2}
            r={RADIUS}
            stroke={SipatColors.cardBorder}
            strokeWidth={STROKE_WIDTH}
            fill="transparent"
          />
          {/* Progress arc */}
          <SvgCircle
            cx={SIZE / 2}
            cy={SIZE / 2}
            r={RADIUS}
            stroke={color}
            strokeWidth={STROKE_WIDTH}
            fill="transparent"
            strokeDasharray={`${CIRCUMFERENCE}`}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            rotation="-90"
            origin={`${SIZE / 2}, ${SIZE / 2}`}
          />
        </Svg>
        <Text style={styles.statValue}>{value}</Text>
      </View>
      <Text style={styles.statLabel} numberOfLines={1}>{label}</Text>
    </View>
  );
});

export function QuickStats({ stats }: QuickStatsProps) {
  return (
    <View style={styles.container}>
      {stats.map((stat) => (
        <CircularIndicator key={stat.label} {...stat} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: SipatSpacing.lg,
    paddingHorizontal: SipatSpacing.md,
  },
  statItem: {
    alignItems: 'center',
    gap: SipatSpacing.sm,
  },
  circleContainer: {
    position: 'relative',
    alignItems: 'center',
    justifyContent: 'center',
  },
  statValue: {
    position: 'absolute',
    fontSize: 14,
    fontWeight: '700',
    color: SipatColors.navyLight,
  },
  statLabel: {
    fontSize: 10,
    color: SipatColors.textSecondary,
    fontWeight: '500',
    maxWidth: 70,
    textAlign: 'center',
  },
});
