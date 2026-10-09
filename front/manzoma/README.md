# manzoma — frontend

Vue 3 single-page application for **NCO Manzoma (منظومة NCO)**: personnel records, committee (لجان) workflows, a real-time presentation screen, photo review and reports.

Deep documentation: [docs/frontend.md](../../docs/frontend.md) · [docs/README.md](../../docs/README.md)

## Setup

Node `^20.19.0 || >=22.12.0`.

```sh
npm install
npm run dev
```

Vite serves `http://localhost:5173` with HMR.

### Environment

Create `.env.local` in this directory to point at your backend:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MEDIA_BASE_URL=http://localhost:8000
VITE_SOCKET_BASE_URL=localhost:8000/
VITE_WS_PROTOCOL=ws
```

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | REST API base (Django mounts `/api/v1/`) |
| `VITE_MEDIA_BASE_URL` | Media/photo host — **no trailing slash** |
| `VITE_SOCKET_BASE_URL` | WebSocket host, e.g. `localhost:8000/` |
| `VITE_WS_PROTOCOL` | `ws` or `wss` |
| `VITE_APP_NAME`, `VITE_ENAPLE_LOGS` | Present but unused |

Precedence: `.env` → `.env.development` (dev) / `.env.production` (build) → `.env.local`.

## Scripts

| Command | What it does |
| --- | --- |
| `npm run dev` | Dev server with HMR |
| `npm run build` | Production build → `dist/` |
| `npm run preview` | Serve the built `dist/` locally |
| `npm run test:unit` | Vitest in watch mode (`npx vitest run` for a single pass) |
| `npm run format` | Prettier — no semicolons, single quotes, width 100 |

## Structure

```
src/
├── api/         # axios client (api/http.js) + per-resource modules
├── services/    # request shaping, loading + error wrapping
├── stores/      # Pinia: auth, lagna, persons, reports, uiSettings, loading
├── router/      # route modules (MainAdmin, SemiAdmin, auth, errors) + guard
├── layouts/     # MainAdminLayout, default, SemiAdminLayout
├── components/  # fields/, global/ (+ dataTable, popup), layouts/, mainAdmin/
├── composables/ # useSocket, useBreadcrumbs, useSidebarRoutes, useUiSettingsPage
├── utils/       # handleApiError, uiSettings, arabicUtils
├── views/       # route screens
└── __tests__/   # Vitest specs
```

Conventions:

- **URLs** live in `src/api/modules/` — never inline them in views.
- **Query params** are wrapped as `{ params }` inside `src/services/`.
- **Shared state** belongs in a Pinia store; page state stays local.
- **Reusable markup** goes in `src/components/` (`BaseTable`, `BaseModalForm`, `TablePagination`, `ModalOverlay`).
- Use the `@/` alias (`@` → `src`).

## Building for Docker

The `Dockerfile` does **not** build the SPA — it copies a prebuilt `dist/`:

```sh
npm run build
docker build -t manzoma-web .
```

Details: [docs/deployment.md](../../docs/deployment.md).

## Known issues

Before working here, read [docs/troubleshooting.md](../../docs/troubleshooting.md). Highlights:

- `html2canvas` is imported by several views but **not declared** in `package.json` — add it if the build fails.
- Nine API calls target endpoints the backend does not serve ([list](../../docs/api.md#gaps-frontend-calls-with-no-backend-route)).
- WebSocket URL building, login redirects and a few store actions have known bugs.
- `src/__tests__/App.spec.js` asserts stale content and fails as-is.

## IDE

[VS Code](https://code.visualstudio.com/) + the [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) extension (disable Vetur), plus the [Vue.js devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) browser extension.
