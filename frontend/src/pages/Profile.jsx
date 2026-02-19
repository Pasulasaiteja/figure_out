import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { User, Mail, Award, Calendar, LogOut } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { userAPI, achievementAPI } from '../services/api'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

const Profile = () => {
  const { user, logout, updateUser } = useAuthStore()
  const navigate = useNavigate()
  const [editing, setEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [achievements, setAchievements] = useState([])
  const [formData, setFormData] = useState({
    name: user?.name || '',
    age: user?.age || '',
    weight: user?.weight || '',
    height: user?.height || '',
    gender: user?.gender || '',
  })

  useEffect(() => {
    fetchAchievements()
  }, [])

  const fetchAchievements = async () => {
    try {
      const response = await achievementAPI.getMy()
      setAchievements(response.data)
    } catch (error) {
      console.error('Failed to load achievements')
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await userAPI.updateProfile(formData)
      updateUser(response.data)
      toast.success('Profile updated successfully!')
      setEditing(false)
    } catch (error) {
      toast.error('Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/')
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Profile Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-8"
      >
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-purple-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {user?.name?.[0]?.toUpperCase()}
            </div>
            <div>
              <h1 className="text-3xl font-bold">{user?.name}</h1>
              <p className="text-gray-600 dark:text-gray-400 flex items-center gap-2">
                <Mail size={16} />
                {user?.email}
              </p>
              <p className="text-sm text-gray-500 flex items-center gap-2 mt-1">
                <Calendar size={14} />
                Joined {new Date(user?.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="btn-secondary flex items-center gap-2 text-red-600 dark:text-red-400"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="text-center">
            <p className="text-2xl font-bold text-primary-600">{user?.workout_streak}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Day Streak</p>
          </div>
          <div className="text-center border-l border-r border-gray-300 dark:border-gray-600">
            <p className="text-2xl font-bold text-orange-600">{user?.total_calories_burned}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Calories Burned</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-pink-600">₹{user?.charity_contribution}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Charity Impact</p>
          </div>
        </div>
      </motion.div>

      {/* Profile Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-8"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <User size={24} />
            Profile Information
          </h2>
          <button
            onClick={() => setEditing(!editing)}
            className="btn-secondary"
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {editing ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="input"
                required
              />
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="label">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="input"
                  min="13"
                  max="120"
                />
              </div>

              <div>
                <label className="label">Weight (kg)</label>
                <input
                  type="number"
                  name="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  className="input"
                  min="30"
                  max="300"
                />
              </div>

              <div>
                <label className="label">Height (cm)</label>
                <input
                  type="number"
                  name="height"
                  value={formData.height}
                  onChange={handleChange}
                  className="input"
                  min="100"
                  max="250"
                />
              </div>
            </div>

            <div>
              <label className="label">Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="input"
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        ) : (
          <div className="space-y-4">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Age</p>
                <p className="text-lg font-medium">{user?.age || 'Not set'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Gender</p>
                <p className="text-lg font-medium">{user?.gender || 'Not set'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Weight</p>
                <p className="text-lg font-medium">{user?.weight ? `${user.weight} kg` : 'Not set'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Height</p>
                <p className="text-lg font-medium">{user?.height ? `${user.height} cm` : 'Not set'}</p>
              </div>
            </div>
          </div>
        )}
      </motion.div>

      {/* Achievements */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-8"
      >
        <h2 className="text-2xl font-bold flex items-center gap-2 mb-6">
          <Award size={24} />
          Achievements ({achievements.length})
        </h2>

        {achievements.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {achievements.map((userAch) => (
              <div
                key={userAch.id}
                className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-lg border-2 border-yellow-200 dark:border-yellow-700"
              >
                <div className="text-4xl mb-2">{userAch.achievement.badge_icon}</div>
                <h3 className="font-bold mb-1">{userAch.achievement.name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {userAch.achievement.description}
                </p>
                <p className="text-xs text-gray-500 mt-2">
                  Unlocked {new Date(userAch.unlocked_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <Award size={48} className="mx-auto mb-3 opacity-50" />
            <p>No achievements yet. Keep working out to unlock them!</p>
          </div>
        )}
      </motion.div>
    </div>
  )
}

export default Profile
