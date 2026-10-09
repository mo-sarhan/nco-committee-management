<template>
  <div v-if="loadingStore.isGlobalLoading" class="global-loader-overlay">
    <div class="spinner"></div>
    <h1>جارِ التحميل...</h1>
  </div>
</template>

<script setup>
import { useLoadingStore } from '@/stores/loadingStore'
const loadingStore = useLoadingStore()
</script>

<style scoped>
.global-loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.spinner {
  border: 5px solid #f3f3f3;
  border-top: 5px solid var(--secondColor);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
