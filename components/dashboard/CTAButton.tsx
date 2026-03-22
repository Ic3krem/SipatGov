import { StyleSheet, Text, TouchableOpacity } from 'react-native';

import { SipatColors, SipatRadius, SipatSpacing } from '@/constants/theme';

interface CTAButtonProps {
  text: string;
  onPress?: () => void;
}

export function CTAButton({ text, onPress }: CTAButtonProps) {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress} activeOpacity={0.85}>
      <Text style={styles.text}>{text}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: SipatColors.gold,
    height: 56,
    borderRadius: SipatRadius.pill,
    marginHorizontal: SipatSpacing.xl,
    alignItems: 'center',
    justifyContent: 'center',
    // Gold shadow for that warm glow effect
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 10,
    elevation: 6,
  },
  text: {
    fontSize: 16,
    fontWeight: '700',
    color: SipatColors.navy,
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
});
