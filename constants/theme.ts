import { Platform } from 'react-native';

/**
 * SipatGov Brand Color System
 * ────────────────────────────
 * Derived from the shield logo palette:
 *   • Navy/Purple  — shield body, dark backgrounds
 *   • Red (#CE1126) — PH flag red, central figure
 *   • Blue (#0038A8) — PH flag blue, eye arc
 *   • Gold (#D4A843) — border accents, CTAs, highlights
 */
export const SipatColors = {
  // ── Brand (from logo) ─────────────────────────────
  navy: '#0A0E1A',          // deepest — splash/onboarding bg
  navyLight: '#1B2A5B',     // shield body upper
  navyMid: '#141832',       // cards on dark bg
  purple: '#2D1B4E',        // glow/ambient light
  red: '#CE1126',           // PH flag red / shield figure
  redLight: '#E8384F',      // lighter red for accents
  blue: '#0038A8',          // PH flag blue / eye arc
  blueLight: '#1E6FD9',     // interactive blue
  gold: '#D4A843',          // primary accent / CTAs
  goldLight: '#E8C96A',     // hover/highlight gold
  goldPale: '#FFF3CD',      // very light gold for badges

  // Aliases for backward compat — now navy instead of green
  primary: '#0A0E1A',
  primaryLight: '#1B2A5B',
  primaryDark: '#060810',
  accent: '#D4A843',
  accentLight: '#E8C96A',

  // ── Promise status ────────────────────────────────
  kept: '#2ECC71',
  broken: '#E74C3C',
  pending: '#F39C12',
  inProgress: '#3498DB',
  delayed: '#E67E22',
  partiallyKept: '#F1C40F',
  unverifiable: '#95A5A6',

  // ── Project status ────────────────────────────────
  planned: '#9B59B6',
  bidding: '#3498DB',
  awarded: '#2ECC71',
  ongoing: '#1ABC9C',
  completed: '#27AE60',
  cancelled: '#E74C3C',
  suspended: '#E67E22',

  // ── Onboarding (dark theme) ───────────────────────
  onboardingBg: '#0A0E1A',
  onboardingText: '#FFFFFF',
  onboardingAccent: '#D4A843',
  onboardingSubtext: '#8892A0',

  // ── Dashboard (light theme) ───────────────────────
  dashboardBg: '#F5F7FA',
  cardBg: '#FFFFFF',
  cardBorder: '#E8ECF1',
  sectionTitle: '#1B2A5B',    // navy instead of generic dark

  // ── Text hierarchy ────────────────────────────────
  textPrimary: '#0A0E1A',     // navy — ties text to brand
  textSecondary: '#5A6678',
  textMuted: '#9AA3B0',

  // ── Utility ───────────────────────────────────────
  success: '#2ECC71',
  warning: '#F39C12',
  error: '#E74C3C',
  info: '#1E6FD9',
} as const;

const tintColorLight = SipatColors.gold;
const tintColorDark = '#FFFFFF';

export const Colors = {
  light: {
    text: SipatColors.textPrimary,
    background: SipatColors.dashboardBg,
    tint: tintColorLight,
    icon: '#5A6678',
    tabIconDefault: '#8892A0',
    tabIconSelected: SipatColors.navy,
    card: SipatColors.cardBg,
    cardBorder: SipatColors.cardBorder,
  },
  dark: {
    text: '#ECEDEE',
    background: SipatColors.navy,
    tint: tintColorDark,
    icon: '#9BA1A6',
    tabIconDefault: '#5A6678',
    tabIconSelected: SipatColors.gold,
    card: SipatColors.navyMid,
    cardBorder: '#1E2040',
  },
};

// ── Typography Scale ──────────────────────────────────────
export const SipatTypography = {
  h1: { fontSize: 28, fontWeight: '700' as const, lineHeight: 34 },
  h2: { fontSize: 24, fontWeight: '700' as const, lineHeight: 30 },
  h3: { fontSize: 20, fontWeight: '600' as const, lineHeight: 26 },
  body: { fontSize: 15, fontWeight: '400' as const, lineHeight: 22 },
  bodySmall: { fontSize: 13, fontWeight: '400' as const, lineHeight: 18 },
  caption: { fontSize: 11, fontWeight: '400' as const, lineHeight: 16 },
  button: { fontSize: 15, fontWeight: '600' as const, lineHeight: 20 },
  tabLabel: { fontSize: 11, fontWeight: '500' as const, lineHeight: 14 },
};

// ── Spacing Scale ─────────────────────────────────────────
export const SipatSpacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  section: 32,
};

// ── Border Radius Scale ───────────────────────────────────
export const SipatRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  pill: 28,
  circle: 9999,
};

export const Fonts = Platform.select({
  ios: {
    sans: 'system-ui',
    serif: 'ui-serif',
    rounded: 'ui-rounded',
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
  web: {
    sans: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    serif: "Georgia, 'Times New Roman', serif",
    rounded: "'SF Pro Rounded', 'Hiragino Maru Gothic ProN', Meiryo, 'MS PGothic', sans-serif",
    mono: "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
  },
});
