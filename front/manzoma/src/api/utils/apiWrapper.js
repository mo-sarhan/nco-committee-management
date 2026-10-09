import { useLoadingStore } from '@/stores/loadingStore'

export async function withLoading(apiCall) {
    const loadingStore = useLoadingStore()
    loadingStore.startLoading()
    try {
        const result = await apiCall()
        return result
    } catch (error) {
        throw error
    } finally {
        loadingStore.stopLoading()
    }
}