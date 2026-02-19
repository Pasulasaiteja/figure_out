/**
 * Auth Store - Zustand
 */
import { create } from 'zustand'
import { authAPI, userAPI } from '../services/api'

// Check initial auth state
const initialToken = localStorage.getItem('token')
const initialUser = localStorage.getItem('user')
let parsedUser = null
try {
  parsedUser = initialUser ? JSON.parse(initialUser) : null
} catch (e) {
  parsedUser = null
}

export const useAuthStore = create((set) => ({
  user: parsedUser,
  token: initialToken,
  isAuthenticated: !!(initialToken && parsedUser),
  loading: false,
  authChecked: !!(initialToken && parsedUser),
  error: null,

  register: async (data) => {
    set({ loading: true, error: null })
    try {
      const response = await authAPI.register(data)
      const { access_token, user } = response.data
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      set({
        user,
        token: access_token,
        isAuthenticated: true,
        loading: false,
      })
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      set({ error: message, loading: false })
      return { success: false, error: message }
    }
  },

  login: async (email, password) => {
    set({ loading: true, error: null })
    try {
      const response = await authAPI.login({ username: email, password })
      const { access_token, user } = response.data
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      set({
        user,
        token: access_token,
        isAuthenticated: true,
        loading: false,
      })
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      set({ error: message, loading: false })
      return { success: false, error: message }
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  checkAuth: async () => {
    const token = localStorage.getItem('token')
    const userStr = localStorage.getItem('user')
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr)
        set({
          user,
          token,
          isAuthenticated: true,
          authChecked: true,
        })
      } catch (error) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          authChecked: true,
        })
      }
    } else {
      set({ authChecked: true })
    }
  },

  updateUser: (userData) => {
    set({ user: userData })
    localStorage.setItem('user', JSON.stringify(userData))
  },
}))
