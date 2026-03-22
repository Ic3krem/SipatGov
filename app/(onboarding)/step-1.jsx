import { useRouter } from 'expo-router';
import { Text, TouchableOpacity, View } from 'react-native';
import Animated, { FadeIn, FadeInDown, FadeInUp } from 'react-native-reanimated';

export default function OnboardingStep1() {
  const router = useRouter();

  return (
    <View className="flex-1 bg-sipat-onboarding-bg px-8 pt-20">
      <Animated.View entering={FadeIn.duration(800)} className="items-center mb-12">
        <View className="w-[200px] h-[200px] rounded-full bg-[rgba(212,168,67,0.1)] border-2 border-[rgba(212,168,67,0.3)] items-center justify-center">
          <Text style={{ fontSize: 80 }}>&#x1F441;</Text>
        </View>
      </Animated.View>

      <Animated.View entering={FadeInUp.delay(300).duration(600)} className="flex-1">
        <Text className="text-sipat-accent text-sm font-semibold mb-4 tracking-widest">1 / 3</Text>
        <Text className="text-white text-[32px] font-extrabold mb-4 leading-[40px]">Buksan ang mga mata</Text>
        <Text className="text-sipat-onboarding-sub text-base leading-6">
          Alamin kung saan napupunta ang pondo ng iyong lungsod. Tingnan ang mga budget, proyekto, at gastusin ng iyong lokal na pamahalaan.
        </Text>
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(600).duration(400)} className="flex-row justify-between items-center pb-12">
        <TouchableOpacity className="py-3 px-5" onPress={() => router.push('/(onboarding)/step-3')}>
          <Text className="text-sipat-onboarding-sub text-base">Laktawan</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-sipat-accent py-3.5 px-10 rounded-xl" activeOpacity={0.8} onPress={() => router.push('/(onboarding)/step-2')}>
          <Text className="text-sipat-navy text-base font-bold">Susunod</Text>
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
}
