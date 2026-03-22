import { useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { router } from 'expo-router';

import { ShieldLogo } from '@/components/ShieldLogo';
import { SipatColors } from '@/constants/theme';
import { useLanguageStore } from '@/store/language-store';
import { isOnboardingCompleted } from '@/utils/storage';

SplashScreen.preventAutoHideAsync();

export default function SplashScreenPage() {
  const { language, isLoaded, loadLanguage } = useLanguageStore();

  useEffect(() => {
    loadLanguage();
  }, [loadLanguage]);

  useEffect(() => {
    if (!isLoaded) return;

    SplashScreen.hideAsync();

    const timer = setTimeout(async () => {
      if (!language) {
        router.replace('/language-select');
      } else {
        const onboarded = await isOnboardingCompleted();
        if (onboarded) {
          router.replace('/(tabs)');
        } else {
          router.replace('/(onboarding)' as any);
        }
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [isLoaded, language]);

  return (
    <View style={styles.container}>
      {/* Ambient purple glow behind the logo */}
      <View style={styles.glowOuter} />
      <View style={styles.glowInner} />

      <View style={styles.content}>
        <ShieldLogo size={180} />
        <Text style={styles.title}>SipatGov</Text>
        <Text style={styles.tagline}>Civic Transparency Platform</Text>
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
  glowOuter: {
    position: 'absolute',
    top: '12%',
    width: 340,
    height: 340,
    borderRadius: 170,
    backgroundColor: SipatColors.purple,
    opacity: 0.35,
  },
  glowInner: {
    position: 'absolute',
    top: '18%',
    width: 200,
    height: 200,
    borderRadius: 100,
    backgroundColor: SipatColors.gold,
    opacity: 0.06,
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 38,
    fontWeight: '700',
    color: SipatColors.red,
    marginTop: 16,
    letterSpacing: 3,
  },
  tagline: {
    fontSize: 13,
    color: SipatColors.onboardingSubtext,
    marginTop: 8,
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
});
