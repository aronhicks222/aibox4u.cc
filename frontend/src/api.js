import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  register: (data) => apiClient.post('/auth/register', data),
  login: (data) => apiClient.post('/auth/login', data),
  getMe: () => apiClient.get('/auth/me'),
};

// Tools APIs
export const toolsAPI = {
  getAll: (params) => apiClient.get('/tools', { params }),
  getById: (id) => apiClient.get(`/tools/${id}`),
  create: (data) => apiClient.post('/tools', data),
  update: (id, data) => apiClient.put(`/tools/${id}`, data),
  delete: (id) => apiClient.delete(`/tools/${id}`),
};

// Submissions APIs
export const submissionsAPI = {
  create: (data) => apiClient.post('/submissions', data),
  getAll: () => apiClient.get('/submissions'),
  approve: (id) => apiClient.put(`/submissions/${id}/approve`),
};

// Favorites APIs
export const favoritesAPI = {
  getAll: () => apiClient.get('/favorites'),
  add: (toolId) => apiClient.post(`/favorites/${toolId}`),
  remove: (toolId) => apiClient.delete(`/favorites/${toolId}`),
};

// Categories API
export const categoriesAPI = {
  getAll: () => apiClient.get('/categories'),
};

export default apiClient;
