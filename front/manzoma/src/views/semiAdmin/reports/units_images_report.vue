<template>
  <div class="dashboard-layout rtl-container">
    
  </div>
</template>

<script setup>
import { ref } from 'vue'

</script>

<style scoped>
.rtl-container {
  direction: rtl;
  text-align: right;
}

.dashboard-layout {
  display: grid;
  /* تقسيم الشاشة إلى أعمدة مرنة */
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px;
}
</style>
