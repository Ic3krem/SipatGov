import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { router } from 'expo-router';

import { ShieldLogo } from '@/components/ShieldLogo';
import { SipatColors } from '@/constants/theme';
import { useLanguageStore } from '@/store/language-store';
import type { Language } from '@/utils/i18n';

export default function LanguageSelectScreen() {
  const setLanguage = useLanguageStore((s) => s.setLanguage);

  const handleSelect = async (lang: Language) => {
    await setLanguage(lang);
    router.replace('/(onboarding)' as any);
  };

  return (
    <View style={styles.container}>
      {/* Purple glow behind logo */}
      <View style={styles.glow} />

      <View style={styles.content}>
        <ShieldLogo size={130} />

        <Text style={styles.title}>Pumili ng Wika</Text>
        <Text style={styles.subtitle}>Choose Your Language</Text>

        <View style={styles.buttons}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => handleSelect('tl')}
            activeOpacity={0.8}
          >
            <Text style={styles.buttonText}>TAGALOG</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.button}
            onPress={() => handleSelect('en')}
            activeOpacity={0.8}
          >
            <Text style={styles.buttonText}>ENGLISH</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.navy,
    alignItems: 'center',
    justifyContent: 'center',
  },
  glow: {
    position: 'absolute',
    top: '15%',
    width: 300,
    height: 300,
    borderRadius: 150,
    backgroundColor: SipatColors.purple,
    opacity: 0.3,
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 22,
    fontWeight: '600',
    color: SipatColors.onboardingText,
    marginTop: 32,
  },
  subtitle: {
    fontSize: 16,
    color: SipatColors.onboardingSubtext,
    marginTop: 6,
  },
  buttons: {
    marginTop: 48,
    gap: 16,
    width: 220,
  },
  button: {
    backgroundColor: SipatColors.gold,
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '700',
    color: SipatColors.navy,
    letterSpacing: 1.5,
  },
});
