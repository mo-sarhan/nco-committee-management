<template>
  <div v-if="showZoomOverlay" class="zoom-overlay" @click="$emit('closeZoom')">
    <img :src="zoomedImage" class="zoomed-image" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

defineEmits(['closeZoom'])
const props = defineProps({
  showZoomOverlay: Boolean,
  zoomedImage: String,
})
</script>

<style>
.zoom-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  cursor: zoom-out;
}

.zoomed-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s;
  /* width: 60%; */
  /* height: 90%; */
}

.zoomed-image:hover {
  transform: scale(1.02);
}
</style>
