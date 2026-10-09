import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export function useBreadcrumbs() {
  const route = useRoute()
  const router = useRouter()

  const breadcrumbs = computed(() => {
    let matched = [...route.matched]

    const last = matched[matched.length - 1]

    // Inject breadcrumbParent manually
    if (last?.meta?.breadcrumbParent) {
      const parent = router.getRoutes().find(
        r => r.name === last.meta.breadcrumbParent
      )

      if (parent) {
        matched.splice(matched.length - 1, 0, parent)
      }
    }

    return matched
      .filter(r => r.meta?.label)
      .map(r => {
        let path = null

        if (r.name) {
          try {
            // ✅ Extract only params required by that route
            const requiredParams = r.path.match(/:(\w+)/g)?.map(p =>
              p.replace(':', '').replace('?', '')
            ) || []

            const filteredParams = {}

            requiredParams.forEach(param => {
              if (route.params[param]) {
                filteredParams[param] = route.params[param]
              }
            })

            path = router.resolve({
              name: r.name,
              params: filteredParams
            }).href
          } catch (e) {
            path = null
          }
        }

        return {
          label:
            typeof r.meta.label === 'function'
              ? r.meta.label(route)
              : r.meta.label,
          path
        }
      })
  })

  return { breadcrumbs }
}
