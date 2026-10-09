<script setup>
import { ref, onMounted } from 'vue'
import BaseError from './BaseError.vue'

const endTime = new Date().getTime() + 60 * 60 * 1000 // 1 hour
const timeLeft = ref('')

const updateTimer = () => {
  const now = new Date().getTime()
  const diff = endTime - now

  if (diff <= 0) {
    timeLeft.value = "00:00"
    return
  }

  const minutes = Math.floor(diff / 60000)
  const seconds = Math.floor((diff % 60000) / 1000)

  timeLeft.value = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
}

onMounted(() => {
  setInterval(updateTimer, 1000)
})
</script>

<template>
  <BaseError
    code="🚧"
    title="الموقع تحت الصيانة"
  >
    <h3>العودة خلال:</h3>
    <h2>{{ timeLeft }}</h2>
  </BaseError>
</template>