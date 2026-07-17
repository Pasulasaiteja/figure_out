import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { systemAPI } from '../services/api'
import { 
  Server, 
  Database, 
  Activity, 
  Globe, 
  RefreshCw, 
  CheckCircle2, 
  XCircle,
  Clock,
  Cpu
} from 'lucide-react'

const Health = () => {
  const [healthData, setHealthData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [responseTime, setResponseTime] = useState(0)
  const [lastChecked, setLastChecked] = useState(null)

  const checkHealth = useCallback(async () => {
    setLoading(true)
    setError(null)
    const startTime = performance.now()
    
    try {
      const response = await systemAPI.checkHealth()
      const endTime = performance.now()
      
      setResponseTime(Math.round(endTime - startTime))
      setHealthData(response.data)
      setLastChecked(new Date())
    } catch (err) {
      const endTime = performance.now()
      setResponseTime(Math.round(endTime - startTime))
      
      if (err.response && err.response.data) {
        setHealthData(err.response.data)
      } else {
        setHealthData(null)
        setError('Unable to connect to server. Please try again later.')
      }
      setLastChecked(new Date())
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    checkHealth()
    
    // Auto refresh every 30 seconds
    const interval = setInterval(() => {
      checkHealth()
    }, 30000)
    
    return () => clearInterval(interval)
  }, [checkHealth])

  const formatDate = (date) => {
    if (!date) return 'Never'
    return new Intl.DateTimeFormat('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    }).format(date)
  }

  const isHealthy = healthData?.status === 'healthy'
  const isDbConnected = healthData?.database === 'connected'
  const isOffline = error || !healthData

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  }

  const StatusIcon = ({ status, offline }) => {
    if (offline) return <XCircle className="text-red-500 w-6 h-6" />
    if (status) return <CheckCircle2 className="text-green-500 w-6 h-6" />
    return <XCircle className="text-red-500 w-6 h-6" />
  }

  const StatusText = ({ status, offline, textOn, textOff }) => {
    if (offline) return <span className="text-red-500 font-semibold">{textOff || 'Offline'}</span>
    if (status) return <span className="text-green-500 font-semibold">{textOn || 'Healthy'}</span>
    return <span className="text-red-500 font-semibold">{textOff || 'Unhealthy'}</span>
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">System Health</h1>
          <p className="text-gray-500 dark:text-gray-400">Monitor application and API status</p>
        </div>
        <button
          onClick={checkHealth}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-dark-card border border-gray-200 dark:border-dark-border rounded-lg shadow-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-sm font-medium text-gray-700 dark:text-gray-300 disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh Status
        </button>
      </div>

      {isOffline && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-400 flex items-center gap-3"
        >
          <XCircle className="w-5 h-5 flex-shrink-0" />
          <p>{error || 'Backend Status: Offline. Unable to connect to server.'}</p>
        </motion.div>
      )}

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        {/* Application Card */}
        <motion.div variants={itemVariants} className="card p-6 flex flex-col items-center justify-center text-center space-y-4">
          <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full text-blue-600 dark:text-blue-400">
            <Globe className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Application</h3>
            <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">Transformers AI</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Fitness Platform</p>
          </div>
        </motion.div>

        {/* Frontend Card */}
        <motion.div variants={itemVariants} className="card p-6 flex flex-col items-center justify-center text-center space-y-4 border-t-4 border-green-500">
          <StatusIcon status={true} offline={false} />
          <div>
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Frontend</h3>
            <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
              <StatusText status={true} offline={false} textOn="Running" />
            </p>
          </div>
        </motion.div>

        {/* Backend Card */}
        <motion.div variants={itemVariants} className={`card p-6 flex flex-col items-center justify-center text-center space-y-4 border-t-4 ${isOffline ? 'border-red-500' : (isHealthy ? 'border-green-500' : 'border-red-500')}`}>
          <StatusIcon status={isHealthy} offline={isOffline} />
          <div>
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Backend</h3>
            <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
              <StatusText status={isHealthy} offline={isOffline} textOn="Healthy" textOff="Offline" />
            </p>
            {healthData?.service && <p className="text-sm text-gray-500 dark:text-gray-400">{healthData.service}</p>}
          </div>
        </motion.div>

        {/* Database Card */}
        <motion.div variants={itemVariants} className={`card p-6 flex flex-col items-center justify-center text-center space-y-4 border-t-4 ${isOffline ? 'border-gray-300 dark:border-gray-700' : (isDbConnected ? 'border-green-500' : 'border-red-500')}`}>
          <div className={`p-3 rounded-full ${isOffline ? 'bg-gray-100 dark:bg-gray-800 text-gray-400' : (isDbConnected ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400')}`}>
            <Database className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Database</h3>
            <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
              {isOffline ? (
                <span className="text-gray-500 dark:text-gray-400">Unknown</span>
              ) : (
                <StatusText status={isDbConnected} offline={false} textOn="Connected" textOff="Disconnected" />
              )}
            </p>
          </div>
        </motion.div>
      </motion.div>

      {/* Details Section */}
      <motion.div 
        variants={itemVariants}
        initial="hidden"
        animate="show"
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        <div className="card p-6 flex items-center gap-4">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-lg text-purple-600 dark:text-purple-400">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400">Version</p>
            <p className="font-semibold text-gray-900 dark:text-white">{healthData?.version || '1.0.0'}</p>
          </div>
        </div>

        <div className="card p-6 flex items-center gap-4">
          <div className="p-3 bg-orange-100 dark:bg-orange-900/30 rounded-lg text-orange-600 dark:text-orange-400">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400">Response Time</p>
            <p className="font-semibold text-gray-900 dark:text-white">
              {loading ? '...' : `${responseTime} ms`}
            </p>
          </div>
        </div>

        <div className="card p-6 flex items-center gap-4">
          <div className="p-3 bg-teal-100 dark:bg-teal-900/30 rounded-lg text-teal-600 dark:text-teal-400">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400">Last Checked</p>
            <p className="font-semibold text-gray-900 dark:text-white text-sm">
              {formatDate(lastChecked)}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Health
