import AsyncStorage from '@react-native-async-storage/async-storage';

const ONBOARDING_KEY = 'sipatgov_onboarding_completed';
const HOME_LGU_KEY = 'sipatgov_home_lgu_id';
const HOME_REGION_KEY = 'sipatgov_home_region_id';
const LAST_SYNC_KEY = 'sipatgov_last_sync';

export async function isOnboardingCompleted(): Promise<boolean> {
  try {
    const value = await AsyncStorage.getItem(ONBOARDING_KEY);
    return value === 'true';
  } catch {
    return false;
  }
}

export async function setOnboardingCompleted(completed: boolean): Promise<void> {
  await AsyncStorage.setItem(ONBOARDING_KEY, String(completed));
}

export async function getHomeLguId(): Promise<number | null> {
  const str = await AsyncStorage.getItem(HOME_LGU_KEY);
  if (!str) return null;
  const value = parseInt(str, 10);
  return isNaN(value) ? null : value;
}

export async function setHomeLguId(lguId: number): Promise<void> {
  await AsyncStorage.setItem(HOME_LGU_KEY, String(lguId));
}

export async function getHomeRegionId(): Promise<number | null> {
  const str = await AsyncStorage.getItem(HOME_REGION_KEY);
  if (!str) return null;
  const value = parseInt(str, 10);
  return isNaN(value) ? null : value;
}

export async function setHomeRegionId(regionId: number): Promise<void> {
  await AsyncStorage.setItem(HOME_REGION_KEY, String(regionId));
}

export async function getLastSyncTime(): Promise<Date | null> {
  const value = await AsyncStorage.getItem(LAST_SYNC_KEY);
  if (!value) return null;
  const date = new Date(value);
  return isNaN(date.getTime()) ? null : date;
}

export async function setLastSyncTime(): Promise<void> {
  await AsyncStorage.setItem(LAST_SYNC_KEY, new Date().toISOString());
}
