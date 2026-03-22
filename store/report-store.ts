import { create } from 'zustand';

import type { CreateReportRequest } from '@/types/api';

interface ReportDraft extends Partial<CreateReportRequest> {
  photos: string[]; // local URIs
}

interface ReportState {
  draft: ReportDraft;
  pendingReports: CreateReportRequest[]; // queued for offline sync

  updateDraft: (updates: Partial<ReportDraft>) => void;
  addPhoto: (uri: string) => void;
  removePhoto: (uri: string) => void;
  clearDraft: () => void;
  queueReport: (report: CreateReportRequest) => void;
  dequeueReport: (index: number) => void;
}

const emptyDraft: ReportDraft = {
  photos: [],
};

export const useReportStore = create<ReportState>((set) => ({
  draft: { ...emptyDraft },
  pendingReports: [],

  updateDraft: (updates) =>
    set((state) => ({
      draft: { ...state.draft, ...updates },
    })),

  addPhoto: (uri) =>
    set((state) => ({
      draft: { ...state.draft, photos: [...state.draft.photos, uri] },
    })),

  removePhoto: (uri) =>
    set((state) => ({
      draft: {
        ...state.draft,
        photos: state.draft.photos.filter((p) => p !== uri),
      },
    })),

  clearDraft: () => set({ draft: { ...emptyDraft } }),

  queueReport: (report) =>
    set((state) => ({
      pendingReports: [...state.pendingReports, report],
    })),

  dequeueReport: (index) =>
    set((state) => ({
      pendingReports: state.pendingReports.filter((_, i) => i !== index),
    })),
}));
