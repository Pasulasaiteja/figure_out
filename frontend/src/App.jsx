import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './store/authStore'
import { useThemeStore } from './store/themeStore'
import { useEffect } from 'react'

// Pages
import Landing from './pages/Landing'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import HealthAssessment from './pages/HealthAssessment'
import Workout from './pages/Workout'
import Nutrition from './pages/Nutrition'
import Progress from './pages/Progress'
import Profile from './pages/Profile'
import Health from './pages/Health'

// Components
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import AromiChat from './components/AromiChat'

function App() {
  const { theme } = useThemeStore()
  const { checkAuth } = useAuthStore()

  useEffect(() => {
    // Apply theme
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [theme])

  useEffect(() => {
    // Check authentication on mount
    checkAuth()
  }, [checkAuth])

  return (
    <Router>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: theme === 'dark' ? '#1e293b' : '#fff',
            color: theme === 'dark' ? '#fff' : '#000',
          },
        }}
      />
      
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        
        {/* Protected Routes */}
        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/assessment" element={<HealthAssessment />} />
          <Route path="/workout" element={<Workout />} />
          <Route path="/nutrition" element={<Nutrition />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/health" element={<Health />} />
        </Route>
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      
      {/* AROMI Floating AI Coach */}
      <AromiChat />
    </Router>
  )
}

export default App
