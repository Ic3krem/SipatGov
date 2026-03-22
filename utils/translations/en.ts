export const en = {
  // Splash
  splash: {
    tagline: 'Civic Transparency Platform',
  },

  // Language selection
  languageSelect: {
    title: 'Choose Your Language',
    subtitle: 'Pumili ng Wika',
  },

  // Onboarding
  onboarding: {
    step1Title: 'Welcome to',
    step1Subtitle: 'SipatGov',
    step1Body: 'A civic-tech platform for government transparency and accountability.',
    step2Title: 'Your time to',
    step2Subtitle: 'Observe',
    step2Body: 'Track LGU budgets, projects, and promises in real-time.',
    step3Title: 'Become an',
    step3Subtitle: 'Advocate',
    step3Body: 'Report issues, verify promises, and hold officials accountable.',
    step4Title: 'Observe the',
    step4Subtitle: 'Government',
    step4Body: 'Together, we build a more transparent Philippines.',
    skip: 'Skip',
    next: 'Next',
    getStarted: 'Get Started',
  },

  // Tabs
  tabs: {
    dashboard: 'Home',
    accountability: 'Sipat',
    projects: 'Projects',
    reports: 'Reports',
    profile: 'Profile',
  },

  // Dashboard
  dashboard: {
    title: 'Dashboard',
    cta: 'OBSERVE THE GOVERNMENT',
    promisesKept: 'Kept',
    promisesBroken: 'Broken',
    promisesPending: 'Pending',
    promisesInProgress: 'In Progress',
    totalProjects: 'Total Projects',
    totalReports: 'Reports',
    offlineBanner: 'Offline — showing cached data',
  },

  // Accountability
  accountability: {
    title: 'Accountability',
    selectLgu: 'Select LGU',
    promiseSummary: 'Promise Summary',
    recentPromises: 'Recent Promises',
    viewAll: 'View All',
    noData: 'No data available for this LGU.',
  },

  // Projects
  projects: {
    title: 'Projects',
    searchPlaceholder: 'Search projects...',
    allFilter: 'All',
    projectCount: 'Projects',
    noResults: 'No projects found matching your search.',
    budget: 'Budget',
    contractor: 'Contractor',
    progress: 'Progress',
    ongoing: 'Ongoing',
    completed: 'Completed',
    bidding: 'Bidding',
    delayed: 'Delayed',
    planned: 'Planned',
  },

  // Reports
  reports: {
    title: 'Community Reports',
    newReport: 'New Report',
    submitReport: 'Submit Report',
    reportTitle: 'Title',
    reportTitlePlaceholder: 'Enter a brief title',
    reportDescription: 'Description',
    reportDescriptionPlaceholder: 'Describe the issue or update in detail...',
    reportType: 'Report Type',
    anonymous: 'Submit anonymously',
    submit: 'Submit',
    cancel: 'Cancel',
    all: 'All',
    concerns: 'Concerns',
    tips: 'Tips',
    updates: 'Updates',
    noReports: 'No reports yet',
    noReportsBody: 'Be the first to report an issue or share an update.',
    reportCount: 'reports',
    upvotes: 'upvotes',
    anonymousUser: 'Anonymous',
    concern: 'Concern',
    feedback: 'Feedback',
    corruption_tip: 'Corruption Tip',
    progress_update: 'Progress Update',
    delay_report: 'Delay Report',
    selectType: 'Select report type',
    titleRequired: 'Title is required',
    descriptionRequired: 'Description is required',
    typeRequired: 'Report type is required',
  },

  // Profile
  profile: {
    title: 'Profile',
    editProfile: 'Edit Profile',
    citizen: 'Citizen',
    moderator: 'Moderator',
    admin: 'Admin',
    statsReports: 'Reports Filed',
    statsUpvotes: 'Upvotes Given',
    statsDaysActive: 'Days Active',
    settingsTitle: 'Settings',
    language: 'Language',
    languageEn: 'English',
    languageTl: 'Tagalog',
    region: 'Home Region',
    regionSelect: 'Select Region',
    notifications: 'Notifications',
    darkMode: 'Dark Mode',
    about: 'About SipatGov',
    version: 'Version',
    logout: 'Log Out',
    logoutConfirm: 'Are you sure you want to log out?',
  },

  // Common
  common: {
    loading: 'Loading...',
    error: 'Something went wrong',
    retry: 'Retry',
    comingSoon: 'Coming Soon',
    comingSoonBody: 'This feature is under development.',
  },
};

// Use a structural type so translations in other languages can have different string values
interface TranslationSection {
  [key: string]: string;
}

export interface TranslationKeys {
  splash: TranslationSection;
  languageSelect: TranslationSection;
  onboarding: TranslationSection;
  tabs: TranslationSection;
  dashboard: TranslationSection;
  accountability: TranslationSection;
  projects: TranslationSection;
  reports: TranslationSection;
  profile: TranslationSection;
  common: TranslationSection;
}
