# Frontend (Vue 3)

Application root: `front/manzoma/`

```
front/manzoma/
├── package.json          # scripts, engines, dependencies
├── vite.config.js        # plugins + @ alias
├── vitest.config.js      # jsdom test environment
├── jsconfig.json         # @/* → ./src/*
├── .prettierrc.json      # no semicolons, single quotes, width 100
├── .env / .env.development / .env.production
├── index.html            # entry document (lang="" → set this for RTL)
├── Dockerfile            # nginx image shipping a prebuilt dist/
├── docker/               # entrypoint.sh, nginx.conf, bundled Django static
├── public/               # favicon, icons.js, main.css, popup.css
└── src/
    ├── main.js           # createApp + pinia + router
    ├── App.vue           # GlobalLoader + <router-view>
    ├── api/              # axios client + per-resource modules
    ├── services/         # request shaping, loading/error wrapping
    ├── stores/           # Pinia
    ├── router/           # route modules + guard
    ├── layouts/          # MainAdminLayout, default, SemiAdminLayout
    ├── components/       # fields/, global/, layouts/, mainAdmin/
    ├── composables/      # useSocket, useBreadcrumbs, useSidebarRoutes…
    ├── utils/            # handleApiError, uiSettings, arabic utils
    ├── views/            # route screens
    └── __tests__/        # Vitest
```

## Quick start

```sh
cd front/manzoma
npm install
npm run dev
```

Vite prints the local URL (default `http://localhost:5173`; `vite.config.js` does not override host/port).

| Script | Command | Purpose |
| --- | --- | --- |
| `npm run dev` | `vite` | Dev server with HMR |
| `npm run build` | `vite build` | Production build → `dist/` |
| `npm run preview` | `vite preview` | Serve the built `dist/` locally |
| `npm run test:unit` | `vitest` | Unit tests (watch mode) |
| `npm run format` | `prettier --write src/` | Format sources |

Node engine: `^20.19.0 || >=22.12.0`.

## Stack and tooling

**Runtime**

| Package | Version | Used for |
| --- | --- | --- |
| `vue` | ^3.5.22 | UI framework (Composition API) |
| `vue-router` | ^4.6.3 | Routing |
| `pinia` | ^3.0.3 | State |
| `axios` | ^1.13.2 | HTTP |
| `@tailwindcss/vite`, `tailwindcss` | ^4.1.17 | Utility CSS (v4) |
| `bootstrap` | ^5.3.8 | Component CSS used by some views |
| `@fortawesome/fontawesome-free` | ^7.1.0 | Icons |
| `chart.js`, `vue-chartjs` | ^4.5.1 / ^5.3.3 | Charts |
| `exceljs`, `xlsx` | ^3.4.0 / ^0.18.5 | Excel export |
| `file-saver` | ^2.0.5 | Download triggers |
| `jspdf`, `jspdf-autotable` | ^4.1.0 / ^5.0.7 | PDF export (Arabic via bundled fonts) |
| `sweetalert` | ^2.1.2 | Dialogs |

**Dev**

`vite` ^7.1.11, `@vitejs/plugin-vue` ^6.0.1, `@vitejs/plugin-vue-jsx` ^5.1.1, `vite-plugin-vue-devtools` ^8.0.3, `vitest` ^3.2.4, `@vue/test-utils` ^2.4.6, `jsdom` ^27.0.1, `prettier` 3.6.2.

> ⚠️ **`html2canvas` is imported by several views and by `src/composables/useImageUtils.js` but is not declared in `package.json`.** It only appears as an optional transitive dependency, so a clean `npm install` can leave the import unresolved. Add it explicitly if you need PDF/image capture to build reliably.

**Vite config** (`vite.config.js`) — plugins `vue()`, `vueJsx()`, `vueDevTools()`, `tailwindcss()`; alias `@` → `./src`. No dev proxy and no build overrides.

**Vitest config** (`vitest.config.js`) — merges the Vite config with `environment: 'jsdom'`, excluding `e2e/**`.

**Prettier** — `{ semi: false, singleQuote: true, printWidth: 100 }`.

