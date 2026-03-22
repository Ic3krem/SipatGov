import { StyleSheet, Text, View } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

import { REPORT_TYPE_COLORS, REPORT_TYPE_ICONS } from '@/constants/status';
import { useLanguage } from '@/hooks/use-language';
import type { ReportType } from '@/types/models';

interface ReportTypeChipProps {
  type: ReportType;
  /** Smaller variant for inline use */
  compact?: boolean;
}

export function ReportTypeChip({ type, compact = false }: ReportTypeChipProps) {
  const { t } = useLanguage();
  const color = REPORT_TYPE_COLORS[type];
  const iconName = REPORT_TYPE_ICONS[type] as keyof typeof MaterialIcons.glyphMap;
  const label = t.reports[type] ?? type;

  return (
    <View
      style={[
        styles.chip,
        { backgroundColor: color + '1A' },
        compact && styles.chipCompact,
      ]}
    >
      <MaterialIcons
        name={iconName}
        size={compact ? 10 : 12}
        color={color}
      />
      <Text
        style={[
          styles.label,
          { color },
          compact && styles.labelCompact,
        ]}
      >
        {label}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
    gap: 4,
    alignSelf: 'flex-start',
  },
  chipCompact: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
    gap: 3,
  },
  label: {
    fontSize: 11,
    fontWeight: '600',
  },
  labelCompact: {
    fontSize: 10,
  },
});
