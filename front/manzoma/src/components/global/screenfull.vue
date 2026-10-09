<template>
  <button @click="toggleFullscreen" class="fullscreen-btn">
    <i :class="iconClass"></i>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const isFullscreen = ref(false)

const iconClass = computed(() => (isFullscreen.value ? 'fas fa-compress' : 'fas fa-expand'))

const toggleFullscreen = () => {
  const elem = document.documentElement
  if (!isFullscreen.value) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen()
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen()
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen()
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen()
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen()
    }
  }
  isFullscreen.value = !isFullscreen.value
}

document.addEventListener('fullscreenchange', () => {
  isFullscreen.value = !!document.fullscreenElement
})
</script>

<style scoped>
.fullscreen-btn {
  font-size: 1.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #333;
}
.fullscreen-btn:hover {
  color: #007bff;
}
</style>