## Environment variables

Vite loads `.env` for every mode, then `.env.development` (for `npm run dev`) or `.env.production` (for `npm run build`), each overriding the base file. Use `.env.local` for machine-specific overrides (git-ignored).

| Variable | `.env` | `.env.development` | `.env.production` | Consumed at |
| --- | --- | --- | --- | --- |
| `VITE_API_BASE_URL` | `http://10.0.227.16:8080/api/v1` | `http://localhost:8080/api/v1` | `https://www.afrad.mil.eg/api/v1` | `src/api/http.js:14` (axios `baseURL`) |
| `VITE_MEDIA_BASE_URL` | `http://10.0.227.16:8080` | `http://localhost:8080/` | `https://www.afrad.mil.eg/` | `src/utils/glopal.js` (`getWsUrl`) |
| `VITE_SOCKET_BASE_URL` | `10.0.227.16:8080/` | `localhost:8080/` | `www.afrad.mil.eg/` | `src/composables/useSocket.js` |
| `VITE_WS_PROTOCOL` | `ws` | `ws` | `wss` | `src/composables/useSocket.js` |
| `VITE_APP_NAME` | `manzoma` | `manzoma` | `manzoma` | *unused* |
| `VITE_ENAPLE_LOGS` | `false` | `false` | `false` | *unused (typo: ENAPLE)* |

Notes:

- **Trailing slashes are inconsistent.** `VITE_MEDIA_BASE_URL` has a trailing slash in `.env.development`/`.env.production` but not in `.env`, while `VITE_SOCKET_BASE_URL` always has one. `getWsUrl` concatenates `${base}${path}` → double slashes in production. Normalise these (drop trailing slashes from `VITE_MEDIA_BASE_URL`, keep them consistent on the socket host).
- The HTTP client falls back to `http://localhost:3000/api` if `VITE_API_BASE_URL` is missing — that path does not match Django's `/api/v1/`, so set the variable explicitly.
- The default checked-in values point at a LAN host (`10.0.227.16`); for local work use `.env.development` or a local `.env.local`.

Example local override:

```dotenv
# front/manzoma/.env.local
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MEDIA_BASE_URL=http://localhost:8000
VITE_SOCKET_BASE_URL=localhost:8000/
VITE_WS_PROTOCOL=ws
```

## HTTP client

`src/api/http.js`

- `axios.create({ baseURL: VITE_API_BASE_URL, timeout: 10000, headers: { 'Content-Type': 'multipart/form-data' } })` — **the default content type is multipart**, so every JSON endpoint must pass `headers: { 'Content-Type': 'application/json' }` explicitly (the `uiSettings` module does this).
- **Request interceptor** — injects `Authorization: Bearer <token>` from `authStore.token`, creates an `AbortController` keyed `${method}:${url}` and attaches it as `config.signal`.
- **Response interceptor** — releases the controller; on error builds a message from `error.response?.data?.message` / `error.message`, retries **up to 2 extra times** only when no response was received (network error or timeout), then rethrows and logs `API Error:`.
- `cancelRequest(method, url)` releases a pending request. ⚠️ `src/api/modules/auth.js` calls it with a single config object, so that cancel path is a no-op.
- There is **no token refresh**: a 401 is handled in `src/utils/handleApiError.js`, which clears `localStorage` and routes to `/login`.

## API modules

`src/api/modules/*` — thin functions returning the raw axios promise. Services (`src/services/*`) wrap them with loading/error handling and unwrap `.data`.

### `auth.js`
| Export | Method + path |
| --- | --- |
| `login(credentials)` | `POST login/` |
| `logout()` | `POST logout` |
| `getProfile()` / `getProfileCancelable()` | `GET me` |

### `glopal.js`
| Export | Method + path |
| --- | --- |
| `getAllArmyRanks()` | `GET rank/` |
| `getAllArmyNames(params)` | `GET army/` (⚠️ raw params) |
| `getAllImageRejectionReasons()` | `GET rejection-reasons/` |
| `getAllPonsCons()` | `GET pons-cons/` |
| `getCommanderJobs()` | `GET commander-job/` |
| `getLagnaSpecificsPersonStutus(params)` | `GET lagna/person-status/` |

