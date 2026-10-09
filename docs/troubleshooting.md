# Troubleshooting and known issues

Collected issues found while documenting the repository, with file references. Grouped by severity. Nothing here has been fixed yet — this is a work list.

## Backend

### Settings package is empty

**Symptom** — `python manage.py …` fails with `ImproperlyConfigured: You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure()` or a missing-database error.

`manage.py:9`, `nco/wsgi.py:14` and `nco/asgi.py:12` all default to `nco.settings`, but `nco/settings/__init__.py` is **empty** and imports nothing.

**Fix** — always pass an explicit module:

```sh
python manage.py migrate --settings=nco.settings.sqlite_set
```

or export `DJANGO_SETTINGS_MODULE=nco.settings.sqlite_set`.

### `oracle.py` has no default database

`nco/settings/oracle.py` replaces `DATABASES` with only `oracledb` and `sqlite` aliases — **no `default` key**. Django cannot resolve a default connection with that module. Add a `default` entry before use.

### Celery initialisation

- `nco/celery.py:4` forces `DJANGO_SETTINGS_MODULE='nco.settings.production'`.
- `nco/__init__.py` has `from .celery import app as celery_app` **commented out**, while `__all__ = ['celery_app']` remains — so `manage.py` never loads the Celery app.
- `apps/schadule/celery.py:4` uses `project.settings`, a module that does not exist, and creates a second app named `project`.

**Workaround** — run workers with `celery -A nco.celery worker -l info` (explicit app path).

### Broken management-command package

`apps/customadmin/management/__init___.py` has **three** trailing underscores instead of `__init__.py`. Without a valid package init, Django may not discover `dumps` / `upload_opinions`. Rename the file to `__init__.py` (and remove the stray one).

### Empty migrations package

`backend/nco/apps/api/v1/migrations/` contains only `__init__.py`. Harmless while `apps.api.v1` defines no models, but `makemigrations` on that app will always report nothing to do.

### Permissive committee permission

`apps/lagna/permissions.py` — `AllowToAddOrEditPerson.has_permission()` returns `True` unconditionally; only the object-level check runs. Any authenticated user can attempt the action.

### Hardcoded secrets in source

| Location | Value type |
| --- | --- |
| `nco/settings/base.py:24` | `SECRET_KEY` (also the JWT signing key) |
| `nco/settings/base.py:231-233` | S3 access key / secret (placeholder `test`) |
| `nco/settings/dev.py` | PostgreSQL password |
| `nco/settings/production.py` | PostgreSQL + Oracle passwords |
| `nco/settings/sqlite_set.py`, `oracle.py` | Oracle password |
| `backend/docker-compose.yml:54-55` | pgAdmin email/password |
| `apps/photos/services/check_nsfw_photo.py:46` | `Bearer your_token_here` placeholder |

**Rotate and externalise all of these** before any real deployment.

### `DEBUG` defaults to true

`base.py:27` sets `DEBUG = True` and every environment module inherits from it. Only `production.py`/`oracle.py` flip it off.

### Production database host

`nco/settings/production.py` defines `default` as **SQLite** while PostgreSQL sits in a `postgres` alias with `host: 'localhost:5432'` (lower-case keys). Pick the intended default explicitly.

### No default DRF pagination class

`REST_FRAMEWORK` sets `PAGE_SIZE = 20` but leaves `DEFAULT_PAGINATION_CLASS` commented out, so page sizes and response envelopes differ per viewset. Pass the explicit paginator or expect inconsistency.

### `django-filter` referenced but not installed

`backend/requirement.txt` does not list `django-filter`, yet filtering helpers are used in places. Check imports; add the package if required.

### No beat schedule

There is no `CELERY_BEAT_SCHEDULE`, so nothing runs on a schedule. Add one if periodic reports are expected.

### Stale files

- `nco/nco/refrence.py` (352 lines) — not imported anywhere; appears to be scratch.
- `apps/schadule/` — empty placeholder app, not in `INSTALLED_APPS`.
- `apps/person/models.py` — `FamilyManager` filter lists are placeholders with incomplete logic.
- `apps/customadmin/.../upload_opinions.py:113-124` — image attachment code is commented out.
- `apps/photos/management/commands/create_afr_photo_report.py` — empty stub.

## Frontend

### Login redirect goes nowhere / blank page

