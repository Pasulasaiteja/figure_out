import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Activity, 
  Apple, 
  TrendingUp, 
  User, 
  ClipboardCheck,
  LogOut
} from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { motion } from 'framer-motion'

const Sidebar = ({ isOpen }) => {
  const { logout } = useAuthStore()

  const navItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/assessment', icon: ClipboardCheck, label: 'Health Check' },
    { to: '/workout', icon: Activity, label: 'Workouts' },
    { to: '/nutrition', icon: Apple, label: 'Nutrition' },
    { to: '/progress', icon: TrendingUp, label: 'Progress' },
    { to: '/profile', icon: User, label: 'Profile' },
  ]

  return (
    <motion.aside
      initial={{ x: -260 }}
      animate={{ x: isOpen ? 0 : -260 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-16 bottom-0 w-64 bg-white dark:bg-dark-card border-r border-gray-200 dark:border-dark-border overflow-y-auto z-40"
    >
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`
            }
          >
            <item.icon size={20} />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}

        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 transition-colors"
        >
          <LogOut size={20} />
          <span className="font-medium">Logout</span>
        </button>
      </nav>
    </motion.aside>
  )
}

export default Sidebar
