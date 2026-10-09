import { defineStore } from 'pinia'
import { authApi } from '@/api/modules/auth'
import router from '@/router'
import swal from 'sweetalert'
import { withLoading } from '@/api/utils/apiWrapper'

function readStoredUser() {
  try {
    return JSON.parse(localStorage.getItem('user_data')) || null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: readStoredUser(),
    token: localStorage.getItem('token') || null,
  }),

  // ===================== ACTIONS =====================
  actions: {
    async login(credentials) {
      try {
        const data = await withLoading(() => authApi.login(credentials))

        if (data) {
          this.token = data.data.access
          localStorage.setItem('token', this.token)

          const userPayload = {
            info: data.data.info,
            roles: data.data.role || [], // always array
          }

          this.user = userPayload
          localStorage.setItem('user_data', JSON.stringify(userPayload))
        }

        if (this.user) {
          this.redirectByRole()
        }
      } catch (error) {
        console.error('Login error:', error)

        if (error.response) {
          const statusCode = error.response.status

          if (statusCode === 400 || statusCode === 401) {
            swal({
              title: 'خطأ!',
              text: 'كلمة السر أو اسم المستخدم غير صحيح',
              icon: 'error',
              button: false,
              timer: 10000,
            })
          } else if (statusCode === 500) {
            swal({
              title: 'خطأ!',
              text: 'حدثت مشكلة في الخادم. حاول مرة أخرى لاحقًا.',
              icon: 'error',
              button: false,
              timer: 10000,
            })
          } else {
            swal({
              title: 'خطأ!',
              text: `خطأ غير معروف (${statusCode})`,
              icon: 'error',
              button: false,
              timer: 10000,
            })
          }
        } else if (error.request) {
          swal({
            title: 'خطأ!',
            text: 'تحقق من اتصال الشبكة أو عنوان الخادم.',
            icon: 'error',
            button: false,
            timer: 10000,
          })
        } else {
          swal({
            title: 'خطأ!',
            text: 'خطأ غير متوقع أثناء تسجيل الدخول.',
            icon: 'error',
            button: false,
            timer: 10000,
          })
        }
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user_data')
      authApi.logout().catch(() => {})
      router.push('/login')
    },

    async fetchProfile() {
      if (!this.token) return

      const profile = await authApi.getProfile()
      const data = profile.data

      const userPayload = {
        info: data?.info ?? null,
        roles: data?.role || data?.roles || [],
      }

      this.user = userPayload
      localStorage.setItem('user_data', JSON.stringify(userPayload))
    },

    // ===================== ROLE REDIRECT =====================
    redirectByRole() {
      if (!this.user?.roles) {
        router.push('/login')
        return
      }

      if (this.hasRole('admin')) {
        router.push('/main-admin')
      } else if (this.hasRole('report')) {
        router.push('/main-admin/reports')
      } else if (this.hasRole('show')) {
        router.push('/presentation/lagnas-presenting')
      } else {
        router.push({ name: 'AfrPersons' })
      }
    },
  },

  // ===================== GETTERS =====================
  getters: {
    isLoggedIn: (state) => !!state.token,

    getUserInfo: (state) => state.user?.info || null,

    getRoles: (state) => state.user?.roles || [],

    getMemberName: (state) => state.user?.info?.member_name || 'Guest',

    isSuperuser: (state) => state.user?.roles?.includes('superuser'),

    // ---- Role Checkers ----
    hasRole: (state) => (roleName) => state.user?.roles?.includes(roleName) ?? false,

    hasAnyRole: (state) => (rolesArray) => {
      if (!state.user?.roles) return false
      return rolesArray.some((role) => state.user.roles.includes(role))
    },

    hasAllRoles: (state) => (rolesArray) => {
      if (!state.user?.roles) return false
      return rolesArray.every((role) => state.user.roles.includes(role))
    },
  },
})
