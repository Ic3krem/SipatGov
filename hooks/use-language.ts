import { useCallback } from 'react';

import { useLanguageStore } from '@/store/language-store';
import { getTranslations, type Language } from '@/utils/i18n';

/**
 * Hook for accessing translations in the current language.
 * Returns the full translation object and the current language.
 */
export function useLanguage() {
  const language = useLanguageStore((s) => s.language);
  const setLanguage = useLanguageStore((s) => s.setLanguage);

  // Default to Tagalog if no language selected yet
  const currentLang: Language = language ?? 'tl';
  const translations = getTranslations(currentLang);

  const toggleLanguage = useCallback(async () => {
    await setLanguage(currentLang === 'en' ? 'tl' : 'en');
  }, [currentLang, setLanguage]);

  return {
    lang: currentLang,
    t: translations,
    setLanguage,
    toggleLanguage,
    isLanguageSelected: language !== null,
  };
}
