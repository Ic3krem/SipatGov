import { useRouter } from 'expo-router';
import { Text, TouchableOpacity, View } from 'react-native';
import Animated, { FadeIn, FadeInDown, FadeInUp } from 'react-native-reanimated';

export default function OnboardingStep2() {
  const router = useRouter();

  return (
    <View className="flex-1 bg-sipat-onboarding-bg px-8 pt-20">
      <Animated.View entering={FadeIn.duration(800)} className="items-center mb-10">
        <View className="w-[180px] h-[180px] rounded-full bg-[rgba(212,168,67,0.1)] border-2 border-[rgba(212,168,67,0.3)] items-center justify-center">
          <Text style={{ fontSize: 72 }}>&#x2696;</Text>
        </View>
      </Animated.View>

      <Animated.View entering={FadeInUp.delay(300).duration(600)} className="mb-6">
        <Text className="text-sipat-accent text-sm font-semibold mb-4 tracking-widest">2 / 3</Text>
        <Text className="text-white text-[32px] font-extrabold mb-3 leading-[40px]">Ipaglaban ang Tama</Text>
        <Text className="text-sipat-onboarding-sub text-base leading-6">
          Subaybayan ang mga pangako ng iyong mga opisyal. Alamin kung aling mga pangako ang natupad, hindi natupad, o nakabinbin pa.
        </Text>
      </Animated.View>

      <Animated.View entering={FadeIn.delay(600).duration(600)} className="flex-row gap-2.5 mb-6">
        <View className="flex-1 bg-[rgba(255,255,255,0.05)] rounded-[10px] border-l-[3px] border-l-sipat-kept py-3 items-center gap-1">
          <Text style={{ fontSize: 20 }}>&#x2705;</Text>
          <Text className="text-sipat-onboarding-sub text-[11px] font-semibold">Natupad</Text>
        </View>
        <View className="flex-1 bg-[rgba(255,255,255,0.05)] rounded-[10px] border-l-[3px] border-l-sipat-broken py-3 items-center gap-1">
          <Text style={{ fontSize: 20 }}>&#x274C;</Text>
          <Text className="text-sipat-onboarding-sub text-[11px] font-semibold">Hindi Natupad</Text>
        </View>
        <View className="flex-1 bg-[rgba(255,255,255,0.05)] rounded-[10px] border-l-[3px] border-l-sipat-pending py-3 items-center gap-1">
          <Text style={{ fontSize: 20 }}>&#x23F3;</Text>
          <Text className="text-sipat-onboarding-sub text-[11px] font-semibold">Nakabinbin</Text>
        </View>
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(800).duration(400)} className="flex-row justify-between items-center absolute bottom-12 left-8 right-8">
        <TouchableOpacity className="py-3 px-5" onPress={() => router.push('/(onboarding)/step-3')}>
          <Text className="text-sipat-onboarding-sub text-base">Laktawan</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-sipat-accent py-3.5 px-10 rounded-xl" activeOpacity={0.8} onPress={() => router.push('/(onboarding)/step-3')}>
          <Text className="text-sipat-navy text-base font-bold">Susunod</Text>
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
}
