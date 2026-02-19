import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { assessmentAPI } from '../services/api'
import toast from 'react-hot-toast'

const HealthAssessment = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [existingData, setExistingData] = useState(null)
  const [formData, setFormData] = useState({
    medical_conditions: '',
    allergies: '',
    injuries: '',
    medications: '',
    fitness_level: 'Beginner',
    fitness_goals: '',
    workout_preference: 'Home',
    time_availability: '30min',
    diet_type: 'None',
    calorie_target: 2000,
    dietary_restrictions: '',
    sleep_hours: 7,
    stress_level: 'Medium',
  })

  useEffect(() => {
    fetchExisting()
  }, [])

  const fetchExisting = async () => {
    try {
      const response = await assessmentAPI.get()
      setExistingData(response.data)
      setFormData(response.data)
    } catch (error) {
      // No existing assessment
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await assessmentAPI.create(formData)
      toast.success('Health assessment saved successfully!')
      navigate('/dashboard')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save assessment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold mb-2">Health Assessment</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Tell us about yourself so we can create the perfect plan
        </p>
      </motion.div>

      <motion.form
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        onSubmit={handleSubmit}
        className="card p-8 space-y-6"
      >
        {/* Medical Information */}
        <div>
          <h3 className="text-xl font-bold mb-4">Medical Information</h3>
          
          <div className="space-y-4">
            <div>
              <label className="label">Medical Conditions (if any)</label>
              <input
                type="text"
                name="medical_conditions"
                value={formData.medical_conditions}
                onChange={handleChange}
                className="input"
                placeholder="e.g., Diabetes, Hypertension"
              />
            </div>

            <div>
              <label className="label">Allergies</label>
              <input
                type="text"
                name="allergies"
                value={formData.allergies}
                onChange={handleChange}
                className="input"
                placeholder="e.g., Peanuts, Dairy"
              />
            </div>

            <div>
              <label className="label">Injuries or Limitations</label>
              <input
                type="text"
                name="injuries"
                value={formData.injuries}
                onChange={handleChange}
                className="input"
                placeholder="e.g., Knee injury, Back pain"
              />
            </div>

            <div>
              <label className="label">Current Medications</label>
              <input
                type="text"
                name="medications"
                value={formData.medications}
                onChange={handleChange}
                className="input"
              />
            </div>
          </div>
        </div>

        {/* Fitness Information */}
        <div>
          <h3 className="text-xl font-bold mb-4">Fitness Information</h3>
          
          <div className="space-y-4">
            <div>
              <label className="label">Fitness Level *</label>
              <select
                name="fitness_level"
                value={formData.fitness_level}
                onChange={handleChange}
                className="input"
                required
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>

            <div>
              <label className="label">Fitness Goals *</label>
              <textarea
                name="fitness_goals"
                value={formData.fitness_goals}
                onChange={handleChange}
                className="input"
                rows="3"
                placeholder="e.g., Lose weight, Build muscle, Improve endurance"
                required
              />
            </div>

            <div>
              <label className="label">Workout Preference *</label>
              <select
                name="workout_preference"
                value={formData.workout_preference}
                onChange={handleChange}
                className="input"
                required
              >
                <option value="Home">Home Workouts</option>
                <option value="Gym">Gym Workouts</option>
                <option value="Outdoor">Outdoor Activities</option>
              </select>
            </div>

            <div>
              <label className="label">Daily Time Availability *</label>
              <select
                name="time_availability"
                value={formData.time_availability}
                onChange={handleChange}
                className="input"
                required
              >
                <option value="30min">30 minutes</option>
                <option value="45min">45 minutes</option>
                <option value="60min">60 minutes</option>
                <option value="90min">90+ minutes</option>
              </select>
            </div>
          </div>
        </div>

        {/* Nutrition Information */}
        <div>
          <h3 className="text-xl font-bold mb-4">Nutrition Information</h3>
          
          <div className="space-y-4">
            <div>
              <label className="label">Diet Type *</label>
              <select
                name="diet_type"
                value={formData.diet_type}
                onChange={handleChange}
                className="input"
                required
              >
                <option value="None">No Restrictions</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Keto">Keto</option>
                <option value="Paleo">Paleo</option>
              </select>
            </div>

            <div>
              <label className="label">Daily Calorie Target *</label>
              <input
                type="number"
                name="calorie_target"
                value={formData.calorie_target}
                onChange={handleChange}
                className="input"
                min="1200"
                max="5000"
                required
              />
            </div>

            <div>
              <label className="label">Dietary Restrictions</label>
              <input
                type="text"
                name="dietary_restrictions"
                value={formData.dietary_restrictions}
                onChange={handleChange}
                className="input"
                placeholder="e.g., Gluten-free, Low sodium"
              />
            </div>
          </div>
        </div>

        {/* Lifestyle */}
        <div>
          <h3 className="text-xl font-bold mb-4">Lifestyle</h3>
          
          <div className="space-y-4">
            <div>
              <label className="label">Average Sleep Hours *</label>
              <input
                type="number"
                name="sleep_hours"
                value={formData.sleep_hours}
                onChange={handleChange}
                className="input"
                min="4"
                max="12"
                required
              />
            </div>

            <div>
              <label className="label">Stress Level *</label>
              <select
                name="stress_level"
                value={formData.stress_level}
                onChange={handleChange}
                className="input"
                required
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full btn-primary py-3 disabled:opacity-50"
        >
          {loading ? 'Saving...' : existingData ? 'Update Assessment' : 'Save Assessment'}
        </button>
      </motion.form>
    </div>
  )
}

export default HealthAssessment
