import { useSocket } from '@/composables/useSocket'
import { withSocketLoading } from '@/api/utils/socketLoadingWrapper'

const sockets = new Map()

export const webSocketService = {
  connect(key, path, options = {}, params = {}) {
    if (sockets.has(key)) {
      return sockets.get(key)
    }

    let socketInstance = useSocket(path, options, params)

    socketInstance = withSocketLoading(socketInstance)

    socketInstance.connect()

    sockets.set(key, socketInstance)
    return socketInstance
  },

  get(key) {
    return sockets.get(key)
  },

  disconnect(key) {
    sockets.get(key)?.disconnect()
    sockets.delete(key)
  },

  disconnectAll() {
    sockets.forEach((s) => s.disconnect())
    sockets.clear()
  },
}
