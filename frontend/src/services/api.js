/**
 * API Service - Axios configuration and API calls
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', new URLSearchParams(data), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getMe: () => api.get('/api/auth/me'),
}

// User APIs
export const userAPI = {
  getProfile: () => api.get('/api/users/profile'),
  updateProfile: (data) => api.put('/api/users/profile', data),
  getDashboard: () => api.get('/api/users/dashboard'),
}

// Health Assessment APIs
export const assessmentAPI = {
  create: (data) => api.post('/api/assessment/', data),
  get: () => api.get('/api/assessment/'),
  update: (data) => api.put('/api/assessment/', data),
}

// Workout APIs
export const workoutAPI = {
  generate: () => api.post('/api/workout/generate'),
  getCurrent: () => api.get('/api/workout/current'),
  getDay: (day) => api.get(`/api/workout/day/${day}`),
  complete: (data) => api.post('/api/workout/complete', data),
}

// Nutrition APIs
export const nutritionAPI = {
  generate: () => api.post('/api/nutrition/generate'),
  getCurrent: () => api.get('/api/nutrition/current'),
  getDay: (day) => api.get(`/api/nutrition/day/${day}`),
  getGroceryList: () => api.get('/api/nutrition/grocery-list'),
}

// Progress APIs
export const progressAPI = {
  create: (data) => api.post('/api/progress/', data),
  getRecords: (days = 30) => api.get(`/api/progress/?days=${days}`),
  getSummary: (days = 30) => api.get(`/api/progress/summary?days=${days}`),
  getCharts: (days = 30) => api.get(`/api/progress/charts?days=${days}`),
  seed: () => api.post('/api/progress/seed'),
}

// Chat APIs
export const chatAPI = {
  send: (data) => api.post('/api/chat/', data),
  getSessions: () => api.get('/api/chat/sessions'),
  getSession: (sessionId) => api.get(`/api/chat/session/${sessionId}`),
  deleteSession: (sessionId) => api.delete(`/api/chat/session/${sessionId}`),
}

// Calendar APIs
export const calendarAPI = {
  getAuthUrl: () => api.get('/api/calendar/auth-url'),
  sync: (data) => api.post('/api/calendar/sync', data),
  getEvents: () => api.get('/api/calendar/events'),
  disconnect: () => api.delete('/api/calendar/disconnect'),
}

// Achievement APIs
export const achievementAPI = {
  getAll: () => api.get('/api/achievements/'),
  getMy: () => api.get('/api/achievements/my'),
  check: () => api.get('/api/achievements/check'),
  markViewed: (id) => api.post(`/api/achievements/mark-viewed/${id}`),
  seed: () => api.post('/api/achievements/seed'),
}

export default api