- `src/stores/authStore.js:111-120` (`redirectByRole`) pushes route names `MainAdmin`, `ReportPage`, `ShowPage` — **none of these names exist**. Admin/report/show users can end up stuck on `/login`.
- `src/router/modules/MainAdmin/index.js:38-48` — the default child of `/main-admin` is **commented out**, so `/main-admin` renders an empty content area.
- `src/router/index.js:27` — the guard compares `authStore.user?.role` (singular) while the payload carries `roles`; `modules/SemiAdmin/index.js` requires `role: 'semiAdmin'`, so `/semi-admin` bounces to `/login`.

### WebSockets fail end to end

- `src/composables/useSocket.js:24` builds `protocol://host + protocol + path`. With `VITE_SOCKET_BASE_URL` ending in `/`, the protocol lands in the path: `ws://host:8080/ws/lagna/?…` / `wss://www.afrad.mil.eg/wss/lagna/`. Fix the env value (drop the trailing slash) or the builder.
- `src/stores/lagna.js:554-556` and `src/stores/useReportStore.js:166-168` reference an out-of-scope `wsStore` → **`ReferenceError` on disconnect**. In `presenting.vue:2306-2309` that throws before `removeEventListener`, leaking the listener and leaving the socket open.
- `src/api/utils/socketLoadingWrapper.js:14` overrides `onopen`, so the heartbeat installed by `useSocket` never runs through the service path.
- `useReportStore.js:144-161` reads `event.type` (always `'message'`) instead of the event name, so the `pong` / `report:update` / `report:summary` branches are unreachable.

### Query parameters silently dropped

axios expects `{ params: … }`. These pass a raw object, so every filter/page is lost:

- `src/services/lagnaService.js:142` `fetchLagnaSpecifics`
- `src/services/lagnaService.js:240` `fetchSpecificLagnaMembers`
- `src/services/lagnaService.js:198` `fetchOneLagnaSpecificsPerson`
- `src/services/lagnaService.js:359` `fetchLagnaSpecificsPersonShow`
- `src/api/modules/persons.js:3` `getPersons`
- `src/api/modules/glopal.js` `getAllArmyNames`

Conversely `src/stores/lagna.js:714,721` call `fetchAllowedSpecificCommittPersons({ params })`, producing double-nested `params[page]=…` keys.

### 404s and wrong URLs

- `src/api/modules/lagna.js:36` — `deleteLagnaSpecificsMembers` builds `lagna/ ${cc}/…` with a **literal space** → 404.
- `src/api/modules/persons.js:17-18` — `getUploadedImagesReport` and `getReviewedImagesReport` hit the same `report/` endpoint (same data).
- `src/views/mainAdmin/afrPersons/Index.vue:234` — Excel export fetches `/logo.png`, which is not in `public/` → 404.
- `src/views/mainAdmin/afrPersons/AfrpersonReports/uploadedImagesReport/index.vue:166` — raw `axios.get('get_images_report/?excel=yes')` uses a relative URL → hits the frontend origin.
- `src/components/mainAdmin/AfrPersons/profile/OpinionsSection.vue` — `getFileUrl` builds `/media/…` against the frontend instead of `VITE_MEDIA_BASE_URL`.

### Frontend endpoint mismatches

