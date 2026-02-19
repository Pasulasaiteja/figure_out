import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Apple, Flame, ShoppingCart } from 'lucide-react'
import { nutritionAPI } from '../services/api'
import toast from 'react-hot-toast'

const Nutrition = () => {
  const [plan, setPlan] = useState(null)
  const [selectedDay, setSelectedDay] = useState(1)
  const [meals, setMeals] = useState([])
  const [groceryList, setGroceryList] = useState(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    fetchPlan()
  }, [])

  useEffect(() => {
    if (plan) {
      fetchDayMeals(selectedDay)
    }
  }, [selectedDay, plan])

  const fetchPlan = async () => {
    try {
      const response = await nutritionAPI.getCurrent()
      setPlan(response.data)
    } catch (error) {
      setPlan(null)
    } finally {
      setLoading(false)
    }
  }

  const fetchDayMeals = async (day) => {
    try {
      const response = await nutritionAPI.getDay(day)
      setMeals(response.data)
    } catch (error) {
      toast.error('Failed to load meals')
    }
  }

  const generatePlan = async () => {
    setGenerating(true)
    try {
      const response = await nutritionAPI.generate()
      setPlan(response.data)
      toast.success('Nutrition plan generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate plan')
    } finally {
      setGenerating(false)
    }
  }

  const fetchGroceryList = async () => {
    try {
      const response = await nutritionAPI.getGroceryList()
      setGroceryList(response.data)
      toast.success('Grocery list ready!')
    } catch (error) {
      toast.error('Failed to generate grocery list')
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
            <Apple size={32} />
          </div>
          <h2 className="text-2xl font-bold mb-4">Generate Your Nutrition Plan</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Our AI will create a personalized 7-day meal plan based on your dietary preferences,
            calorie target, and fitness goals.
          </p>
          <button
            onClick={generatePlan}
            disabled={generating}
            className="btn-primary disabled:opacity-50"
          >
            {generating ? 'Generating Plan...' : 'Generate AI Nutrition Plan'}
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
        className="flex items-start justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold mb-2">{plan.title}</h1>
          <p className="text-gray-600 dark:text-gray-400">{plan.description}</p>
          <div className="flex gap-3 mt-3">
            <span className="px-3 py-1 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-full text-sm font-medium">
              {plan.daily_calorie_target} cal/day
            </span>
            <span className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm font-medium">
              {plan.duration_days} Days
            </span>
          </div>
        </div>

        <button
          onClick={fetchGroceryList}
          className="btn-primary flex items-center gap-2"
        >
          <ShoppingCart size={20} />
          Grocery List
        </button>
      </motion.div>

      {/* Grocery List Modal */}
      {groceryList && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold">Weekly Grocery List</h3>
            <button
              onClick={() => setGroceryList(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          
          <div className="grid md:grid-cols-2 gap-2 max-h-64 overflow-y-auto mb-4">
            {groceryList.ingredients.map((ingredient, idx) => (
              <div key={idx} className="flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-700 rounded">
                <span className="text-green-500">✓</span>
                <span className="text-sm">{ingredient}</span>
              </div>
            ))}
          </div>

          <a
            href={groceryList.bigbasket_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary w-full"
          >
            Shop on BigBasket
          </a>
        </motion.div>
      )}

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

      {/* Meals */}
      <div className="space-y-4">
        {meals.map((meal, idx) => (
          <motion.div
            key={meal.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="card p-6"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <span className={`px-2 py-1 rounded text-xs font-medium mb-2 inline-block ${
                  meal.meal_type === 'Breakfast'
                    ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400'
                    : meal.meal_type === 'Lunch'
                    ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/20 dark:text-orange-400'
                    : 'bg-purple-100 text-purple-700 dark:bg-purple-900/20 dark:text-purple-400'
                }`}>
                  {meal.meal_type}
                </span>
                
                <h3 className="text-xl font-bold mb-2">{meal.name}</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {meal.description}
                </p>

                {/* Macros */}
                <div className="grid grid-cols-4 gap-4 mb-4">
                  <div className="text-center p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                      {meal.calories}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Calories</div>
                  </div>
                  <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      {meal.protein}g
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Protein</div>
                  </div>
                  <div className="text-center p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                    <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                      {meal.carbs}g
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Carbs</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                      {meal.fat}g
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Fat</div>
                  </div>
                </div>

                {/* Ingredients */}
                {meal.ingredients && meal.ingredients.length > 0 && (
                  <details className="mb-4">
                    <summary className="cursor-pointer font-medium text-primary-600 dark:text-primary-400 mb-2">
                      Ingredients
                    </summary>
                    <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400 space-y-1">
                      {meal.ingredients.map((ingredient, i) => (
                        <li key={i}>{ingredient}</li>
                      ))}
                    </ul>
                  </details>
                )}

                {/* Recipe */}
                {meal.recipe_instructions && (
                  <details>
                    <summary className="cursor-pointer font-medium text-primary-600 dark:text-primary-400">
                      Recipe Instructions
                    </summary>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                      {meal.recipe_instructions}
                    </p>
                    {(meal.prep_time || meal.cook_time) && (
                      <div className="flex gap-4 mt-3 text-sm text-gray-600 dark:text-gray-400">
                        {meal.prep_time && <span>Prep: {meal.prep_time} min</span>}
                        {meal.cook_time && <span>Cook: {meal.cook_time} min</span>}
                      </div>
                    )}
                  </details>
                )}
              </div>
            </div>
          </motion.div>
        ))}

        {meals.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No meals for this day
          </div>
        )}
      </div>
    </div>
  )
}

export default Nutrition
