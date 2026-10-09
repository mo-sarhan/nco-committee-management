import { icons } from '../../../../public/icons'
import Unauthorized from '@/views/errors/Unauthorized.vue'
import Forbidden from '@/views/errors/Forbidden.vue'
import ServerError from '@/views/errors/ServerError.vue'
import Maintenance from '@/views/errors/Maintenance.vue'
import NotFound from '@/views/errors/NotFound.vue'

export default [
  {
    path: '/401',
    component: Unauthorized,
  },
  {
    path: '/403',
    component: Forbidden,
  },
  {
    path: '/500',
    component: ServerError,
  },
  {
    path: '/maintenance',
    component: Maintenance,
  },

  // 🔥 404 MUST BE LAST
  {
    path: '/:pathMatch(.*)*',
    component: NotFound,
  },
]
