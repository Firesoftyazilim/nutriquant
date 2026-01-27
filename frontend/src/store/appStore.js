/**
 * Zustand Global State Management
 */

import { create } from 'zustand';

// LocalStorage'dan wallpaper'ı yükle
const loadWallpaper = () => {
  try {
    return localStorage.getItem('nutriquant_wallpaper') || 'default';
  } catch {
    return 'default';
  }
};

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

  // Wallpaper
  currentWallpaper: loadWallpaper(),
  setCurrentWallpaper: (wallpaper) => {
    localStorage.setItem('nutriquant_wallpaper', wallpaper);
    set({ currentWallpaper: wallpaper });
  },
}));
