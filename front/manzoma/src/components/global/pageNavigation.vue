<template>
  <div class="header-box">
    <div class="header">
      <nav class="breadcrumbs">
        <router-link
          v-for="(crumb, index) in breadcrumbs"
          :key="index"
          :to="(index !== breadcrumbs.length - 1 && crumb.path) ? crumb.path : '/'"
          class="crumb"
          :class="{ active: index === breadcrumbs.length - 1 }"
        >
          {{ crumb.label }}
        </router-link>
      </nav>
    </div>
    <SmartBack/>
  </div>
</template>

<script setup>
import { useBreadcrumbs } from '@/composables/useBreadcrumbs'
import SmartBack from './SmartBack.vue';

const { breadcrumbs } = useBreadcrumbs()
console.log("breadcrumbs==============>",breadcrumbs.value)
</script>

<style scoped>
.header-box {
  width: 100%;
  max-width: 100%;
  margin: auto;
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header h1 {
  margin: 0;
  color: var(--dark-blue);
}
.breadcrumbs {
  display: flex;
  gap: 8px;
  color: black;
  font-size: 14px;
}
.crumb {
  color: black;
}
.crumb::after {
  content: '/';
  margin-inline-start: 8px;
}
.crumb:last-child::after {
  content: '';
}
.crumb.active {
  font-weight: 600;
  pointer-events: none;
  color: var(--primary-color);
  font-weight: bold;
}
</style>
