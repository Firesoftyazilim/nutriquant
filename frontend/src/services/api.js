/**
 * Backend API Service
 * Tüm HTTP ve WebSocket iletişimi
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
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
  const ws = new WebSocket(`ws://localhost:8000/ws/weight`);
  
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
