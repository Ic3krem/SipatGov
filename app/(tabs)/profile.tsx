import { useState } from 'react';
import {
  Alert,
  Modal,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';

import { SipatColors, SipatSpacing, SipatRadius, SipatTypography } from '@/constants/theme';
import { PHILIPPINE_REGIONS, type RegionData } from '@/constants/regions';
import { useLanguage } from '@/hooks/use-language';
import { useAuthStore } from '@/store/auth-store';
import type { User } from '@/types/models';

// ── Mock user for display while auth isn't connected ──────
const MOCK_USER: User = {
  id: 1,
  email: 'juan.delacruz@email.com',
  phone: '+63 917 123 4567',
  display_name: 'Juan dela Cruz',
  avatar_url: null,
  home_lgu_id: 1,
  home_region_id: 1,
  role: 'citizen',
  is_verified: true,
  onboarding_completed: true,
};

// ── Mock stats ────────────────────────────────────────────
const MOCK_STATS = {
  reportsCount: 12,
  upvotes: 48,
  daysActive: 34,
};

// ── Role badge label helper ───────────────────────────────
function getRoleBadge(role: User['role'], t: Record<string, string>) {
  switch (role) {
    case 'citizen':
      return t.citizen;
    case 'moderator':
      return t.moderator;
    case 'admin':
      return t.admin;
    default:
      return t.citizen;
  }
}

export default function ProfileScreen() {
  const { t, lang, toggleLanguage } = useLanguage();
  const logout = useAuthStore((s) => s.logout);

  // Use the auth store user if available, fallback to mock
  const authUser = useAuthStore((s) => s.user);
  const user = authUser ?? MOCK_USER;

  // Local state for settings
  const [selectedRegionId, setSelectedRegionId] = useState<number>(
    user.home_region_id ?? 1
  );
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [darkModeEnabled, setDarkModeEnabled] = useState(false);
  const [regionPickerVisible, setRegionPickerVisible] = useState(false);

  // Derived
  const selectedRegion = PHILIPPINE_REGIONS.find(
    (r) => r.id === selectedRegionId
  );

  // Handlers
  const handleLogout = () => {
    Alert.alert(
      t.profile.logout,
      t.profile.logoutConfirm,
      [
        { text: t.reports?.cancel ?? 'Cancel', style: 'cancel' },
        {
          text: t.profile.logout,
          style: 'destructive',
          onPress: () => logout(),
        },
      ]
    );
  };

  const handleSelectRegion = (region: RegionData) => {
    setSelectedRegionId(region.id);
    setRegionPickerVisible(false);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* ── Avatar Section ─────────────────────────────── */}
        <View style={styles.avatarSection}>
          <View style={styles.avatarCircle}>
            <MaterialIcons name="person" size={52} color={SipatColors.textMuted} />
          </View>
          <Text style={styles.displayName}>
            {user.display_name ?? 'SipatGov User'}
          </Text>
          <Text style={styles.contactInfo}>
            {user.email ?? user.phone ?? ''}
          </Text>
          <View style={styles.roleBadge}>
            <MaterialIcons
              name="verified-user"
              size={14}
              color={SipatColors.gold}
            />
            <Text style={styles.roleBadgeText}>
              {getRoleBadge(user.role, t.profile)}
            </Text>
          </View>
        </View>

        {/* ── Stats Row ──────────────────────────────────── */}
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{MOCK_STATS.reportsCount}</Text>
            <Text style={styles.statLabel}>{t.profile.statsReports}</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{MOCK_STATS.upvotes}</Text>
            <Text style={styles.statLabel}>{t.profile.statsUpvotes}</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{MOCK_STATS.daysActive}</Text>
            <Text style={styles.statLabel}>{t.profile.statsDaysActive}</Text>
          </View>
        </View>

        {/* ── Settings Section ───────────────────────────── */}
        <Text style={styles.sectionTitle}>{t.profile.settingsTitle}</Text>
        <View style={styles.settingsCard}>
          {/* Language toggle */}
          <TouchableOpacity
            style={styles.settingsItem}
            onPress={toggleLanguage}
            activeOpacity={0.6}
          >
            <View style={styles.settingsItemLeft}>
              <View style={[styles.settingsIcon, { backgroundColor: SipatColors.blue + '15' }]}>
                <MaterialIcons name="language" size={20} color={SipatColors.blue} />
              </View>
              <View>
                <Text style={styles.settingsItemTitle}>{t.profile.language}</Text>
                <Text style={styles.settingsItemSubtitle}>
                  {lang === 'en' ? t.profile.languageEn : t.profile.languageTl}
                </Text>
              </View>
            </View>
            <MaterialIcons
              name="chevron-right"
              size={22}
              color={SipatColors.textMuted}
            />
          </TouchableOpacity>

          <View style={styles.settingsDivider} />

          {/* Home Region selector */}
          <TouchableOpacity
            style={styles.settingsItem}
            onPress={() => setRegionPickerVisible(true)}
            activeOpacity={0.6}
          >
            <View style={styles.settingsItemLeft}>
              <View style={[styles.settingsIcon, { backgroundColor: SipatColors.gold + '20' }]}>
                <MaterialIcons name="location-on" size={20} color={SipatColors.gold} />
              </View>
              <View style={styles.settingsTextContainer}>
                <Text style={styles.settingsItemTitle}>{t.profile.region}</Text>
                <Text style={styles.settingsItemSubtitle} numberOfLines={1}>
                  {selectedRegion?.name ?? t.profile.regionSelect}
                </Text>
              </View>
            </View>
            <MaterialIcons
              name="chevron-right"
              size={22}
              color={SipatColors.textMuted}
            />
          </TouchableOpacity>

          <View style={styles.settingsDivider} />

          {/* Notifications toggle */}
          <View style={styles.settingsItem}>
            <View style={styles.settingsItemLeft}>
              <View style={[styles.settingsIcon, { backgroundColor: SipatColors.red + '15' }]}>
                <MaterialIcons name="notifications" size={20} color={SipatColors.red} />
              </View>
              <Text style={styles.settingsItemTitle}>{t.profile.notifications}</Text>
            </View>
            <Switch
              value={notificationsEnabled}
              onValueChange={setNotificationsEnabled}
              trackColor={{
                false: '#D1D5DB',
                true: SipatColors.gold + 'AA',
              }}
              thumbColor={notificationsEnabled ? SipatColors.gold : '#F3F4F6'}
              ios_backgroundColor="#D1D5DB"
            />
          </View>

          <View style={styles.settingsDivider} />

          {/* Dark mode toggle */}
          <View style={styles.settingsItem}>
            <View style={styles.settingsItemLeft}>
              <View style={[styles.settingsIcon, { backgroundColor: SipatColors.navy + '12' }]}>
                <MaterialIcons name="dark-mode" size={20} color={SipatColors.navy} />
              </View>
              <Text style={styles.settingsItemTitle}>{t.profile.darkMode}</Text>
            </View>
            <Switch
              value={darkModeEnabled}
              onValueChange={setDarkModeEnabled}
              trackColor={{
                false: '#D1D5DB',
                true: SipatColors.gold + 'AA',
              }}
              thumbColor={darkModeEnabled ? SipatColors.gold : '#F3F4F6'}
              ios_backgroundColor="#D1D5DB"
            />
          </View>

          <View style={styles.settingsDivider} />

          {/* About */}
          <TouchableOpacity style={styles.settingsItem} activeOpacity={0.6}>
            <View style={styles.settingsItemLeft}>
              <View style={[styles.settingsIcon, { backgroundColor: SipatColors.blueLight + '15' }]}>
                <MaterialIcons name="info" size={20} color={SipatColors.blueLight} />
              </View>
              <View>
                <Text style={styles.settingsItemTitle}>{t.profile.about}</Text>
                <Text style={styles.settingsItemSubtitle}>
                  {t.profile.version} 1.0.0
                </Text>
              </View>
            </View>
            <MaterialIcons
              name="chevron-right"
              size={22}
              color={SipatColors.textMuted}
            />
          </TouchableOpacity>
        </View>

        {/* ── Logout Button ──────────────────────────────── */}
        <TouchableOpacity
          style={styles.logoutButton}
          onPress={handleLogout}
          activeOpacity={0.7}
        >
          <MaterialIcons name="logout" size={20} color={SipatColors.red} />
          <Text style={styles.logoutText}>{t.profile.logout}</Text>
        </TouchableOpacity>

        {/* Bottom spacing */}
        <View style={styles.bottomSpacer} />
      </ScrollView>

      {/* ── Region Picker Modal ──────────────────────────── */}
      <Modal
        visible={regionPickerVisible}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={() => setRegionPickerVisible(false)}
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>{t.profile.regionSelect}</Text>
            <TouchableOpacity
              onPress={() => setRegionPickerVisible(false)}
              hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            >
              <MaterialIcons name="close" size={24} color={SipatColors.textPrimary} />
            </TouchableOpacity>
          </View>
          <ScrollView style={styles.regionList}>
            {PHILIPPINE_REGIONS.map((region) => {
              const isSelected = region.id === selectedRegionId;
              return (
                <TouchableOpacity
                  key={region.id}
                  style={[
                    styles.regionItem,
                    isSelected && styles.regionItemSelected,
                  ]}
                  onPress={() => handleSelectRegion(region)}
                  activeOpacity={0.6}
                >
                  <Text
                    style={[
                      styles.regionItemText,
                      isSelected && styles.regionItemTextSelected,
                    ]}
                  >
                    {region.name}
                  </Text>
                  {isSelected && (
                    <MaterialIcons
                      name="check-circle"
                      size={22}
                      color={SipatColors.gold}
                    />
                  )}
                </TouchableOpacity>
              );
            })}
            <View style={{ height: 40 }} />
          </ScrollView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

// ── Styles ──────────────────────────────────────────────────
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: SipatSpacing.xl,
    paddingTop: SipatSpacing.md,
  },

  // ── Avatar Section ─────────────────────────────────────
  avatarSection: {
    alignItems: 'center',
    paddingVertical: SipatSpacing.xxl,
  },
  avatarCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: SipatColors.cardBg,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: SipatColors.gold,
    shadowColor: SipatColors.gold,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 4,
  },
  displayName: {
    fontSize: 22,
    fontWeight: '700',
    color: SipatColors.navy,
    marginTop: 14,
  },
  contactInfo: {
    ...SipatTypography.bodySmall,
    color: SipatColors.textSecondary,
    marginTop: SipatSpacing.xs,
  },
  roleBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    marginTop: 10,
    paddingHorizontal: 14,
    paddingVertical: 5,
    backgroundColor: SipatColors.goldPale,
    borderRadius: SipatRadius.lg,
  },
  roleBadgeText: {
    ...SipatTypography.bodySmall,
    fontWeight: '600',
    color: SipatColors.gold,
  },

  // ── Stats Row ──────────────────────────────────────────
  statsRow: {
    flexDirection: 'row',
    gap: SipatSpacing.md,
    marginBottom: SipatSpacing.xxl,
  },
  statCard: {
    flex: 1,
    backgroundColor: SipatColors.cardBg,
    borderRadius: SipatRadius.md,
    paddingVertical: SipatSpacing.lg,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  statNumber: {
    fontSize: 22,
    fontWeight: '700',
    color: SipatColors.navy,
  },
  statLabel: {
    ...SipatTypography.caption,
    fontWeight: '500',
    color: SipatColors.textMuted,
    marginTop: SipatSpacing.xs,
    textAlign: 'center',
  },

  // ── Settings Section ───────────────────────────────────
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: SipatColors.navy,
    marginBottom: 10,
    paddingLeft: SipatSpacing.xs,
  },
  settingsCard: {
    backgroundColor: SipatColors.cardBg,
    borderRadius: SipatRadius.md,
    paddingVertical: SipatSpacing.xs,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  settingsItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SipatSpacing.lg,
    minHeight: 56,
  },
  settingsItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SipatSpacing.md,
    flex: 1,
  },
  settingsTextContainer: {
    flex: 1,
    marginRight: SipatSpacing.sm,
  },
  settingsIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  settingsItemTitle: {
    ...SipatTypography.body,
    fontWeight: '500',
    color: SipatColors.textPrimary,
  },
  settingsItemSubtitle: {
    fontSize: 12,
    color: SipatColors.textMuted,
    marginTop: 2,
  },
  settingsDivider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: SipatColors.cardBorder,
    marginLeft: 64,
  },

  // ── Logout Button ──────────────────────────────────────
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: SipatSpacing.sm,
    marginTop: SipatSpacing.xxl,
    height: 48,
    borderRadius: SipatRadius.md,
    borderWidth: 1.5,
    borderColor: SipatColors.red,
    backgroundColor: SipatColors.cardBg,
  },
  logoutText: {
    fontSize: 16,
    fontWeight: '600',
    color: SipatColors.red,
  },
  bottomSpacer: {
    height: 40,
  },

  // ── Region Picker Modal ────────────────────────────────
  modalContainer: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SipatSpacing.xl,
    paddingVertical: SipatSpacing.lg,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: SipatColors.cardBorder,
    backgroundColor: SipatColors.cardBg,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: SipatColors.navy,
  },
  regionList: {
    flex: 1,
    paddingHorizontal: SipatSpacing.lg,
    paddingTop: SipatSpacing.sm,
  },
  regionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: SipatSpacing.lg,
    paddingVertical: 14,
    marginVertical: 3,
    borderRadius: 10,
    backgroundColor: SipatColors.cardBg,
  },
  regionItemSelected: {
    backgroundColor: SipatColors.goldPale,
    borderWidth: 1,
    borderColor: SipatColors.gold + '40',
  },
  regionItemText: {
    ...SipatTypography.body,
    fontWeight: '500',
    color: SipatColors.textPrimary,
    flex: 1,
    marginRight: SipatSpacing.sm,
  },
  regionItemTextSelected: {
    color: SipatColors.navy,
    fontWeight: '600',
  },
});
