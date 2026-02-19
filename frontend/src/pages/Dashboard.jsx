import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Flame, TrendingUp, Calendar, Heart, Plus, Activity } from 'lucide-react'
import { useDashboardStore } from '../store/dashboardStore'
import { useAuthStore } from '../store/authStore'
import { assessmentAPI } from '../services/api'
import toast from 'react-hot-toast'

const Dashboard = () => {
  const { stats, loading, fetchDashboard } = useDashboardStore()
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const [hasAssessment, setHasAssessment] = useState(false)
  const [checkingAssessment, setCheckingAssessment] = useState(true)

  useEffect(() => {
    fetchDashboard()
    checkAssessment()
  }, [])

  const checkAssessment = async () => {
    try {
      await assessmentAPI.get()
      setHasAssessment(true)
    } catch (error) {
      setHasAssessment(false)
    } finally {
      setCheckingAssessment(false)
    }
  }

  const statCards = [
    {
      title: 'Workout Streak',
      value: stats?.workout_streak || 0,
      unit: 'days',
      icon: Flame,
      color: 'text-orange-500',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
    },
    {
      title: 'Calories Burned',
      value: stats?.total_calories_burned || 0,
      unit: 'kcal',
      icon: TrendingUp,
      color: 'text-green-500',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'Charity Impact',
      value: stats?.charity_contribution || 0,
      unit: '₹',
      icon: Heart,
      color: 'text-pink-500',
      bgColor: 'bg-pink-50 dark:bg-pink-900/20',
    },
    {
      title: 'Completed Today',
      value: stats?.completed_today || 0,
      unit: 'workouts',
      icon: Activity,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    },
  ]

  if (checkingAssessment || loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!hasAssessment) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl mx-auto text-center py-16"
      >
        <div className="card p-8">
          <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center text-white mx-auto mb-4">
            <Activity size={32} />
          </div>
          <h2 className="text-2xl font-bold mb-4">Complete Your Health Assessment</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Before we can create your personalized fitness plan, we need to know more about you.
            This quick 12-question assessment will help us tailor everything to your needs.
          </p>
          <button
            onClick={() => navigate('/assessment')}
            className="btn-primary"
          >
            Start Assessment
          </button>
        </div>
      </motion.div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">
          Welcome back, {user?.name}! 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Here's your fitness overview
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="card card-hover p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={stat.color} size={24} />
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              {stat.title}
            </p>
            <p className="text-2xl font-bold">
              {stat.value} <span className="text-sm font-normal">{stat.unit}</span>
            </p>
          </motion.div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Workout Plan */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6"
        >
          <h3 className="text-xl font-bold mb-4">Workout Plan</h3>
          {stats?.has_active_plan ? (
            <>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Your personalized 7-day plan is ready
              </p>
              <button
                onClick={() => navigate('/workout')}
                className="btn-primary"
              >
                View Workouts
              </button>
            </>
          ) : (
            <>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Generate your AI-powered workout plan
              </p>
              <button
                onClick={() => navigate('/workout')}
                className="btn-primary"
              >
                <Plus size={20} className="inline mr-2" />
                Generate Plan
              </button>
            </>
          )}
        </motion.div>

        {/* Upcoming Sessions */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6"
        >
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Calendar size={20} />
            Upcoming Sessions
          </h3>
          {stats?.upcoming_sessions && stats.upcoming_sessions.length > 0 ? (
            <div className="space-y-3">
              {stats.upcoming_sessions.map((session, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-3 bg-gray-50 dark:bg-dark-bg rounded-lg"
                >
                  <div>
                    <p className="font-medium">{session.title}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {new Date(session.start_time).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 dark:text-gray-400">
              No upcoming sessions scheduled
            </p>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard
