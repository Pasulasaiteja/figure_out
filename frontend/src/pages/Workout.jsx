import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Play, CheckCircle, Flame, Clock, Zap } from 'lucide-react'
import { workoutAPI } from '../services/api'
import toast from 'react-hot-toast'

const Workout = () => {
  const [plan, setPlan] = useState(null)
  const [selectedDay, setSelectedDay] = useState(1)
  const [exercises, setExercises] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetchPlan()
  }, [])

  useEffect(() => {
    if (plan) {
      fetchDayExercises(selectedDay)
    }
  }, [selectedDay, plan])

  const fetchPlan = async () => {
    try {
      const response = await workoutAPI.getCurrent()
      setPlan(response.data)
    } catch (error) {
      setPlan(null)
    } finally {
      setLoading(false)
    }
  }

  const fetchDayExercises = async (day) => {
    try {
      const response = await workoutAPI.getDay(day)
      setExercises(response.data)
    } catch (error) {
      toast.error('Failed to load exercises')
    }
  }

  const generatePlan = async () => {
    setGenerating(true)
    try {
      const response = await workoutAPI.generate()
      setPlan(response.data)
      toast.success('Workout plan generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate plan')
    } finally {
      setGenerating(false)
    }
  }

  const completeExercise = async (exerciseId, calories) => {
    try {
      await workoutAPI.complete({
        exercise_id: exerciseId,
        calories_burned: calories,
      })
      fetchDayExercises(selectedDay)
      toast.success('Exercise completed! 🎉')
    } catch (error) {
      toast.error('Failed to complete exercise')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!plan) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl mx-auto text-center py-16"
      >
        <div className="card p-8">
          <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center text-white mx-auto mb-4">
            <Zap size={32} />
          </div>
          <h2 className="text-2xl font-bold mb-4">Generate Your Workout Plan</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Our AI will create a personalized 7-day workout plan based on your health assessment,
            fitness level, and goals.
          </p>
          <button
            onClick={generatePlan}
            disabled={generating}
            className="btn-primary disabled:opacity-50"
          >
            {generating ? 'Generating Plan...' : 'Generate AI Workout Plan'}
          </button>
        </div>
      </motion.div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">{plan.title}</h1>
        <p className="text-gray-600 dark:text-gray-400">{plan.description}</p>
        <div className="flex gap-3 mt-3">
          <span className="px-3 py-1 bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 rounded-full text-sm font-medium">
            {plan.difficulty_level}
          </span>
          <span className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm font-medium">
            {plan.duration_days} Days
          </span>
        </div>
      </motion.div>

      {/* Day Selector */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {[1, 2, 3, 4, 5, 6, 7].map((day) => (
          <button
            key={day}
            onClick={() => setSelectedDay(day)}
            className={`px-6 py-3 rounded-lg font-medium whitespace-nowrap transition-all ${
              selectedDay === day
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            Day {day}
          </button>
        ))}
      </div>

      {/* Exercises */}
      <div className="space-y-4">
        {exercises.map((exercise, idx) => (
          <motion.div
            key={exercise.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className={`card p-6 ${exercise.is_completed ? 'opacity-60' : ''}`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    exercise.category === 'Warmup'
                      ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400'
                      : exercise.category === 'Cardio'
                      ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400'
                      : exercise.category === 'Strength'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
                      : 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                  }`}>
                    {exercise.category}
                  </span>
                  {exercise.is_completed && (
                    <CheckCircle size={16} className="text-green-500" />
                  )}
                </div>
                
                <h3 className="text-xl font-bold mb-2">{exercise.name}</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-3">
                  {exercise.description}
                </p>

                <div className="flex flex-wrap gap-4 text-sm">
                  {exercise.sets && (
                    <div className="flex items-center gap-1">
                      <Zap size={16} className="text-gray-500" />
                      <span>{exercise.sets} sets × {exercise.reps} reps</span>
                    </div>
                  )}
                  {exercise.rest_period && (
                    <div className="flex items-center gap-1">
                      <Clock size={16} className="text-gray-500" />
                      <span>Rest: {exercise.rest_period}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-1">
                    <Flame size={16} className="text-orange-500" />
                    <span>{exercise.estimated_calories} calories</span>
                  </div>
                </div>

                {exercise.fitness_tip && (
                  <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      💡 Tip: {exercise.fitness_tip}
                    </p>
                  </div>
                )}
              </div>

              <div className="flex flex-col gap-2">
                {exercise.youtube_video_id && (
                  <a
                    href={`https://www.youtube.com/watch?v=${exercise.youtube_video_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary flex items-center gap-2"
                  >
                    <Play size={16} />
                    Watch
                  </a>
                )}
                
                {!exercise.is_completed && (
                  <button
                    onClick={() => completeExercise(exercise.id, exercise.estimated_calories)}
                    className="btn-primary"
                  >
                    Complete
                  </button>
                )}
              </div>
            </div>

            {exercise.instructions && (
              <details className="mt-4">
                <summary className="cursor-pointer font-medium text-primary-600 dark:text-primary-400">
                  View Instructions
                </summary>
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                  {exercise.instructions}
                </p>
              </details>
            )}
          </motion.div>
        ))}

        {exercises.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No exercises for this day
          </div>
        )}
      </div>
    </div>
  )
}

export default Workout
