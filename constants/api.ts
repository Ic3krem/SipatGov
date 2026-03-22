import { Platform } from 'react-native';

// Android emulator uses 10.0.2.2 to reach host machine's localhost
const DEV_HOST = Platform.OS === 'android' ? '10.0.2.2' : 'localhost';

export const API_BASE_URL = __DEV__
  ? `http://${DEV_HOST}:8000/api/v1`
  : 'https://api.sipatgov.ph/api/v1';

export const ENDPOINTS = {
  // Auth
  AUTH_REGISTER: '/auth/register',
  AUTH_LOGIN: '/auth/login',
  AUTH_REFRESH: '/auth/refresh',
  AUTH_ME: '/auth/me',
  AUTH_ONBOARDING: '/auth/me/onboarding',

  // Regions
  REGIONS: '/regions',
  PROVINCES: (regionId: number) => `/regions/${regionId}/provinces`,
  LGUS_BY_PROVINCE: (provinceId: number) => `/regions/provinces/${provinceId}/lgus`,

  // LGUs
  LGUS: '/lgus',
  LGU_DETAIL: (id: number) => `/lgus/${id}`,
  LGU_SUMMARY: (id: number) => `/lgus/${id}/summary`,
  LGUS_MAP: '/lgus/map',

  // Projects
  PROJECTS: '/projects',
  PROJECT_DETAIL: (id: number) => `/projects/${id}`,
  PROJECTS_MAP: '/projects/map',

  // Budgets
  BUDGETS: '/budgets',
  BUDGETS_SUMMARY: '/budgets/summary',

  // Promises
  PROMISES: '/promises',
  PROMISE_DETAIL: (id: number) => `/promises/${id}`,
  PROMISES_STATS: '/promises/stats',

  // Reports
  REPORTS: '/reports',
  REPORT_DETAIL: (id: number) => `/reports/${id}`,
  REPORT_UPVOTE: (id: number) => `/reports/${id}/upvote`,

  // Documents
  DOCUMENTS: '/documents',
  DOCUMENT_DETAIL: (id: number) => `/documents/${id}`,

  // Dashboard
  DASHBOARD: '/dashboard',
  DASHBOARD_NATIONAL: '/dashboard/national',

  // Search
  SEARCH: '/search',
} as const;
