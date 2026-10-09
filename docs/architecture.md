# Architecture

This document describes the system as a whole: the components, how they talk to each other, and where each concern lives.

## Overview

**NCO Manzoma** (منظومة) is an internal web application for managing personnel records and committee (لجان) workflows. It covers:

- Personnel dossiers (units, education, punishment, medical, family, travel, efficiency, security, psychological reports).
- Committee ("lagna") lifecycle: creation, specific sessions, members, assigned persons, voting, opinions, reasons, final decisions.
- A real-time presentation screen used during committee sessions, driven by WebSockets.
- Photo intake with automated review flags (NSFW detection) and photo coverage reports.
- Configurable UI sections/fields so pages can be rearranged without a code release.
- Reports for photo coverage and committee statistics.

The system is a **Django REST Framework monolith** serving a **Vue 3 single-page application**, with **Django Channels** for WebSockets, **Celery** for background work, and **nginx** in front.

## System diagram

```
                       Browser (RTL, Arabic UI)
                               |
                               | HTTPS
                               v
                    +--------------------+
                    |  nginx (edge)      |   web_server_nginx/nginx.conf
                    |  :80 / :443        |   front/manzoma/docker/nginx.conf
                    +--------------------+
                      |       |      |
        try_files SPA |       |      | static / images aliases
                      v       |      v
        +---------------+     |   /static/  -> collected Django static
        | Vue dist/     |     |   /images/  -> media (photo) storage
        +---------------+     |
                              |  /api/  /admin/  /wss/
                              v
                    +--------------------+
                    | nco_backend :8080  |   Django (Daphne/ASGI)
                    |  - HTTP (DRF)      |
                    |  - WebSocket       |
                    +--------------------+
                        |    |    |    |
        +---------------+    |    |    +----------------+
        |                    |    |                       |
        v                    v    v                       v
  +-----------+        +---------+  +-------------+  +------------+
  | PostgreSQL|        | Redis   |  | RabbitMQ    |  | S3 / local |
  | or SQLite |        | cache + |  | (Celery)    |  | media      |
  | or Oracle |        | channel |  +------+------+  +------------+
  +-----------+        +---------+         |
                                           v
                                    +-------------+
                                    | Celery      |
                                    | workers     |
                                    +------+------+
                                           |
                                    +------+------+
                                    | NSFW svc    |  :6086
                                    +-------------+

  Browser  <--- WebSocket --->  /ws/lagna/ and /report/wss/photo/report/
```

## Components

| Component | Location | Role |
| --- | --- | --- |
| Vue 3 SPA | `front/manzoma/` | All user-facing screens, RTL, Pinia state |
| Django project | `backend/nco/nco/` | Settings, URLconf, ASGI/WSGI, Celery app |
| Domain apps | `backend/nco/apps/` | person, lagna, photos, report, users, tanzem, uisettings, api/v1, customadmin, schadule |
| Edge nginx | `web_server_nginx/` | TLS termination, SPA fallback, reverse proxy |
| Frontend image | `front/manzoma/Dockerfile` + `docker/` | nginx serving the built `dist/` plus bundled static |
| Supporting services | `backend/docker-compose.yml` | PostgreSQL, Redis, RabbitMQ, pgAdmin, NSFW checker |
| Oracle DDL | `backend/nco/oracle_*.sql` | Schema/lookup scripts for an existing Oracle source |

## Request flow

1. **Page load** — nginx serves `index.html` (`try_files $uri $uri/ /index.html`), plus hashed assets from `dist/assets/`.
2. **API calls** — the SPA calls `${VITE_API_BASE_URL}/…`, e.g. `https://www.afrad.mil.eg/api/v1/persons/`. nginx proxies `/api/` to `http://nco_backend:8080`, Django routes `api/v1/` → `apps/api/v1/urls.py`.
3. **Authentication** — `POST /api/v1/login/` returns a SimpleJWT access token plus extended claims (`is_superuser`, `role`, `info`). The SPA stores the token in `localStorage` and sends `Authorization: Bearer <token>` via the Axios interceptor (`src/api/http.js`).
4. **Media** — image URLs are built from `VITE_MEDIA_BASE_URL`; nginx serves them from the `/images/` alias (the backend writes them to `MEDIA_URL = '/images/'`).
5. **Realtime** — the SPA opens WebSockets; Django Channels authenticates the `token` query parameter through `JWTAuthMiddleware` and adds the socket to a group. Producers (Celery tasks, view actions) send to the group; consumers push events to the browser.

## Realtime topology

Two consumers, mounted from `backend/nco/nco/asgi.py`:

| Mount | Route file | Path | Consumer | Group naming |
| --- | --- | --- | --- | --- |
| `report/` | `apps/report/routing.py` | `/report/wss/photo/report/` | `PrntPhotoReportConsumer` | `photo_report` (superuser or `report.can_see_all_army`) else `photo_report_<prnt_army_code>` |
| `lagna/` | `apps/lagna/routing.py` | `/lagna/ws/lagna/` | `LagnaShowConsumer` | `comm_<lagna_code>` and `comm_<lagna_code>_head` / `comm_<lagna_code>_voter` |

