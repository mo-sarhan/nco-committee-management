import { createRouter, createWebHistory } from 'vue-router'
import mainAdminRoutes from './modules/MainAdmin/index'
import semiAdminRoutes from './modules/SemiAdmin/index'
import errors from './modules/errors/index'
// import presentation from './modules/presentation/index'
import auth from './modules/auth/index'
// import glopalRoutes from './modules/routes'
import { useAuthStore } from '@/stores/authStore'

const routes = [
  ...auth,
  // ...glopalRoutes,
  ...mainAdminRoutes,
  ...semiAdminRoutes,
  ...errors,
  // ...presentation,
  { path: '/', redirect: '/login' },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) return next('/login')

  if (to.meta.role && !authStore.hasRole(to.meta.role)) {
    return next('/login') // redirect if role mismatch
  }

  // if (to.meta.guest && authStore.isLoggedIn) return next(`/${authStore.user.role}-admin`);
  // if (to.meta.guest && authStore.isLoggedIn) return next(`/presentation/admin-controle`);
  if (to.meta.guest && authStore.isLoggedIn) return next(`/main-admin`)

  next()
})

export default router
