/**
 * Zustand Global State Management
 */

import { create } from 'zustand';

export const useAppStore = create((set) => ({
  // Loading state
  isLoading: true,
  setLoading: (loading) => set({ isLoading: loading }),

  // Selected profile
  selectedProfile: null,
  setSelectedProfile: (profile) => set({ selectedProfile: profile }),

  // Current weight (real-time)
  currentWeight: 0,
  setCurrentWeight: (weight) => set({ currentWeight: weight }),

  // Last analysis result
  lastResult: null,
  setLastResult: (result) => set({ lastResult: result }),

  // Battery status
  batteryPercent: 100,
  setBatteryPercent: (percent) => set({ batteryPercent: percent }),

  // Settings
  settings: {
    wallpaper: null,
    soundEnabled: true,
    brightness: 100,
  },
  setSettings: (settings) => set({ settings }),
}));
