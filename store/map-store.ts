import { create } from 'zustand';

interface MapFilters {
  category: string | null;
  status: string | null;
  fiscalYear: number | null;
}

interface MapState {
  filters: MapFilters;
  selectedMarkerId: number | null;

  setFilter: (key: keyof MapFilters, value: string | number | null) => void;
  clearFilters: () => void;
  setSelectedMarker: (id: number | null) => void;
}

const defaultFilters: MapFilters = {
  category: null,
  status: null,
  fiscalYear: null,
};

export const useMapStore = create<MapState>((set) => ({
  filters: { ...defaultFilters },
  selectedMarkerId: null,

  setFilter: (key, value) =>
    set((state) => ({
      filters: { ...state.filters, [key]: value },
    })),

  clearFilters: () => set({ filters: { ...defaultFilters } }),

  setSelectedMarker: (id) => set({ selectedMarkerId: id }),
}));
