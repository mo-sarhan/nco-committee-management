<template>
  <div class="layout" dir="rtl">
    <!-- <Sidebar :is-open="isSidebarOpen" @toggle-sidebar="toggleSidebar" /> -->

    <div :class="['content-container', isSidebarOpen ? 'sidebar-open' : '']">
      <Header @toggle-sidebar="toggleSidebar" />

      <main class="main">
        <router-view />
      </main>

      <Footer />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from '@/components/layouts/mainAdmin/Header.vue'
import Sidebar from '@/components/layouts/mainAdmin/Sidebar.vue'
import Footer from '@/components/layouts/mainAdmin/Footer.vue'

// This is the SINGLE source of truth for the sidebar's locked/open state
const isSidebarOpen = ref(false)
const toggleSidebar = () => (isSidebarOpen.value = !isSidebarOpen.value)
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: #f9fafb;
  display: flex;
  direction: rtl;
}

.content-container {
  flex: 1;
  margin-right: 70px;
  transition: margin-right 0.3s ease;
}

.sidebar-open {
  margin-right: 260px;
}
.semi-sidebar-open {
  margin-right: 120px;
  background-color: black;
}

.main {
  padding: 20px 20px;
  min-height: 83%;
}
</style>
