import { useCallback, useRef, useState } from 'react';
import {
  FlatList,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  type ViewToken,
} from 'react-native';
import { router } from 'expo-router';
import { MaterialIcons } from '@expo/vector-icons';

import { DotIndicator } from '@/components/onboarding/DotIndicator';
import { OnboardingCard } from '@/components/onboarding/OnboardingCard';
import { SipatColors } from '@/constants/theme';
import { useLanguage } from '@/hooks/use-language';
import { setOnboardingCompleted } from '@/utils/storage';

const VIEWABILITY_CONFIG = { viewAreaCoveragePercentThreshold: 50 };

export default function OnboardingScreen() {
  const { t } = useLanguage();
  const [currentIndex, setCurrentIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);

  const slides = [
    { key: '1', title: t.onboarding.step1Title, subtitle: t.onboarding.step1Subtitle, body: t.onboarding.step1Body },
    { key: '2', title: t.onboarding.step2Title, subtitle: t.onboarding.step2Subtitle, body: t.onboarding.step2Body },
    { key: '3', title: t.onboarding.step3Title, subtitle: t.onboarding.step3Subtitle, body: t.onboarding.step3Body },
    { key: '4', title: t.onboarding.step4Title, subtitle: t.onboarding.step4Subtitle, body: t.onboarding.step4Body },
  ];

  const isLastSlide = currentIndex === slides.length - 1;

  const onViewableItemsChanged = useCallback(
    ({ viewableItems }: { viewableItems: ViewToken[] }) => {
      if (viewableItems.length > 0 && viewableItems[0].index != null) {
        setCurrentIndex(viewableItems[0].index);
      }
    },
    [],
  );

  const handleNext = () => {
    if (isLastSlide) {
      handleFinishOnboarding();
    } else {
      flatListRef.current?.scrollToIndex({ index: currentIndex + 1 });
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      flatListRef.current?.scrollToIndex({ index: currentIndex - 1 });
    }
  };

  const handleFinishOnboarding = async () => {
    await setOnboardingCompleted(true);
    router.replace('/(tabs)');
  };

  return (
    <View style={styles.container}>
      <FlatList
        ref={flatListRef}
        data={slides}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        bounces={false}
        keyExtractor={(item) => item.key}
        renderItem={({ item }) => (
          <OnboardingCard
            title={item.title}
            subtitle={item.subtitle}
            body={item.body}
          />
        )}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={VIEWABILITY_CONFIG}
      />

      {/* Navigation chevrons */}
      {currentIndex > 0 && (
        <TouchableOpacity
          style={[styles.chevron, styles.chevronLeft]}
          onPress={handlePrev}
          activeOpacity={0.6}
        >
          <MaterialIcons name="chevron-left" size={28} color={SipatColors.textMuted} />
        </TouchableOpacity>
      )}
      {!isLastSlide && (
        <TouchableOpacity
          style={[styles.chevron, styles.chevronRight]}
          onPress={handleNext}
          activeOpacity={0.6}
        >
          <MaterialIcons name="chevron-right" size={28} color={SipatColors.textMuted} />
        </TouchableOpacity>
      )}

      {/* Bottom controls */}
      <View style={styles.controls}>
        <TouchableOpacity onPress={handleFinishOnboarding} style={styles.skipButton}>
          <Text style={styles.skipText}>{t.onboarding.skip}</Text>
        </TouchableOpacity>

        <DotIndicator total={slides.length} current={currentIndex} />

        <TouchableOpacity
          onPress={handleNext}
          style={[styles.nextButton, isLastSlide && styles.getStartedButton]}
          activeOpacity={0.8}
        >
          <Text style={[styles.nextText, isLastSlide && styles.getStartedText]}>
            {isLastSlide ? t.onboarding.getStarted : t.onboarding.next}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  chevron: {
    position: 'absolute',
    top: '45%',
    zIndex: 10,
    padding: 4,
  },
  chevronLeft: {
    left: 8,
  },
  chevronRight: {
    right: 8,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingBottom: 40,
    paddingTop: 16,
    backgroundColor: '#FFFFFF',
  },
  skipButton: {
    padding: 8,
    minWidth: 80,
  },
  skipText: {
    fontSize: 15,
    color: SipatColors.textSecondary,
  },
  nextButton: {
    padding: 8,
    minWidth: 80,
    alignItems: 'flex-end',
  },
  nextText: {
    fontSize: 15,
    fontWeight: '600',
    color: SipatColors.gold,
  },
  getStartedButton: {
    backgroundColor: SipatColors.gold,
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4,
  },
  getStartedText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
});
