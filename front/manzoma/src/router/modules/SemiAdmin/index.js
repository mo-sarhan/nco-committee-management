import MainAdminLayout from '@/layouts/MainAdminLayout.vue'
import Index from '@/views/semiAdmin/Index.vue'

export default [
  {
    path: '/semi-admin',
    component: MainAdminLayout,
    meta: { requiresAuth: true, role: 'semiAdmin' },
    children: [
      {
        path: '',
        name: 'semiIndex',
        component: Index,
      },
    ],
  },
]
