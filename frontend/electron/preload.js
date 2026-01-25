/**
 * Electron Preload Script
 * Renderer process için güvenli API
 */

const { contextBridge } = require('electron');

// API'yi window.electron olarak expose et
contextBridge.exposeInMainWorld('electron', {
  platform: process.platform,
  isDev: process.env.NODE_ENV === 'development'
});
