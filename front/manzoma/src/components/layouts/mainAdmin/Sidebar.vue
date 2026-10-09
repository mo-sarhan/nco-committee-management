<template>
  <div
    class="sidebar"
    :class="{
      mini: !isOpen && !isHover,
      hover: isHover && !isOpen,
      open: isOpen,
      hiden: route.name == 'presenting',
    }"
    @mouseenter="isHover = true"
    @mouseleave="isHover = false"
    dir="rtl"
  >
    <!-- HEADER -->
    <div class="header" :style="miniMode ? 'justify-content: center;' : ''">
      <h1 v-if="!miniMode" class="logo">لوحة تحكم المدير</h1>
      <button @click="toggleLock" class="toggle-btn">
        <span v-if="!isOpen">☰</span>
        <span v-else>✕</span>
      </button>
    </div>

    <!-- MENU -->
    <nav class="menu">
      <div v-for="item in navItems" :key="item.title">
        <!-- PARENT WITH CHILDREN -->
        <div
          v-if="item.children"
          class="menu-item"
          :class="{ active: isParentActive(item) }"
          @click="toggleSubmenu(item.title)"
          :style="miniMode ? 'justify-content:center' : ''"
        >
          <span class="menu-icon" v-html="item.icon"></span>
          <span v-if="!miniMode" class="text">{{ item.title }}</span>
          <span
            v-if="!miniMode"
            class="arrow"
            :style="{ transform: isMenuOpen(item.title) ? 'rotate(180deg)' : '' }"
          >
            ▾
          </span>
        </div>

        <div v-if="item.children && isMenuOpen(item.title) && !miniMode" class="submenu">
          <router-link
            v-for="child in item.children"
            :key="child.name"
            :to="{ name: child.name }"
            class="submenu-item"
            :class="{ active: isRouteActive(child.name) }"
          >
            {{ child.title }}
          </router-link>
        </div>

        <!-- SINGLE ITEM -->
        <router-link
          v-else-if="!item.children"
          :to="{ name: item.name }"
          class="menu-item"
          :class="{ active: route.name === item.name }"
          :style="miniMode ? 'justify-content: center;' : ''"
        >
          <span class="menu-icon" v-html="item.icon"></span>
          <span v-if="!miniMode" class="text">{{ item.title }}</span>
        </router-link>
      </div>
    </nav>

    <!-- LOGOUT -->
    <div class="logout">
      <button class="logout-btn" @click="logout">
        <span class="icon" v-html="icons.LogOut"></span>
        <span v-if="!miniMode" class="text">تسجيل الخروج</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { icons } from '../../../../public/icons'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useSidebarRoutes } from '@/composables/useSidebarRoutes'

const { sidebarRoutes: navItems } = useSidebarRoutes()
const authStore = useAuthStore()
const logout = authStore.logout

const props = defineProps({
  isOpen: Boolean,
})
const emit = defineEmits(['toggle-sidebar'])

const route = useRoute()
const isHover = ref(false)
const openMenus = ref([])

const miniMode = computed(() => !props.isOpen && !isHover.value)

const toggleLock = () => emit('toggle-sidebar')

// single route active
const isRouteActive = (name) => route.name === name

// parent active if ANY child is active
const isParentActive = (item) => item.children?.some((child) => child.name === route.name)

// submenu open
const isMenuOpen = (title) => openMenus.value.includes(title)

const toggleSubmenu = (title) => {
  if (isMenuOpen(title)) {
    openMenus.value = []
  } else {
    openMenus.value = [title]
  }
}

onMounted(() => {
  console.log('route.name', route.name)
})
watch(
  () => route.name,
  () => {
    const parent = navItems.value.find((item) => item.children?.some((c) => c.name === route.name))
    openMenus.value = parent ? [parent.title] : []
  },
  { immediate: true },
)
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  background: #1f2937;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden;
  z-index: 200;
}

/* MODES */
.sidebar.mini {
  width: 70px;
}
.sidebar.hiden {
  width: 0px;
}
.sidebar.hover {
  width: 260px;
}
.sidebar.open {
  width: 260px;
}

/* HEADER */
.header {
  background: #111827;
  padding: 23px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #374151;
}

.logo {
  font-size: 17px;
  font-weight: bold;
}
.toggle-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 22px;
  cursor: pointer;
}
.toggle-btn:hover {
  color: white;
}

/* MENU */
.menu {
  flex: 1;
  margin-top: 10px;
}
.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: #d1d5db;
  border-bottom: 1px solid #374151;
  transition: background 0.2s;
  text-decoration: none;
}
.menu-item:hover {
  background: #374151;
  color: #fff;
  cursor: pointer;
}
.menu-item.active {
  background: #4b5563;
  color: #fff;
  font-weight: bold;
  border-right: 15px solid var(--primary-color);
}
/* Rotate arrow when submenu is open */
.menu-item.active .arrow {
  color: var(--primary-color);
  transform: rotate(180deg);
}
.menu-icon {
  min-width: 24px;
}
.text {
  white-space: nowrap;
}

/* SUBMENU */
.submenu {
  background: #111827; /* dark base */
  padding-right: 24px; /* indent from parent */
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease; /* smooth open */
}
.submenu-item {
  display: block;
  padding: 10px 16px;
  text-decoration: none;
  font-size: 14px;
  margin: 4px 0;
  color: #cbd5e1;
  border-radius: 6px;
  transition: all 0.2s ease;
}
.submenu-item:hover {
  background: #1f2937;
  color: #fff;
}
.submenu-item.active {
  color: white;
  font-weight: bold;
  background: #374151;
}
.arrow {
  margin-right: auto;
  font-size: 15px;
  opacity: 0.9;
  transition: transform 0.3s ease;
}
/* LOGOUT */
.logout {
  padding: 15px;
  border-top: 1px solid #374151;
}
.logout-btn {
  width: 100%;
  padding: 12px 16px;
  background: #b91c1c33;
  border: none;
  border-radius: 6px;
  color: #fca5a5;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.logout-btn:hover {
  background: #7f1d1d66;
}
</style>
