import { create } from 'zustand';

interface DashboardState {
  selectedLguId: number | null;
  selectedFiscalYear: number;

  setSelectedLgu: (lguId: number | null) => void;
  setFiscalYear: (year: number) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  selectedLguId: null,
  selectedFiscalYear: new Date().getFullYear(),

  setSelectedLgu: (lguId) => set({ selectedLguId: lguId }),
  setFiscalYear: (year) => set({ selectedFiscalYear: year }),
}));
