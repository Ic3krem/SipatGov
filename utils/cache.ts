import AsyncStorage from '@react-native-async-storage/async-storage';

interface CachedData<T> {
  data: T;
  timestamp: number;
}

const DEFAULT_TTL_MS = 60 * 60 * 1000; // 1 hour

/**
 * Fetch data with an AsyncStorage cache fallback.
 * On success, caches the result. On failure, returns cached data if available.
 */
export async function cachedFetch<T>(
  cacheKey: string,
  fetcher: () => Promise<T>,
  ttlMs: number = DEFAULT_TTL_MS,
): Promise<{ data: T; fromCache: boolean }> {
  try {
    const data = await fetcher();
    // Cache the successful result
    const cached: CachedData<T> = { data, timestamp: Date.now() };
    await AsyncStorage.setItem(cacheKey, JSON.stringify(cached));
    return { data, fromCache: false };
  } catch {
    // Try to return cached data
    const raw = await AsyncStorage.getItem(cacheKey);
    if (raw) {
      const cached: CachedData<T> = JSON.parse(raw);
      return { data: cached.data, fromCache: true };
    }
    throw new Error(`No data available (offline and no cache for ${cacheKey})`);
  }
}

/**
 * Get cached data without fetching, if available and not expired.
 */
export async function getCached<T>(
  cacheKey: string,
  ttlMs: number = DEFAULT_TTL_MS,
): Promise<T | null> {
  const raw = await AsyncStorage.getItem(cacheKey);
  if (!raw) return null;
  const cached: CachedData<T> = JSON.parse(raw);
  if (Date.now() - cached.timestamp > ttlMs) return null;
  return cached.data;
}

/**
 * Clear a specific cache entry.
 */
export async function clearCache(cacheKey: string): Promise<void> {
  await AsyncStorage.removeItem(cacheKey);
}
