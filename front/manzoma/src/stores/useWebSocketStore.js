import { defineStore } from 'pinia'
import { webSocketService } from '@/services/webSocketService'

export const useWebSocketStore = defineStore('websocket', {
  state: () => ({
    sockets: {},
  }),

  actions: {
    connect(key, path, options,params) {
      const socket = webSocketService.connect(key, path, options,params)
      this.sockets[key] = socket
      return socket
    },

    disconnect(key) {
      webSocketService.disconnect(key)
      delete this.sockets[key]
    },

    disconnectAll() {
      webSocketService.disconnectAll()
      this.sockets = {}
    },
  },
})