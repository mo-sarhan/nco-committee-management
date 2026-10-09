import router from '@/router'

export function handleApiError(error) {
  const status = error?.response?.status

  console.error('API Error:', error)

  if (status === 401) {
    localStorage.clear()
    router.push({ name: 'login' })
  }

  throw error
}