The lagna consumer reads `?lagna=<code>` and `?token=<jwt>`, verifies the user is a member of that committee, and pushes `settings`, `show_person`, `votes`, `comm_report` and `notify` events.

> Note: nginx proxies `/wss/` (not `/ws/`). The exact public socket path therefore depends on the proxy rewrite in front of the app — see [deployment.md](deployment.md#websocket-proxying).

## Background work

- **Celery app**: `backend/nco/nco/celery.py` (broker `amqp://…@localhost:5672`).
- **Tasks** live in `apps/photos/tasks.py`:
  - `calculate_person_photos(photo_id)` — recomputes per-person photo coverage flags and writes `AfrPhotoReport`, then broadcasts the photo report over WebSockets.
  - `check_photo_nsfw(photo_id)` — posts the image to the NSFW service (`http://localhost:6086/api/upload_check`), stores `is_nsfw`, retries on connection errors.
- Both are triggered by a `post_save` signal on `PhotoInfo` (`apps/photos/signals.py`).
- `apps/report/tasks.py` is empty; `apps/schadule/` is a placeholder whose Celery app is misconfigured (see [troubleshooting.md](troubleshooting.md)).
- There is **no `CELERY_BEAT_SCHEDULE`** in the repo — nothing runs on a timer out of the box.

## Data model at a glance

```
ArmyCode / Rank / Jobs / FamilyDegreeCode      (tanzem — reference)
        |
        v
   Profile  <---- 1:1 ---- django.contrib.auth.User
        |
        |  (army_code, prnt_army_code, rank, job)
        v
   AfrPerson  (AFR_PER_DATA)
     |-- Family, AfrEducation, AfrUnits, AfrVacation, AfrTravel
     |-- AfrPunishment, MedicalHistory, AfrPsychologicalReport
     |-- AfrSecuritySituation, efficiency/statistics (views)
     |
     |--< PhotoInfo -- RejectPhotoInfo -- RejectPhotoReason
     |
     +--< LagnaAfrSnapData  (a person's snapshot for a committee)
     |        |--< LagnaPersonReasons, AfrSnapOpinion,
     |        |    AfrSnapFinalDecition, LagnaCommSnapDetail
     |        +--> LagnaCommanderData
     |
     +--< LagnaPersons  (person placed in a committee session)
              |--< LagnaPersonVotes, LagnaPersonsOpinions, LagnaPersonPonsCons

   Lagna (committee) --< LagnaTypeSpacific (specific session)
              |      |--< LagnaMember
              |      +-- (parent/root self references for main vs sub)
   LagnaAfrStatus, LagnaType, LagnaCategory, VoteType, LagnaMemberType ...
```

Report models (`PrntPhotoReport`, `UnitPhotoReport`, `LagnaAfrReport`, …) map to database views and are read-only aggregates.

## Frontend layering

```
views/*.vue  (route screens)
   |
   +--> components/  (BaseTable, popups, field widgets, layout chrome)
   |
   +--> stores/      (Pinia: auth, lagna, persons, reports, uiSettings, loading)
   |
   +--> services/    (lagnaService, personsService, glopal, webSocketService)
   |
   +--> api/modules/ (thin axios calls per resource)
   |
   +--> api/http.js  (axios instance, auth header, retries, cancel)
```

Rules of thumb when working in the frontend:

- **URLs** belong in `src/api/modules/`, not in views.
- **Request shaping** (`{ params }` wrapping) belongs in `src/services/`.
- **Shared state** belongs in `src/stores/`.
- **Reusable markup** belongs in `src/components/`.

## Configuration surface

| Concern | Frontend | Backend | Edge |
| --- | --- | --- | --- |
| API base | `VITE_API_BASE_URL` | `ROOT_URLCONF`, `/api/v1/` | `location /api/` proxy |
| Media base | `VITE_MEDIA_BASE_URL` | `MEDIA_URL`, `MEDIA_ROOT` | `location /images/` alias |
| Sockets | `VITE_SOCKET_BASE_URL`, `VITE_WS_PROTOCOL` | `CHANNEL_LAYERS`, ASGI | `location /wss/` proxy |
| Database | — | `DATABASES` per settings module | — |
| Hosts | — | `ALLOWED_HOSTS` | `server_name`, `map $host $frontend_root` |

## Technology summary

**Backend** — Django 5.x, Django REST Framework, SimpleJWT, drf-yasg (Swagger), django-jazzmin (admin theme), django-cors-headers, Django Channels + Daphne/uvicorn, Celery + RabbitMQ, django-redis, django-storages + boto3 (S3), Pillow, pandas, psycopg.

**Frontend** — Vue 3 (Composition API), Vue Router 4, Pinia, Axios, Vite 7, Tailwind CSS 4, Bootstrap 5, Chart.js, ExcelJS, jsPDF (+ autotable), sweetalert.

**Infrastructure** — PostgreSQL 16, Redis, RabbitMQ, pgAdmin, an NSFW classification microservice, nginx, Docker Compose.

See [backend.md](backend.md), [frontend.md](frontend.md), [api.md](api.md) and [deployment.md](deployment.md) for the details of each part.
