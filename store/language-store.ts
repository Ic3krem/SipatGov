import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';

import type { Language } from '@/utils/i18n';

const LANGUAGE_KEY = 'sipatgov_language';

interface LanguageState {
  language: Language | null; // null = not yet selected
  isLoaded: boolean;
  setLanguage: (lang: Language) => Promise<void>;
  loadLanguage: () => Promise<void>;
}

export const useLanguageStore = create<LanguageState>((set) => ({
  language: null,
  isLoaded: false,

  setLanguage: async (lang: Language) => {
    await AsyncStorage.setItem(LANGUAGE_KEY, lang);
    set({ language: lang });
  },

  loadLanguage: async () => {
    try {
      const stored = await AsyncStorage.getItem(LANGUAGE_KEY);
      set({
        language: (stored as Language) || null,
        isLoaded: true,
      });
    } catch {
      // AsyncStorage may fail on first run — proceed without stored language
      set({ language: null, isLoaded: true });
    }
  },
}));
