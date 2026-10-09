<template>
  <div class="dashboard-layout rtl-container">
    <StatCard
      v-for="metric in metrics"
      :key="metric.title"
      :title="metric.title"
      :value="metric.value"
      :icon="metric.icon"
      :color="metric.color"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StatCard from '@/components/mainAdmin/StateCard.vue'
import { icons } from '../../../public/icons'

const metrics = ref([
  {
    title: 'تقرير الصور للوحدات',
    value: '',
    icon: icons.Group,
    color: '#059669',
  },
  // {
  //   title: 'الحسابات المعلقة/المراجعة',
  //   value: '42',
  //   icon: icons.Gavel,
  //   color: '#f97316',
  // },
])
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
