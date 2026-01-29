/**
 * Backend API Service
 * Tüm HTTP ve WebSocket iletişimi
 */

import axios from 'axios';

// Backend API URL - Raspberry Pi'de aynı makinede çalışıyor
const API_BASE_URL =  'http://127.0.0.1:8000';

// Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 saniye - AI analizi uzun sürebilir
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== HEALTH ====================

export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

// ==================== SCALE ====================

export const getWeight = async () => {
  const response = await api.get('/api/scale/weight');
  return response.data.weight;
};

export const tareScale = async () => {
  const response = await api.post('/api/scale/tare');
  return response.data;
};

// WebSocket için ağırlık stream'i
export const connectWeightStream = (onWeightUpdate) => {
  const ws = new WebSocket(`ws://127.0.0.1:8000/ws/weight`);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onWeightUpdate(data.weight);
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
};

// ==================== CAMERA ====================

export const captureImage = async () => {
  const response = await api.get('/api/camera/capture', {
    responseType: 'blob'
  });
  return URL.createObjectURL(response.data);
};

export const startCameraPreview = async () => {
  const response = await api.post('/api/camera/preview/start');
  return response.data;
};

export const stopCameraPreview = async () => {
  const response = await api.post('/api/camera/preview/stop');
  return response.data;
};

// ==================== AI & ANALYSIS ====================

export const analyzeFood = async (weight, profileId = null) => {
  const response = await api.post('/api/analyze', {
    weight,
    profile_id: profileId
  });
  return response.data;
};

export const testModel = async (imageBlob) => {
  const formData = new FormData();
  formData.append('file', imageBlob, 'captured.jpg');
  
  const response = await api.post('/api/model-test', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const scanComplete = async (plateId = null) => {
  const response = await api.post('/api/scan-complete', {
    plate_id: plateId
  });
  return response.data;
};

// ==================== PLATES ====================

export const getPlates = async () => {
  const response = await api.get('/api/plates');
  return response.data.plates;
};

export const createPlate = async (plateData) => {
  const response = await api.post('/api/plates', plateData);
  return response.data;
};

export const deletePlate = async (plateId) => {
  const response = await api.delete(`/api/plates/${plateId}`);
  return response.data;
};

// ==================== PROFILES ====================

export const getProfiles = async () => {
  const response = await api.get('/api/profiles');
  return response.data.profiles;
};

export const createProfile = async (profileData) => {
  const response = await api.post('/api/profiles', profileData);
  return response.data;
};

export const updateProfile = async (profileId, profileData) => {
  const response = await api.put(`/api/profiles/${profileId}`, profileData);
  return response.data;
};

export const deleteProfile = async (profileId) => {
  const response = await api.delete(`/api/profiles/${profileId}`);
  return response.data;
};

export const getProfileHistory = async (profileId) => {
  const response = await api.get(`/api/profiles/${profileId}/history`);
  return response.data;
};

// ==================== MEASUREMENTS ====================

export const saveMeasurement = async (measurementData) => {
  const response = await api.post('/api/measurements', measurementData);
  return response.data;
};

export const getMeasurements = async () => {
  const response = await api.get('/api/measurements');
  return response.data.measurements;
};

// ==================== SETTINGS ====================

export const getSettings = async () => {
  const response = await api.get('/api/settings');
  return response.data;
};

export const setWallpaper = async (wallpaperName) => {
  const response = await api.post('/api/settings/wallpaper', {
    name: wallpaperName
  });
  return response.data;
};

// ==================== HARDWARE CONTROL ====================

export const controlLED = async (color) => {
  const response = await api.post(`/api/led/${color}`);
  return response.data;
};

export const playSound = async (sound) => {
  const response = await api.post(`/api/speaker/${sound}`);
  return response.data;
};

export const getBattery = async () => {
  const response = await api.get('/api/battery');
  return response.data;
};

export default api;
