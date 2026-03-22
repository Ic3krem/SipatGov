import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { SipatColors } from '@/constants/theme';

interface LGUMarkerProps {
  score: number;
  name: string;
  selected?: boolean;
}

function getScoreColor(score: number): string {
  if (score >= 75) return SipatColors.kept;
  if (score >= 50) return SipatColors.gold;
  return SipatColors.red;
}

export const LGUMarker = React.memo(function LGUMarker({ score, name, selected }: LGUMarkerProps) {
  const color = getScoreColor(score);

  return (
    <View style={styles.container}>
      {selected && (
        <View style={styles.tooltip}>
          <Text style={styles.tooltipText} numberOfLines={1}>{name}</Text>
        </View>
      )}
      <View style={[styles.marker, { backgroundColor: color }, selected && styles.selected]}>
        <Text style={styles.score}>{Math.round(score)}</Text>
      </View>
      <View style={[styles.arrow, { borderTopColor: color }]} />
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  marker: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#FFFFFF',
    shadowColor: SipatColors.navy,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  selected: {
    width: 40,
    height: 40,
    borderRadius: 20,
    borderWidth: 3,
    borderColor: SipatColors.gold,
  },
  score: {
    fontSize: 10,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  arrow: {
    width: 0,
    height: 0,
    borderLeftWidth: 6,
    borderRightWidth: 6,
    borderTopWidth: 8,
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    marginTop: -1,
  },
  tooltip: {
    position: 'absolute',
    top: -28,
    backgroundColor: SipatColors.navy,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    maxWidth: 130,
  },
  tooltipText: {
    fontSize: 10,
    color: '#FFFFFF',
    fontWeight: '600',
  },
});
