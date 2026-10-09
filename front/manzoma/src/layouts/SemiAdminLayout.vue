<template>
  <div class="semi-admin-layout">
    <header>
      <h1>Semi Admin Panel</h1>
      <button @click="logout">Logout</button>
    </header>
    <aside>
      <!-- Navigation Menu -->
      <ul>
        <li><router-link to="/semi-admin">Dashboard</router-link></li>
      </ul>
    </aside>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore';
const authStore = useAuthStore();
const logout = () => authStore.logout();
</script>

<style>
.semi-admin-layout { display: grid; grid-template-areas: "header header" "aside main"; grid-template-columns: 200px 1fr; grid-template-rows: 60px 1fr; height: 100vh; }
header { grid-area: header; background: #8e44ad; color: white; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem; }
aside { grid-area: aside; background: #9b59b6; color: white; padding: 1rem; }
main { grid-area: main; padding: 1rem; }
</style>
