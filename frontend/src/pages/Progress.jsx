import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, Flame, Activity, Weight, Plus, X, BarChart3 } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { progressAPI } from '../services/api'
import toast from 'react-hot-toast'

const Progress = () => {
  const [summary, setSummary] = useState(null)
  const [chartData, setChartData] = useState(null)
  const [timeRange, setTimeRange] = useState(30)
  const [loading, setLoading] = useState(true)
  const [seeding, setSeeding] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [formData, setFormData] = useState({
    weight: '',
    calories_burned: '',
    workout_completed: 1,
    workout_duration: '',
    calories_consumed: '',
    water_intake: '',
    sleep_hours: '',
    energy_level: 'Medium',
    mood: 'Good',
    notes: ''
  })

  useEffect(() => {
    fetchData()
  }, [timeRange])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [summaryRes, chartsRes] = await Promise.all([
        progressAPI.getSummary(timeRange),
        progressAPI.getCharts(timeRange),
      ])
      setSummary(summaryRes.data)
      setChartData(chartsRes.data)
    } catch (error) {
      toast.error('Failed to load progress data')
    } finally {
      setLoading(false)
    }
  }

  const generateSampleData = async () => {
    setSeeding(true)
    try {
      await progressAPI.seed()
      toast.success('Sample progress data generated!')
      fetchData()
    } catch (error) {
      toast.error('Failed to generate sample data')
    } finally {
      setSeeding(false)
    }
  }

  const handleFormChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    
    try {
      const data = {
        weight: formData.weight ? parseFloat(formData.weight) : null,
        calories_burned: parseInt(formData.calories_burned) || 0,
        workout_completed: parseInt(formData.workout_completed),
        workout_duration: parseInt(formData.workout_duration) || 0,
        calories_consumed: formData.calories_consumed ? parseInt(formData.calories_consumed) : null,
        water_intake: formData.water_intake ? parseFloat(formData.water_intake) : null,
        sleep_hours: formData.sleep_hours ? parseFloat(formData.sleep_hours) : null,
        energy_level: formData.energy_level,
        mood: formData.mood,
        notes: formData.notes || null
      }
      
      await progressAPI.create(data)
      toast.success('Progress logged successfully!')
      setShowForm(false)
      setFormData({
        weight: '',
        calories_burned: '',
        workout_completed: 1,
        workout_duration: '',
        calories_consumed: '',
        water_intake: '',
        sleep_hours: '',
        energy_level: 'Medium',
        mood: 'Good',
        notes: ''
      })
      fetchData()
    } catch (error) {
      toast.error('Failed to log progress')
    } finally {
      setSubmitting(false)
    }
  }

  const hasNoData = !chartData || (
    chartData.calories?.length === 0 && 
    chartData.weight?.length === 0 && 
    chartData.workouts?.length === 0
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const statCards = [
    {
      title: 'Total Workouts',
      value: summary?.total_workouts || 0,
      icon: Activity,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    },
    {
      title: 'Calories Burned',
      value: summary?.total_calories_burned || 0,
      icon: Flame,
      color: 'text-orange-500',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
    },
    {
      title: 'Current Streak',
      value: summary?.current_streak || 0,
      unit: 'days',
      icon: TrendingUp,
      color: 'text-green-500',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'Weight Change',
      value: summary?.weight_change ? `${summary.weight_change > 0 ? '+' : ''}${summary.weight_change}` : 'N/A',
      unit: summary?.weight_change ? 'kg' : '',
      icon: Weight,
      color: 'text-purple-500',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between flex-wrap gap-4"
      >
        <div>
          <h1 className="text-3xl font-bold mb-2">Progress Tracking</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor your fitness journey
          </p>
        </div>

        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setShowForm(true)}
            className="btn-primary flex items-center gap-2"
          >
            <Plus size={18} />
            Log Progress
          </button>
          
          {[7, 30, 90].map((days) => (
            <button
              key={days}
              onClick={() => setTimeRange(days)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                timeRange === days
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {days}D
            </button>
          ))}
        </div>
      </motion.div>

      {/* Log Progress Modal */}
      {showForm && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setShowForm(false)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-dark-card rounded-xl p-6 max-w-lg w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Log Today's Progress</h2>
              <button onClick={() => setShowForm(false)} className="text-gray-500 hover:text-gray-700">
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Weight (kg)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="weight"
                    value={formData.weight}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="70.5"
                  />
                </div>
                <div>
                  <label className="label">Calories Burned</label>
                  <input
                    type="number"
                    name="calories_burned"
                    value={formData.calories_burned}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="350"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Workouts Completed</label>
                  <select
                    name="workout_completed"
                    value={formData.workout_completed}
                    onChange={handleFormChange}
                    className="input"
                  >
                    <option value={0}>0 - Rest Day</option>
                    <option value={1}>1 Workout</option>
                    <option value={2}>2 Workouts</option>
                    <option value={3}>3+ Workouts</option>
                  </select>
                </div>
                <div>
                  <label className="label">Workout Duration (min)</label>
                  <input
                    type="number"
                    name="workout_duration"
                    value={formData.workout_duration}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="45"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Calories Consumed</label>
                  <input
                    type="number"
                    name="calories_consumed"
                    value={formData.calories_consumed}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="2000"
                  />
                </div>
                <div>
                  <label className="label">Water Intake (L)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="water_intake"
                    value={formData.water_intake}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="2.5"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Sleep Hours</label>
                  <input
                    type="number"
                    step="0.5"
                    name="sleep_hours"
                    value={formData.sleep_hours}
                    onChange={handleFormChange}
                    className="input"
                    placeholder="7.5"
                  />
                </div>
                <div>
                  <label className="label">Energy Level</label>
                  <select
                    name="energy_level"
                    value={formData.energy_level}
                    onChange={handleFormChange}
                    className="input"
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="label">Mood</label>
                <div className="flex gap-4">
                  {['Bad', 'Neutral', 'Good'].map((m) => (
                    <label key={m} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="mood"
                        value={m}
                        checked={formData.mood === m}
                        onChange={handleFormChange}
                        className="text-primary-600"
                      />
                      <span>{m === 'Bad' ? '😔' : m === 'Neutral' ? '😐' : '😊'} {m}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="label">Notes (optional)</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleFormChange}
                  className="input"
                  rows={2}
                  placeholder="How did you feel today?"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full btn-primary py-3 disabled:opacity-50"
              >
                {submitting ? 'Saving...' : 'Save Progress'}
              </button>
            </form>
          </motion.div>
        </motion.div>
      )}

      {/* Empty State */}
      {hasNoData ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-8 text-center"
        >
          <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center text-white mx-auto mb-4">
            <BarChart3 size={32} />
          </div>
          <h2 className="text-2xl font-bold mb-4">No Progress Data Yet</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
            Start tracking your fitness journey! Log your daily progress or generate sample data to see the charts in action.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <button
              onClick={() => setShowForm(true)}
              className="btn-primary"
            >
              <Plus size={18} className="inline mr-2" />
              Log Progress
            </button>
            <button
              onClick={generateSampleData}
              disabled={seeding}
              className="btn-secondary disabled:opacity-50"
            >
              {seeding ? 'Generating...' : 'Generate Sample Data'}
            </button>
          </div>
        </motion.div>
      ) : (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {statCards.map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="card p-6"
              >
                <div className={`p-3 rounded-lg ${stat.bgColor} w-fit mb-4`}>
                  <stat.icon className={stat.color} size={24} />
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold">
                  {stat.value} {stat.unit && <span className="text-sm font-normal">{stat.unit}</span>}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Charts */}
          {chartData && (
            <>
              {/* Calories Chart */}
              {chartData.calories && chartData.calories.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="card p-6"
                >
                  <h3 className="text-xl font-bold mb-4">🔥 Calories Burned</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData.calories}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="calories" fill="#f97316" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </motion.div>
              )}

              {/* Weight Chart */}
              {chartData.weight && chartData.weight.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="card p-6"
                >
                  <h3 className="text-xl font-bold mb-4">⚖️ Weight Progress</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData.weight}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                      <YAxis domain={['dataMin - 1', 'dataMax + 1']} />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="weight" 
                        stroke="#8b5cf6" 
                        strokeWidth={3}
                        dot={{ fill: '#8b5cf6', strokeWidth: 2 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </motion.div>
              )}

              {/* Workouts Chart */}
              {chartData.workouts && chartData.workouts.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="card p-6"
                >
                  <h3 className="text-xl font-bold mb-4">💪 Workout Frequency</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData.workouts}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="workouts" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </motion.div>
              )}
            </>
          )}

          {/* Summary Stats */}
          {summary && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card p-6"
            >
              <h3 className="text-xl font-bold mb-4">📊 Summary</h3>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Avg Workout Duration
                  </p>
                  <p className="text-2xl font-bold">
                    {summary.average_workout_duration?.toFixed(1) || 0} <span className="text-sm font-normal">min</span>
                  </p>
                </div>
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Total Workouts
                  </p>
                  <p className="text-2xl font-bold">{summary.total_workouts}</p>
                </div>
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Avg Calories/Day
                  </p>
                  <p className="text-2xl font-bold">
                    {summary.records?.length > 0
                      ? Math.round(summary.total_calories_burned / summary.records.length)
                      : 0}
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </>
      )}
    </div>
  )
}

export default Progress
