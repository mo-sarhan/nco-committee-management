<template>
  <header class="header" dir="rtl">
    <div class="left">
      <img src="@/assets/Images/logo.png" alt="logo" width="50px" />
      <h1 class="header-title">هيئـــة التنظيـــم والادارة ق.م</h1>
    </div>

    <div class="right">
      <Screenfull />

      <button class="icon-btn" title="الإعدادات">
        <span v-html="icons.Settings"></span>
      </button>

      <div class="user-menu-wrapper" ref="menuWrapper">
        <button class="icon-btn" @click="toggleUserMenu" title="الملف الشخصي">
          <span v-html="icons.User"></span>
        </button>

        <div v-if="isUserMenuOpen" class="user-menu">
          <div class="menu-header">
            <span class="user-name">{{ username }}</span>

            <small class="user-role">{{ armyName ? armyName : 'مدير النظام' }}</small>
          </div>

          <button class="menu-item"><span v-html="icons.Settings"></span> الإعدادات</button>

          <button class="menu-item"><span v-html="icons.User"></span> حسابي</button>

          <button class="menu-item logout" @click="logout">
            <span v-html="icons.LogOut"></span> تسجيل الخروج
          </button>
        </div>
      </div>

      <div class="welcome">مرحباً، {{ username }}</div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { icons } from '../../../../public/icons.js'
import { useAuthStore } from '@/stores/authStore'
import Screenfull from '@/components/global/screenfull.vue'

const isUserMenuOpen = ref(false)
const menuWrapper = ref(null)
const authStore = useAuthStore()
const logout = authStore.logout
const username = authStore.user.info.username
const armyName = authStore.user.info.profile.army_name
const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

// Close menu when clicking outside
const handleClickOutside = (e) => {
  if (menuWrapper.value && !menuWrapper.value.contains(e.target)) {
    isUserMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.header {
  background: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 20;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  direction: rtl;
}

.left,
.right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-title {
  font-size: 20px;
  color: #333;
}

.icon-btn {
  padding: 10px;
  border-radius: 8px;
  background: none;
  border: none;
  cursor: pointer;
  color: #555;
  transition: background 0.2s;
}

.icon-btn:hover {
  background: #f0f0f0;
}

.welcome {
  font-size: 14px;
  color: #555;
  border-left: 1px solid #ddd;
  padding-left: 12px;
  margin-left: 8px;
}

/* USER MENU */
.user-menu-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.user-menu {
  position: absolute;
  top: 48px;
  right: -30px;
  width: 180px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.12);
  padding: 10px 0;
  animation: fadeIn 0.2s ease;
  direction: rtl;
  z-index: 50;
}
.user-menu::before {
  content: '';
  position: absolute;
  top: -8px;
  right: 40px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid white;
  filter: drop-shadow(0px -1px 1px rgba(0, 0, 0, 0.1));
}

.menu-header {
  padding: 8px 14px;
  border-bottom: 1px solid #eee;
}

.user-name {
  display: block;
  font-size: 15px;
  font-weight: bold;
  color: #333;
}

.user-role {
  font-size: 12px;
  color: #777;
}

/* Menu buttons */
.menu-item {
  width: 100%;
  padding: 10px 14px;
  background: none;
  border: none;
  text-align: right;
  font-size: 14px;
  color: #444;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-item:hover {
  background: #f5f5f5;
}

.menu-item span {
  margin-left: 6px; /* RTL icon spacing */
}

.logout {
  color: #d9534f !important;
}

.logout:hover {
  background: #fde8e8;
}

/* Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
