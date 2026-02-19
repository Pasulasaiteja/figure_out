import { Menu, Moon, Sun, Bell, User } from 'lucide-react'
import { useThemeStore } from '../store/themeStore'
import { useAuthStore } from '../store/authStore'
import { Link } from 'react-router-dom'

const Navbar = ({ onMenuClick }) => {
  const { theme, toggleTheme } = useThemeStore()
  const { user } = useAuthStore()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            <Menu size={24} />
          </button>
          
          <Link to="/dashboard" className="flex items-center gap-2">
            <div className="w-8 h-8 gradient-primary rounded-lg flex items-center justify-center text-white font-bold">
              T
            </div>
            <span className="font-bold text-xl">Transformers</span>
          </Link>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={toggleTheme}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
          
          <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg relative">
            <Bell size={20} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          
          <Link
            to="/profile"
            className="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center text-white">
              {user?.name?.[0]?.toUpperCase() || <User size={16} />}
            </div>
            <span className="hidden md:block font-medium">{user?.name}</span>
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
