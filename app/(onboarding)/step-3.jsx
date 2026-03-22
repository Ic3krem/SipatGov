import { useRouter } from 'expo-router';
import { useState } from 'react';
import { FlatList, Text, TouchableOpacity, View } from 'react-native';
import Animated, { FadeIn, FadeInDown, FadeInUp } from 'react-native-reanimated';

import { PHILIPPINE_REGIONS } from '@/constants/regions';
import { useOnboarding } from '@/hooks/use-onboarding';

export default function OnboardingStep3() {
  const router = useRouter();
  const { markComplete } = useOnboarding();
  const [selectedRegionId, setSelectedRegionId] = useState(null);

  const handleFinish = async () => {
    const regionId = selectedRegionId ?? 1;
    await markComplete(regionId, regionId);
    router.replace('/(tabs)/');
  };

  return (
    <View className="flex-1 bg-sipat-onboarding-bg pt-20">
      <Animated.View entering={FadeInUp.duration(600)} className="px-8 mb-6">
        <Text className="text-sipat-accent text-sm font-semibold mb-4 tracking-widest">3 / 3</Text>
        <Text className="text-white text-[28px] font-extrabold mb-2">Pumili ng Iyong Lugar</Text>
        <Text className="text-sipat-onboarding-sub text-[15px] leading-[22px]">
          Piliin ang iyong rehiyon para makita ang mga proyekto at budget na malapit sa iyo.
        </Text>
      </Animated.View>

      <Animated.View entering={FadeIn.delay(300).duration(600)} className="flex-1 px-6">
        <FlatList
          data={PHILIPPINE_REGIONS}
          keyExtractor={(item) => String(item.id)}
          showsVerticalScrollIndicator={false}
          renderItem={({ item }) => {
            const sel = selectedRegionId === item.id;
            return (
              <TouchableOpacity
                className={`flex-row items-center rounded-xl py-3.5 px-4 mb-2 border ${sel ? 'bg-[rgba(212,168,67,0.1)] border-sipat-accent' : 'bg-[rgba(255,255,255,0.04)] border-transparent'}`}
                activeOpacity={0.7}
                onPress={() => setSelectedRegionId(item.id)}
              >
                <View className={`w-[22px] h-[22px] rounded-full border-2 items-center justify-center mr-3.5 ${sel ? 'border-sipat-accent' : 'border-sipat-onboarding-sub'}`}>
                  {sel && <View className="w-3 h-3 rounded-full bg-sipat-accent" />}
                </View>
                <View className="flex-1 flex-row items-center gap-2.5">
                  <Text className={`text-[13px] font-bold w-14 ${sel ? 'text-sipat-accent' : 'text-sipat-onboarding-sub'}`}>{item.code}</Text>
                  <Text className={`text-sm flex-1 text-white ${sel ? 'font-semibold' : ''}`} numberOfLines={1}>{item.name}</Text>
                </View>
              </TouchableOpacity>
            );
          }}
        />
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(500).duration(400)} className="px-8 pb-12 pt-4">
        <TouchableOpacity
          className={`bg-sipat-accent py-4 rounded-xl items-center ${!selectedRegionId ? 'opacity-40' : ''}`}
          activeOpacity={0.8}
          onPress={handleFinish}
          disabled={!selectedRegionId}
        >
          <Text className="text-sipat-navy text-lg font-bold tracking-wide">Tapusin</Text>
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
}