These requested paths have **no route in the backend** and return 404 (full table in [api.md](api.md#gaps-frontend-calls-with-no-backend-route)):

| Path | Requested by |
| --- | --- |
| `POST /api/v1/logout` | `auth.js:7` |
| `GET /api/v1/me` | `auth.js:8,13` |
| `GET /api/v1/units/` | `persons.js:4` |
| `GET /api/v1/get_images_report/` | `persons.js:5` |
| `GET /api/v1/person/<id>/` | `persons.js:6` |
| `POST /api/v1/attend_person/<id>/` | `persons.js:10` |
| `GET /api/v1/vote/<id>/` | `persons.js:12` |
| `GET /api/v1/get_lagna_statistics/` | `persons.js:13` |
| `GET /api/v1/report/` | `persons.js:17-18` (only `/report/lagna/` exists) |

Note the photo report prefix: `report_router` is mounted under `photo/`, so the correct path is `/api/v1/photo/report/`, not `/api/v1/report/`.

### Auth and state bugs

- `src/stores/authStore.js:141` — `hasRole` dereferences `state.user.roles` without `?.` → **crashes when logged out** (used by `profileImageUpload.vue:60`, `specificLagnaPersonProfile.vue:477`, `personsImagesReport.vue:41,66`).
- `src/stores/authStore.js:9` — unguarded `JSON.parse(localStorage.getItem('user_data'))`.
- `src/stores/authStore.js:95-101` — `fetchProfile` overwrites the `{info, roles}` user shape.
- `src/api/http.js:61-68` vs `src/api/modules/auth.js:12-14` — `cancelRequest(method, url)` is called with a single config object → cancel is a no-op.
- `src/utils/handleApiError.js:8-11` — 401 handler calls `localStorage.clear()`, wiping unrelated keys.
- `src/stores/userStore.js:2` imports `usersApi` from a module that does not exist → store broken; `src/composables/useUsers.js:3` imports `@/store/userStore` (wrong path).

### Store actions hitting the wrong list

- `src/stores/lagna.js:696` `setLagnaPersonsFilters` and `:739` `setSpecificSort` call `fetchCommitts()` (the committee list) instead of the person/specific list.
- `src/views/mainAdmin/reports/commitiReportData/index.vue:172` — `setSort` assigns a **Promise** to the `commitiReportData` ref, breaking the table; it also reads `filters.sortBy` off the ref instead of `.value`.
- `src/stores/lagna.js:749` — `clearCurrent` sets an undeclared `currentPerson`.
- `src/stores/persons.js` — assigns undeclared `cuuDetailePersons`/`cuuDetailePersons`/`loaded` keys.

### Inconsistent service return shapes

`personsService` returns `.data` for list calls but the **full axios response** for `fetchPersonInfo` / `fetchLaganPersonInfo` / `fetchBasicPersonInfo` and mutations, so callers mix `res.data` vs `res`.

### Dead / mismatched component contracts

- `src/views/mainAdmin/afrPersons/Index.vue:51-56` passes `:open`/`:isEdit`/`:modelValue` to `AfrPersonModal`, which expects `isModalOpen`/`isEditMode`/`currentAfrPerson` → the add/edit modal never opens; `openEdit()` is never called.
- Same file: `@rowClick="goToProfile"` receives only the row (the `page` argument is `undefined`) and most columns are `copyable`, which suppresses row clicks → row navigation does nothing.
- `src/components/layouts/mainAdmin/Header.vue` receives `@toggle-sidebar` but defines no such emit; settings/profile buttons have no handlers.
- `src/components/fields/glopalSearch.vue:47-51` — the back-sync `watch` is commented out, so the parent `v-model` never updates.
- `src/components/fields/selectField.vue:24` — `modelValue: String` with numeric option values → prop-type warnings.
- `src/components/global/dataTable/BaseTable.vue:66` — `col.value` is invoked unconditionally → breaks if a column has no value function.
- `src/components/mainAdmin/AfrPersons/ImageUploadPanel.vue` — unguarded `selectedType.value.photo_type_name`.
- `src/views/mainAdmin/lagna/Index.vue:285-303` — `handlePersonsSelected`/`addSelectedPersons` reference an undefined `lagnaStore`.
- `src/views/mainAdmin/lagna/specificLagnaPersonProfile.vue:769,804,831` — unguarded `error.response.data.details`; `:799` uses `error.status` instead of `error.response?.status`; `:1779` has a corrupted CSS selector (`سسسسسس .leader-label`).

### Missing dependency: `html2canvas`

Imported by `presenting/presenting.vue`, `afrPersons/Index.vue`, `useImageUtils.js` and others, but **not declared** in `package.json` — it only exists as an optional transitive dependency. A clean `npm install` can break the build. Add it explicitly:

```sh
npm install html2canvas
```

### Layout / navigation oddities

- `src/components/global/pageNavigation.vue:8` — crumbs with a `null` path (including the last one) link to `/`, which redirects to `/login`; mitigated only by `pointer-events: none` on the active crumb.
- `src/layouts/SemiAdminLayout.vue` is an orphan whose unscoped `<style>` targets global `header`/`aside`/`main`.
- `src/layouts/default.vue` imports `Sidebar` without using it.

### Styling problems

- `public/main.css:23` — `main { z-index: -1 }` can push content behind backgrounds.
- `public/main.css:19` — invalid `font-feature-settings: l;`.
- `public/main.css:8` — `unicode-bidi: bidi-override` combined with `user-select: none` (`:18`) can fight normal RTL text and selection.
- Invalid values `width: -61%; font-size: -26px;` in `presenting.vue:2439-2441` and `profileImageUpload.vue:325-327`.
- Dead `@media (max-width: 20px)` rules in `sectionBlock.vue:186`, `presenting.vue:2365`, `profileImageUpload.vue:264`.
- `index.html` has `<html lang="">` — set `lang="ar"` for correct Arabic rendering and hyphenation.
- `src/assets/libs/tailwindcss.js` — unused vendored Tailwind build.

### Orphaned files

Not referenced by the router (safe to archive once confirmed):

`views/HomeView.vue`, `views/AdminControl.vue`, `views/atteendReport.vue`, `views/mainAdmin/Index.vue`, `views/mainAdmin/Users.vue`, `views/mainAdmin/lagna/lagnaData.vue`, `views/mainAdmin/lagna/lagnaMembers.vue`, `views/mainAdmin/lagna/UnFitnessReportModal copy.vue`, `views/mainAdmin/lagna/UnFitnessReportModal copy 2.vue`, `views/presentation/presenting7.vue`, `views/presentation/presenting7 copy.vue`, `views/semiAdmin/Lagna.vue` (has a stray `div` before `<template>` → would not compile), `views/semiAdmin/{Users,Reports,Settings}.vue`, `views/semiAdmin/reports/units_images_report.vue`, `components/global/popup/Rejectpop.vue`, `components/global/popup/reasonsPopup copy.vue`, `components/mainAdmin/AfrPersons/profile/addOpinionModal.vue`, `components/mainAdmin/dataTableStatistic.vue`, `utils/buildSidebarMenu.js`.

`HomeView.vue` (4,326 lines) and `presenting7*.vue` also import popups from `@/components/popup/*`, a path that does not exist.

### Logging noise

472+ `console.log` calls across `src/`, including on every navigation (`router/index.js:23`), every sidebar mount (`Sidebar.vue:181`), and in `BaseTable`. Remove before release.

### Stale test

`src/__tests__/App.spec.js:9` asserts `"You did it!"`, which `App.vue` no longer renders — `npm run test:unit` fails out of the box.

## Infrastructure

### No application service

Both nginx configs proxy to `nco_backend:8080`, but **no Dockerfile or Compose service defines it**. You must supply the application container/host.

### Dockerfile typo

`front/manzoma/Dockerfile:2` copies to `/user/share/nginx/html` while the vhost map expects `/usr/share/nginx/html/…` → 404 for the SPA unless corrected.

### Windows paths in container config

`front/manzoma/docker/nginx.conf` aliases `/images/` to `T:/app_photo/media/`, which does not exist in a Linux container. Same in `web_server_nginx/nginx.conf` for the bare-metal server (intentional there, but only valid on that host).

### Missing certs

Both configs require `/etc/certs/cert.pem` + `key.pem`, which are not in the image or the repo — mount them or nginx fails on 443.

### Entrypoint issues

`front/manzoma/docker/entrypoint.sh` has no shebang and no signal trap, so `docker stop` relies on SIGKILL.

### nginx hardening gaps

No gzip, no cache headers, no CSP, HSTS commented out, no `ssl_protocols`/ciphers, no `proxy_read_timeout`, and `client_max_body_size 5M` (too small for photo uploads).

### Volume must be pre-created

`backend/docker-compose.yml` declares `nco_database` as `external: true` — `docker compose up` fails unless you run `docker volume create nco_database` first.

### Unpinned everything

`backend/requirement.txt` has no versions; `redis` and `nginx` image tags are unpinned; there is no lock file.

### No root `.gitignore`

Only `front/manzoma/.gitignore` exists. A `git init && git add .` would commit:

- `backend/nco/nco/db.sqlite3` (~1.1 GiB)
- `backend/nco_env/` (a full Python virtualenv)
- `front/manzoma/node_modules/`
- `backend/.db.env`, `front/manzoma/.env*`

Create a root `.gitignore` (see [development.md](development.md#version-control-hygiene)).

### No CI

No `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`, `Makefile` or `Procfile`.

## Quick fixes checklist

```text
[ ] Add DJANGO_SETTINGS_MODULE to docs/scripts (or fix settings/__init__.py)
[ ] Add a `default` DB to nco/settings/oracle.py
[ ] Rename apps/customadmin/management/__init___ → __init__
[ ] Uncomment the Celery import in nco/__init__.py; fix apps/schadule/celery.py
[ ] Externalise and rotate SECRET_KEY, DB passwords, S3 keys, NSFW token
[ ] Uncomment the default child route of /main-admin
[ ] Fix authStore.redirectByRole route names
[ ] Fix the role comparison in router/index.js (roles vs role)
[ ] Wrap query params as { params } in lagnaService/persons/glopal
[ ] Fix the space in lagna.js:36
[ ] Fix useSocket URL building + the out-of-scope wsStore disconnects
[ ] npm install html2canvas
[ ] Fix AfrPersonModal prop contract and row-click navigation
[ ] Repair the stale App.spec.js assertion
[ ] Add a root .gitignore
[ ] Fix the Dockerfile /user → /usr typo and the container /images/ alias
```

## Related

- [backend.md](backend.md) · [frontend.md](frontend.md) · [deployment.md](deployment.md)
