<template>
  <div class="afrperson-container">
    <pageNavigation />

    <div class="report-page">
      <StatCard
        v-for="metric in metrics"
        :key="metric.title"
        :title="metric.title"
        :value="metric.value"
        :icon="metric.icon"
        :fontawesome="metric.fontawesome"
        :color="metric.color"
        :clickable="metric.clickable"
        :routeName="metric.routeName"
        :routeParams="metric.routeParams"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import pageNavigation from '@/components/global/pageNavigation.vue'
import StatCard from '@/components/mainAdmin/StateCard.vue'
import { icons } from '../../../../../public/icons'

const metrics = ref([
  {
    title: 'تقرير مراجعة الصور',
    // value: '14,500',
    fontawesome: 'fa-solid fa-magnifying-glass',
    color: '#059669',
    clickable: true,
    routeName: 'uploadedImagesReport',
    routeParams: {},
  },
  // {
  //   title: 'تقرير رفع الصور',
  //   value: '42',
  //   fontawesome:'fa-solid fa-magnifying-glass',
  //   color: '#f97316',
  //   clickable:true,
  //   routeName: 'uploadedImagesReport',
  //   routeParams:{

  //   }
  // },
])
</script>

<style scoped>
.report-page {
  display: grid;
  /* تقسيم الشاشة إلى أعمدة مرنة */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  max-width: 600px;
  padding: 20px;
}
</style>
