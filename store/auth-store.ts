import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';

import { clearTokens, setTokens } from '@/services/api-client';
import type { User } from '@/types/models';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  setUser: (user: User) => void;
  login: (user: User, accessToken: string, refreshToken: string) => Promise<void>;
  logout: () => Promise<void>;
  setLoading: (loading: boolean) => void;
  loadStoredUser: () => Promise<void>;
}

const USER_STORAGE_KEY = 'sipatgov_user';

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  setUser: (user) => set({ user, isAuthenticated: true, error: null }),

  login: async (user, accessToken, refreshToken) => {
    await setTokens(accessToken, refreshToken);
    await AsyncStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    set({ user, isAuthenticated: true, error: null });
  },

  logout: async () => {
    await clearTokens();
    await AsyncStorage.removeItem(USER_STORAGE_KEY);
    set({ user: null, isAuthenticated: false, error: null });
  },

  setLoading: (loading) => set({ isLoading: loading }),

  loadStoredUser: async () => {
    try {
      const stored = await AsyncStorage.getItem(USER_STORAGE_KEY);
      if (stored) {
        let user: User;
        try {
          user = JSON.parse(stored) as User;
        } catch (parseError) {
          console.warn('Failed to parse stored user data, clearing corrupted entry:', parseError);
          await AsyncStorage.removeItem(USER_STORAGE_KEY);
          set({ isLoading: false, error: 'Corrupted user data was cleared. Please log in again.' });
          return;
        }
        set({ user, isAuthenticated: true, isLoading: false, error: null });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.warn('Failed to load stored user from AsyncStorage:', error);
      set({ isLoading: false, error: 'Failed to load user data.' });
    }
  },
}));
