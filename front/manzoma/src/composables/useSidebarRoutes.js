import { useRouter } from 'vue-router'
import { computed } from 'vue'

export function useSidebarRoutes() {
  const router = useRouter()

  const sidebarRoutes = computed(() => {
    const main = router.options.routes.find(r => r.path === '/main-admin' )

    return main.children
      .filter(r => r.meta?.sidebar)
      .map(parent => {
        if (!parent.children) {
          return {
            title: parent.meta.label,
            name: parent.name,
            icon: parent.meta.icon,
          }
        }

        return {
          title: parent.meta.label,
          icon: parent.meta.icon,
          children: parent.children
            .filter(c => c.meta?.sidebar)
            .map(c => ({
              title: c.meta.label,
              name: c.name,
            })),
        }
      })
  })

  return { sidebarRoutes }
}
