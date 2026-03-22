import { StyleSheet, Text, TouchableOpacity } from 'react-native';

import { SipatColors } from '@/constants/theme';

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
    paddingVertical: 16,
    borderRadius: 12,
    marginHorizontal: 20,
    alignItems: 'center',
    // Gold shadow for that warm glow effect
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 10,
    elevation: 6,
  },
  text: {
    fontSize: 15,
    fontWeight: '800',
    color: SipatColors.navy,
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
});
