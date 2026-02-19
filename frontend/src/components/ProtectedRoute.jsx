import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, token, authChecked } = useAuthStore()

  // Show loading while checking auth
  if (!authChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-dark-bg">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated || !token) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
