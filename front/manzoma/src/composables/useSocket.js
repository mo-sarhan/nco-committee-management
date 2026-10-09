import { ref } from 'vue'

export function useSocket(wsPath, options = {}, params = {}) {
  const socket = ref(null)
  const isConnected = ref(false)
  let heartbeatTimer = null
  let reconnectTimer = null

  const { reconnectInterval = 3000, heartbeatInterval = 10000, autoReconnect = true } = options

  const buildUrl = () => {
    const base = (import.meta.env.VITE_SOCKET_BASE_URL || '').trim()
    const protocol =
      import.meta.env.VITE_WS_PROTOCOL || (location.protocol === 'https:' ? 'wss' : 'ws')

    const token = localStorage.getItem('token')
    const path = wsPath.startsWith('/') ? wsPath : `/${wsPath}`

    const query = new URLSearchParams({
      token,
      ...params,
    }).toString()

    const host = base.replace(/^(wss?|https?):\/\//, '').replace(/\/+$/, '')

    return `${protocol}://${host}${path}?${query}`
  }

  const startHeartbeat = () => {
    stopHeartbeat()
    heartbeatTimer = setInterval(() => {
      if (socket.value?.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({ type: 'ping' }))
      }
    }, heartbeatInterval)
  }

  const stopHeartbeat = () => {
    clearInterval(heartbeatTimer)
    heartbeatTimer = null
  }

  const connect = () => {
    if (socket.value) return
    // const token = localStorage.getItem('token')
    socket.value = new WebSocket(buildUrl())

    socket.value.onopen = () => {
      isConnected.value = true

      // socket.value.send(
      //   JSON.stringify({
      //     type: 'authentication',
      //     token: token,
      //   }),
      // )

      startHeartbeat()
    }

    socket.value.onclose = () => {
      isConnected.value = false
      stopHeartbeat()
      socket.value = null

      if (autoReconnect) {
        reconnectTimer = setTimeout(connect, reconnectInterval)
      }
    }

    socket.value.onerror = () => {
      socket.value?.close()
    }
  }

  const disconnect = () => {
    autoReconnect && clearTimeout(reconnectTimer)
    stopHeartbeat()
    socket.value?.close()
    socket.value = null
  }

  return {
    socket,
    isConnected,
    connect,
    disconnect,
  }
}
