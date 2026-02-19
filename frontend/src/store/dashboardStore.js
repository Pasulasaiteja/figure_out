/**
 * Dashboard Store - Zustand
 */
import { create } from 'zustand'
import { userAPI } from '../services/api'

export const useDashboardStore = create((set) => ({
  stats: null,
  loading: false,
  error: null,

  fetchDashboard: async () => {
    set({ loading: true, error: null })
    try {
      const response = await userAPI.getDashboard()
      set({ stats: response.data, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },
}))
