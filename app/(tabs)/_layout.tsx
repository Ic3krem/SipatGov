import { Tabs } from 'expo-router';
import { MaterialIcons } from '@expo/vector-icons';

import { SipatColors, SipatTypography } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { useLanguage } from '@/hooks/use-language';
import { HapticTab } from '@/components/haptic-tab';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const { t } = useLanguage();
  const isDark = colorScheme === 'dark';

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: SipatColors.gold,
        tabBarInactiveTintColor: isDark ? '#5A6678' : '#9AA3B0',
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarLabelStyle: {
          ...SipatTypography.tabLabel,
        },
        tabBarIconStyle: {
          marginTop: 2,
        },
        tabBarStyle: {
          backgroundColor: isDark ? SipatColors.navy : '#FFFFFF',
          borderTopColor: isDark ? '#1E2040' : SipatColors.cardBorder,
          borderTopWidth: 1,
          paddingTop: 6,
          paddingBottom: 8,
          height: 60,
          elevation: 8,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: -2 },
          shadowOpacity: 0.06,
          shadowRadius: 4,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: t.tabs.dashboard,
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="map" size={24} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="accountability"
        options={{
          title: t.tabs.accountability,
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="balance" size={24} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="projects"
        options={{
          title: t.tabs.projects,
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="construction" size={24} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="reports"
        options={{
          title: t.tabs.reports,
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="campaign" size={24} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: t.tabs.profile,
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="person" size={24} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
