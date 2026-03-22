import { useCallback, useEffect, useState } from 'react';

import {
  getHomeLguId,
  getHomeRegionId,
  isOnboardingCompleted,
  setHomeLguId,
  setHomeRegionId,
  setOnboardingCompleted,
} from '@/utils/storage';

export function useOnboarding() {
  const [isComplete, setIsComplete] = useState<boolean | null>(null);
  const [selectedLguId, setSelectedLguId] = useState<number | null>(null);
  const [selectedRegionId, setSelectedRegionId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const completed = await isOnboardingCompleted();
        const lguId = await getHomeLguId();
        const regionId = await getHomeRegionId();
        setIsComplete(completed);
        setSelectedLguId(lguId);
        setSelectedRegionId(regionId);
      } catch (error) {
        console.warn('Failed to load onboarding state from AsyncStorage:', error);
        setIsComplete(false);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  const markComplete = useCallback(async (lguId: number, regionId: number) => {
    try {
      await setOnboardingCompleted(true);
      await setHomeLguId(lguId);
      await setHomeRegionId(regionId);
      setIsComplete(true);
      setSelectedLguId(lguId);
      setSelectedRegionId(regionId);
    } catch (error) {
      console.warn('Failed to save onboarding state to AsyncStorage:', error);
    }
  }, []);

  return {
    isComplete,
    isLoading,
    selectedLguId,
    selectedRegionId,
    markComplete,
  };
}
