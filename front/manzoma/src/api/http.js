import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const getErrorMessage = (error) => {
  const status = error.response?.status

  if (error.response?.data?.message) return error.response.data.message
  if (error.message) return error.message
  return 'API Error'
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 10000,
  headers: { 'Content-Type': 'multipart/form-data' },
  // headers: { 'Content-Type': 'application/json' },
})

const controllers = new Map()

http.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) config.headers.Authorization = `Bearer ${authStore.token}`

  const controller = new AbortController()
  config.signal = controller.signal

  const key = `${config.method}:${config.url}`
  controllers.set(key, controller)

  return config
})

http.interceptors.response.use(
  (response) => {
    const key = `${response.config.method}:${response.config.url}`
    controllers.delete(key)
    return response
  },
  async (error) => {
    const config = error.config
    if (config) {
      const key = `${config.method}:${config.url}`
      controllers.delete(key)
    }

    const message = getErrorMessage(error)
    if (!config || !config.retryCount) config.retryCount = 0

    if ((error.code === 'ECONNABORTED' || !error.response) && config.retryCount < 2) {
      config.retryCount += 1
      return http(config)
    }

    console.error('API Error:', message)
    return Promise.reject(error)
  },
)

export function cancelRequest(method, url) {
  const key = `${method}:${url}`
  const controller = controllers.get(key)
  if (controller) {
    controller.abort()
    controllers.delete(key)
  }
}

export default http
