import { useRouter } from 'vue-router'

export function useSmartBack(fallback = '/') {
  const router = useRouter()

  const goBack = () => {
    if (window.history.length > 1) {
      router.back()
    } else {
      router.push(fallback)
    }
  }

  return { goBack }
}
