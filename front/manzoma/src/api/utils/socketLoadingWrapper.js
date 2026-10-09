import { useLoadingStore } from '@/stores/loadingStore'

export function withSocketLoading(socketInstance) {
  const loadingStore = useLoadingStore()

  const originalConnect = socketInstance.connect
  const originalDisconnect = socketInstance.disconnect

  socketInstance.connect = () => {
    loadingStore.startLoading()

    originalConnect()

    const socket = socketInstance.socket.value
    if (!socket) {
      loadingStore.stopLoading()
      return
    }

    const originalOnOpen = socket.onopen
    const originalOnError = socket.onerror

    socket.onopen = (event) => {
      originalOnOpen?.(event)
      loadingStore.stopLoading()
      socketInstance.isConnected.value = true
    }

    socket.onerror = (event) => {
      originalOnError?.(event)
      loadingStore.stopLoading()
    }
  }

  socketInstance.disconnect = () => {
    originalDisconnect()
    loadingStore.stopLoading()
  }

  return socketInstance
}
