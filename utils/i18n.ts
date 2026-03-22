import { en, type TranslationKeys } from './translations/en';
import { tl } from './translations/tl';

export type Language = 'en' | 'tl';

const translations: Record<Language, TranslationKeys> = { en, tl };

/**
 * Get the full translation object for a language.
 */
export function getTranslations(lang: Language): TranslationKeys {
  return translations[lang];
}

/**
 * Get a nested translation value by dot-separated key path.
 * e.g., t('onboarding.step1Title', 'tl') -> 'Buksan ang'
 */
export function t(keyPath: string, lang: Language): string {
  const keys = keyPath.split('.');
  let result: unknown = translations[lang];
  for (const key of keys) {
    if (result && typeof result === 'object' && key in result) {
      result = (result as Record<string, unknown>)[key];
    } else {
      // Fallback to English
      result = translations.en;
      for (const fallbackKey of keys) {
        if (result && typeof result === 'object' && fallbackKey in result) {
          result = (result as Record<string, unknown>)[fallbackKey];
        } else {
          return keyPath; // Return key path if not found
        }
      }
      break;
    }
  }
  return typeof result === 'string' ? result : keyPath;
}