### `persons.js`
| Export | Method + path |
| --- | --- |
| `getPersons(params)` | `GET persons/` (⚠️ raw params) |
| `getUnits()` | `GET units/` |
| `getImagesReport()` | `GET get_images_report/` |
| `getPersonDetails(mil_ser, op)` | `GET person/{m}/?op={op}` |
| `getPersonInfo(mil_ser)` | `GET persons/{m}/` |
| `getLaganPersonInfo(mil_ser)` | `GET persons/{m}/?prnt_army=true` |
| `fetchBasicPersonInfo(mil_ser)` | `GET persons/{m}/?basic=1` |
| `postAttendance(mil_ser, payload)` | `POST attend_person/{m}/` |
| `checkPhotoReview(mil_ser, photo_id, payload)` | `POST persons/{m}/photos/{photo_id}/check/` |
| `getVote(mil_ser, vote_type, final_decision)` | `GET vote/{m}/?…` |
| `getLagnaStatistics(lagna_date)` | `GET get_lagna_statistics/?lagna_date={d}` |
| `getUploadedImagesReport(params)` / `getReviewedImagesReport(params)` | `GET report/` (⚠️ identical endpoints) |

⚠️ **Nine of these paths do not exist in the backend** — `logout`, `me`, `units/`, `get_images_report/`, `person/{m}/`, `attend_person/{m}/`, `vote/{m}/`, `get_lagna_statistics/` and `report/` all return 404. Full table in [api.md](api.md#gaps-frontend-calls-with-no-backend-route).

### `lagna.js` (largest)
CRUD for committees (`lagna/`), specific sessions (`lagna/{cc}/lagna-spacific…`), members, persons, decisions, statuses, snaps, reasons, opinions, votes, reports, plus lookups (`lagna/get-lagna-type/`, `lagna/get-lagna-category/`, `lagna-member/member-user/`, `lagna-member/member-type/`).

⚠️ `deleteLagnaSpecificsMembers` builds `lagna/ ${cc}/…` — a literal space (`lagna.js:36`) → 404.

### `opinions.js`
`GET opinion-types/?person_id=…`, and per-person `opinions/`, `opinions/add/`, `opinions/{oid}/delete/`, `votes/add/`.

### `personPhoto.js`
`GET photo/` (types) and `POST photo/` (multipart upload).

### `reasons.js`
`GET/POST …/reasons/…` plus `…/add-reason/` (GET/PATCH).

### `uiSettings.js`
Sections/fields CRUD + `reorder/`, and `GET ui-settings/pages/{page_key}/`.

> There is **no `api/modules/users.js`**, yet `src/stores/userStore.js` imports `usersApi` from it — that store is broken/dead.

## Router

`src/router/index.js` composes `auth` + `MainAdmin` + `SemiAdmin` + `errors` (the standalone `presentation` and `routes` modules are commented out; presentation routes live inside the MainAdmin tree). History mode with `scrollBehavior: { top: 0 }`. `/` → `/login`.

**Guard** (`router/index.js:22-36`):

1. `to.meta.requiresAuth && !isLoggedIn` → `/login`
2. `to.meta.role && user?.role !== to.meta.role` → `/login` ⚠️ compares `user.role` (singular) against a payload that carries `roles`
3. `to.meta.guest && isLoggedIn` → `/main-admin`
4. otherwise allow

### Route map

**Auth** (`router/modules/auth/index.js`)

| Path | Name | Component | Meta |
| --- | --- | --- | --- |
| `/login` | `Login` | `views/auth/Login.vue` | `guest: true` |

**Main admin** (`router/modules/MainAdmin/index.js`, layout `MainAdminLayout`)

| Path | Name | Component |
| --- | --- | --- |
| `/main-admin` | — | `MainAdminLayout` ⚠️ **default child is commented out → blank content area** |
| `/main-admin/afr-persons` | `AfrPersons` | `mainAdmin/afrPersons/Index.vue` |
| `/main-admin/afr-persons/profile/:id?/:person_name?/:committe_code?/:spacific_id?/:person_id?` | `AfrPersonProfile` | `mainAdmin/afrPersons/profile.vue` |
| `/main-admin/afr-persons/profile-image-upload/:id/:person_name` | `profileImageUpload` | `profileImageUpload.vue` |
| `/main-admin/afr-persons/reports` | `AfrPersonsReports` | `AfrpersonReports/index.vue` |
| `…/reports/uploaded-images-report` | `uploadedImagesReport` | `uploadedImagesReport/index.vue` |
| `…/reports/units-images-report/:prnt_army_code` | `unitsImagesReport` | `unitsImagesReport.vue` |
| `…/reports/persons-images-report/:prnt_army_code/:unit_code?/` | `personsImagesReport` | `personsImagesReport.vue` |
| `/main-admin/lagna` | `lagnaData` | `lagna/Index.vue` |
| `/main-admin/lagna/lagna-specific-data/:committe_code/:committe_name` | `lagaSpecificData` | `lagna/lagaSpecificData.vue` |
| `/main-admin/lagna/lagna-details/:committe_code?/:spacific_id?/:specific_name?/:committe_name` | `lagnaDetails` | `lagna/lagnaDetails.vue` |
| `/main-admin/lagna/lagna-details/specific-lagna-person-profile/:id?/…` | `specificLagnaPersonProfile` | `lagna/specificLagnaPersonProfile.vue` |
| `/main-admin/lagna/lagn-members` | `lagnaMembers` | `lagna/Index.vue` (same view) |
| `/main-admin/lagna/lagna-judg` | `lagnaJudg` | `lagna/Index.vue` (same view) |
| `/main-admin/reports` | `Reports` | `reports/index.vue` |
| `/main-admin/reports/commiti-report-data` | `commitiReportData` | `reports/commitiReportData/index.vue` |
| `/main-admin/settings` | `Settings` | `mainAdmin/Settings.vue` |
| `/presentation` | — | parent, `meta.sidebar: true` |
| `/presentation/lagnas-presenting` | `LagnasPresenting` | `presenting/index.vue` |
| `/presentation/presenting/:committe_code?/:committe_name?` | `presenting` | `presenting/presenting.vue` |
| `/presentation/admin-controle` | `AdminControle` | `AdminControle/index.vue` |
| `/presentation/admin-controle/admin-panel-window/:committe_code?/:committe_name?` | `AdminPanelWindow` | `AdminControle/AdminPanelWindow.vue` |

**Semi admin** (`router/modules/SemiAdmin/index.js`)

| Path | Name | Component | Meta |
| --- | --- | --- | --- |
| `/semi-admin` | — | `MainAdminLayout` | `requiresAuth`, `role: 'semiAdmin'` |
| `/semi-admin` (child `''`) | `semiIndex` | `semiAdmin/Index.vue` | |

**Errors** (`router/modules/errors/index.js`) — `/401` `Unauthorized`, `/403` `Forbidden`, `/500` `ServerError`, `/maintenance` `Maintenance`, and `/:pathMatch(.*)*` → `NotFound` (last).

⚠️ `meta.label` is a string on most routes but a function on a few (profile routes). `useBreadcrumbs.js` handles the function form; the sidebar does not.

## State (Pinia)

| Store | File | Responsibilities |
| --- | --- | --- |
| `loadingStore` | `stores/loadingStore.js` | `isLoading` / `activeRequests`, ref-counted `startLoading()`/`stopLoading()`; drives `GlobalLoader` |
| `authStore` | `stores/authStore.js` | `user` (parsed from `localStorage.user_data`), `token`, `isLoggedIn`, `hasRole`, `login`, `logout`, `fetchProfile`, `redirectByRole` |
| `glopal` | `stores/glopal.js` | Reference lists: `armyRanks`, `allArmyNames`, `ImageRejectionReasons`, `ponsCons`, `commanderJobs`, `lagnaStatus` |
| `lagna` | `stores/lagna.js` | **Largest store** — committees, specific sessions, members, persons, filters, pagination, snaps, WebSocket connect/disconnect for the presentation screen |
| `persons` | `stores/persons.js` | Person detail, opinions, reasons, opinion/vote types, filters |
| `useReportStore` | `stores/useReportStore.js` | Committee & photo report data, report pagination, report WebSocket |
| `uiSettings` | `stores/uiSettings.js` | Page → sections → fields cache with `sectionsOf`/`fieldsOf`/`isSectionVisible` getters |
| `useWebSocketStore` | `stores/useWebSocketStore.js` | Named socket registry: `connect(key, path, opts, params)`, `disconnect`, `disconnectAll` |
| `userStore` | `stores/userStore.js` | ⚠️ Broken — imports a non-existent `@/api/modules/users` |

Known store bugs (see [troubleshooting.md](troubleshooting.md#frontend)):

- `lagna.setLagnaPersonsFilters` and `lagna.setSpecificSort` call `fetchCommitts()` (wrong list).
- `lagna.disconnectLagnaPersonShowSocket` and `useReportStore.disconnectReportSocket` reference an out-of-scope `wsStore` → `ReferenceError`.
- `authStore.hasRole` dereferences `state.user.roles` without optional chaining → crashes when logged out.
- `lagna.fetchAllowedSpecificCommittPersons` is called with `{ params }` → double-nested query keys.

## Services

| File | Purpose |
| --- | --- |
| `services/lagnaService.js` | Wraps every `api/modules/lagna.js` call with `withLoading` + `handleApiError`, returns `.data` |
| `services/personsService.js` | Same for persons/opinions/reasons (⚠️ returns the **full** axios response for detail/mutation calls — inconsistent with list calls) |
| `services/glopal.js` | Reference-list fetchers, returns `.data` |
| `services/webSocketService.js` | `connect(key, path, options, params)` reuses open sockets by key, wraps them for loading state |

**Param wrapping is done here.** Passing a raw object where axios expects `{ params: … }` silently drops all query parameters — several call sites get this wrong (`fetchLagnaSpecifics`, `fetchSpecificLagnaMembers`, `fetchOneLagnaSpecificsPerson`, `fetchLagnaSpecificsPersonShow`).

## Composables

| File | Exports / behaviour |
| --- | --- |
| `composables/useSocket.js` | Builds the WS URL from `VITE_WS_PROTOCOL` + `VITE_SOCKET_BASE_URL` + path, reads the token from `localStorage`, handles open/error/close with reconnect and a heartbeat. Installs **no** `onmessage` — stores attach their own. |
| `composables/useSidebarRoutes.js` | Flattens the `/main-admin` route tree, keeps entries with `meta.sidebar`, maps label/icon |
| `composables/useBreadcrumbs.js` | Builds crumbs from `meta.label` (supports function labels) and `breadcrumbParent` |
| `composables/useSmartBack.js` | `router.back()` with a fallback when history is too short |
| `composables/useUiSettingsPage.js` | Section ordering + visibility for the profile and presenting pages; exports `PROFILE_PAGE_KEY`, `PRESENTING_PAGE_KEY` and their splitters |
| `composables/useImageUtils.js` | Screenshot/PDF helpers using global `html2canvas` and `window.jspdf` |
| `composables/useUsers.js` | ⚠️ imports `@/store/userStore` (wrong path) |

## Layouts and chrome

- **`layouts/MainAdminLayout.vue`** — fixed `Sidebar`, header, `<router-view>`, `Footer`; `dir="rtl"` throughout; content margin shifts with sidebar state; hides the sidebar chrome for the `presenting` route.
- **`layouts/default.vue`** — alternate layout; imports `Sidebar` without using it.
- **`layouts/SemiAdminLayout.vue`** — orphan; its unscoped `<style>` targets global `header`/`aside`/`main`.
- **`components/layouts/mainAdmin/Header.vue`** — icons from `public/icons.js`, user name/role from `authStore.user.info`, logout. ⚠️ `MainAdminLayout` binds `@toggle-sidebar` but `Header` emits nothing.
- **`components/layouts/mainAdmin/Sidebar.vue`** — mini/hover/lock modes, submenu expansion, active state via `route.path.startsWith`, logout.
- **`components/layouts/mainAdmin/Footer.vue`** — auto year, `dir="rtl"`.
- **Menu** comes from `src/composables/useSidebarRoutes.js`; `src/utils/buildSidebarMenu.js` exists but is unused.
- **Breadcrumbs** render through `components/global/pageNavigation.vue` (also hosts `SmartBack`).

### RTL and Arabic

`index.html` has `<html lang="">` (set to `ar` for correct rendering). Direction is forced in `public/main.css` and repeated as `dir="rtl"` on views/panels. The Cairo variable font is loaded via `@font-face` in `public/main.css` from `src/assets/fonts/Cairo-VariableFont_slnt,wght.ttf`. `src/utils/arabicUtils.js` and `src/utils/arabicFont.js` handle Arabic text shaping for PDF/export output.

## Views

| Area | Views | Notes |
| --- | --- | --- |
| **auth** | `auth/Login.vue` | Token in `authStore.token`; ⚠️ no `required` attributes and no visible error message |
| **afr persons** | `afrPersons/Index.vue` | Person list, filters, export (Excel/PDF), add/edit modal ⚠️ modal props don't match `AfrPersonModal`, row click is broken |
| | `afrPersons/profile.vue` (855 lines) | Full dossier: photos, opinions, reasons, decisions, dynamic UI sections |
| | `afrPersons/profileImageUpload.vue` | Photo type grid + upload + review workflow |
| | `AfrpersonReports/*` | Report landing page + uploaded-images/units/persons reports |
| **lagna** | `lagna/Index.vue` | Committee list (routed three times: `lagnaData`, `lagnaMembers`, `lagnaJudg`) |
| | `lagna/lagaSpecificData.vue` (1,244 lines) | Specific sessions, members, persons tabs, photo report modal |
| | `lagna/lagnaDetails.vue` | Persons + members of a session |
| | `lagna/specificLagnaPersonProfile.vue` (1,944 lines) | Person-in-committee profile: photos, opinions, reasons, decision |
| | `lagna/UnFitnessReportModal.vue` | jsPDF fitness report |
| **reports** | `reports/index.vue`, `reports/commitiReportData/index.vue` | Committee statistics ⚠️ sorting reassigns a ref to a Promise |
| **settings** | `mainAdmin/Settings.vue` (637 lines) | UI section/field editor — the most complete view |
| **presentation** | `presenting/index.vue` → `presenting/presenting.vue` (2,824 lines) | Projection screen driven by WebSocket events |
| | `AdminControle/index.vue` → `AdminPanelWindow.vue` (788 lines) | Committee control panel |
| **semi admin** | `semiAdmin/Index.vue` | Dashboard with hard-coded mock figures |
| **errors** | `errors/Unauthorized|Forbidden|ServerError|Maintenance|NotFound.vue` | `BaseError` variants |
| **orphans** | `HomeView.vue`, `AdminControl.vue`, `atteendReport.vue`, `presenting7.vue`, `presenting7 copy.vue`, `mainAdmin/Index.vue`, `mainAdmin/Users.vue`, `lagna/lagnaData.vue`, `lagna/lagnaMembers.vue`, `semiAdmin/{Lagna,Users,Reports,Settings}.vue` | Not referenced by the router |

## Components

**`components/fields/`** — `glopalSearch`, `searchField`, `selectField`, `searchableSelectField`, `dateField`, `dateRangeField`, `exportBtns`.

**`components/global/`** — `GlobalLoader`, `ModalOverlay`, `BackToTop`, `SmartBack`, `pageNavigation`, `screenfull`.

**`components/global/dataTable/`** — the reusable data layer:

| Component | Role |
| --- | --- |
| `BaseTable.vue` | Config-driven table: `columns` (`prop`, `label`, `render`, `copyable`, `notRowClick`), `rowClick`, footer button slot |
| `TablePagination.vue` | Paging controls |
| `BaseModalForm.vue` | `v-model` field-driven modal form |
| `BaseTableModalSelect.vue` | Modal with row selection |

**`components/global/popup/`** — 25 popups used mainly by `presenting.vue` and the profiles: `acceptpop`, `consistancyPopup`, `courses`, `courtPopup`, `descitionNotesPopup`, `eff_report`, `finalDecition`, `historyPopup`, `inspireWorkShow`, `medicalPopup`, `past-units`, `Poea`, `reasonsPopup`, `Rejectpop` (unused), `relationPopup`, `report`, `reportPopub`, `sec-person`, `StartVotingPopup`, `TraqPopup`, `travelPopup`, `UpdatePopup`, `VacationPopup`, `votingDataPopup`, `reasonsPopup copy.vue` (unused).

**`components/mainAdmin/`** — feature groups: `AfrPersons/*` (modal, upload panel, profile blocks), `profileImageUpload/*` (add/zoom/review), `lagna/*` (controls, tables, modal, members, persons), `users/*` (controls, table, modal), `StateCard.vue`, `dataTableStatistic.vue` (unused).

**`components/layouts/mainAdmin/`** — `Header`, `Sidebar`, `Footer`.

## WebSockets

Chain: view/store → `useWebSocketStore.connect(key, path, options, params)` → `webSocketService.connect()` → `useSocket()` → `socketLoadingWrapper`.

- URL is built in `useSocket.js` as `protocol://host + protocol + path + ?token=…`. ⚠️ Because the checked-in `VITE_SOCKET_BASE_URL` ends with `/`, the protocol gets duplicated into the path (e.g. `…/wss/lagna/`) — fix the env value or the builder before relying on sockets.
- The token comes from `localStorage.token`, set by `authStore.login`.
- `socketLoadingWrapper` overrides `onopen`, which means the heartbeat from `useSocket` never runs through the service path.
- Stores assign `onmessage` after connecting (`lagna.js`, `useReportStore.js`).

**Event protocol** consumed by `presenting/presenting.vue`: `show_person`, `vote`, `settings`, `comm_report`, `pong`, `relation`, `punish`, `relation_approx`, `punish_approx`, `shhh`, `refresh`, `takeScreen`, `end`, `close`, and a default branch that opens a popup.

Backend-side groups and paths are documented in [architecture.md](architecture.md#realtime-topology) and [api.md](api.md#websockets).

## Styling and assets

- **Tailwind 4** imported in `public/main.css` via `@import "tailwindcss"` (the plugin also handles source detection).
- `public/main.css` also sets `unicode-bidi: bidi-override`, `user-select: none`, the `@font-face` for Cairo, and `main { z-index: -1 }` — review these before adding stacked overlays.
- `public/popup.css` holds popup-specific overrides.
- Icons: Font Awesome CSS plus inline SVG strings from `public/icons.js`.
- Image assets: `src/assets/Images/`, `src/assets/404_images/`.
- ⚠️ `src/assets/libs/tailwindcss.js` is a vendored full Tailwind browser build that is not referenced — it only inflates the bundle.

## Tests

`src/__tests__/App.spec.js` mounts `App.vue` and asserts the text `"You did it!"` — **stale**: `App.vue` renders only `GlobalLoader` + `<router-view>`, so the assertion fails today. There are no component, store, or router tests.

```sh
npm run test:unit        # watch mode
npx vitest run           # single pass (use this in CI)
```

## Docker

`front/manzoma/Dockerfile` does **not** build the SPA — it copies an existing `dist/`:

```dockerfile
from nginx
copy ./dist /user/share/nginx/html      # ⚠️ typo: /user instead of /usr
copy docker/static /static/
copy docker/nginx.conf /etc/nginx/conf.d/default.conf
copy docker/entrypoint.sh /entrypoint.sh
run chmod +x /entrypoint.sh
cmd ["/entrypoint.sh"]
```

Build order: `npm run build` → `docker build .`. See [deployment.md](deployment.md).

## Related

- [api.md](api.md) — endpoints and WebSocket protocol
- [development.md](development.md) — local workflows
- [troubleshooting.md](troubleshooting.md) — known frontend issues
