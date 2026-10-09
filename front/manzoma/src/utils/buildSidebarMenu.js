export function buildSidebarMenu(routes, basePath = '') {
  return routes
    .filter(r => r.meta?.menu)
    .map(r => {
      const fullPath = r.path.startsWith('/')
        ? r.path
        : `${basePath}/${r.path}`.replace('//', '/')

      const item = {
        title: r.meta.label,
        name: r.name,
        icon: r.meta.icon,
        path: fullPath,
      }

      if (r.children) {
        const children = buildSidebarMenu(r.children, fullPath)
        if (children.length) {
          item.children = children
        }
      }

      return item
    })
}
