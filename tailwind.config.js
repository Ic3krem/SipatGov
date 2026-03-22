/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        sipat: {
          // Brand (from shield logo)
          navy: '#0A0E1A',
          'navy-light': '#1B2A5B',
          'navy-mid': '#141832',
          purple: '#2D1B4E',
          red: '#CE1126',
          'red-light': '#E8384F',
          blue: '#0038A8',
          'blue-light': '#1E6FD9',
          gold: '#D4A843',
          'gold-light': '#E8C96A',
          'gold-pale': '#FFF3CD',

          // Backward compat aliases
          primary: '#0A0E1A',
          'primary-light': '#1B2A5B',
          'primary-dark': '#060810',
          accent: '#D4A843',
          'accent-light': '#E8C96A',

          // Promise status
          kept: '#2ECC71',
          broken: '#E74C3C',
          pending: '#F39C12',
          'in-progress': '#3498DB',
          delayed: '#E67E22',
          'partially-kept': '#F1C40F',
          unverifiable: '#95A5A6',

          // Surfaces
          'onboarding-bg': '#0A0E1A',
          'onboarding-sub': '#8892A0',
          'dashboard-bg': '#F5F7FA',
          card: '#FFFFFF',
          'card-border': '#E8ECF1',
          'section-title': '#1B2A5B',

          // Text
          'text-primary': '#0A0E1A',
          'text-secondary': '#5A6678',
          'text-muted': '#9AA3B0',
        },
      },
    },
  },
  plugins: [],
};
