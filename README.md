# NCO Manzoma

**منظومة NCO** — an internal web application for managing personnel records and committee (لجان) workflows.

A Vue 3 single-page client talking to a Django REST Framework API, with JWT authentication, real-time presentation screens over WebSockets, photo intake with automated review, configurable UI layouts, and committee reporting.

---

## Features

| Area | What it does |
| --- | --- |
| **Personnel records** | Dossiers covering units, education, punishment, medical, family, travel, leave, efficiency, security and psychological reports |
| **Committees (لجان)** | Create main and sub committees, schedule specific sessions, assign members and persons, record reasons, opinions, votes and final decisions |
| **Real-time presentation** | A projection screen and a control panel driven live over WebSockets — persons, votes, reports and notifications update in the room as they happen |
| **Photo intake** | Multi-type photo upload, automated NSFW screening via a classifier service, accept/reject review workflow, coverage reports per unit and per person |
| **Reports** | Photo coverage (parent army → unit → person) and committee statistics, push-fed to connected clients |
| **Configurable UI** | Admin-managed sections and fields per page (`ui-settings`), so layouts change without a code release |
| **Accounts & roles** | JWT login with roles derived from Django groups, plus model-level permissions for review, rejection and reporting |

---

## Architecture at a glance

```
        Browser (RTL / Arabic)
                │  HTTPS
                ▼
       ┌─────────────────┐
       │   nginx  :443   │  SPA fallback, /api/ /admin/ /wss/ proxy
       └─────────────────┘   /static/ and /images/ file aliases
              │         │
       dist/  │         │  nco_backend:8080
              ▼         ▼
     ┌────────────┐  ┌──────────────────────┐
     │ Vue 3 SPA  │  │ Django (ASGI/Daphne) │
     │   Pinia    │──│ DRF + JWT + Channels │
     └────────────┘  └──────────┬───────────┘
                                │
        ┌───────────┬───────────┼───────────┬────────────┐
        ▼           ▼           ▼           ▼            ▼
   PostgreSQL    Redis      RabbitMQ    Celery       NSFW svc
   / SQLite      cache      broker      workers       :6086
   / Oracle
```

**Two WebSocket channels:**

- `/lagna/ws/lagna/` — committee screen (groups `comm_<code>`, `comm_<code>_head|voter`)
- `/report/wss/photo/report/` — live photo-coverage report (groups `photo_report`, `photo_report_<prnt>`)

Full detail: [docs/architecture.md](docs/architecture.md).

---

## Tech stack

**Frontend** — Vue 3 · Vue Router 4 · Pinia · Axios · Vite 7 · Tailwind CSS 4 · Bootstrap 5 · Chart.js · ExcelJS · jsPDF

**Backend** — Django 5 · Django REST Framework · SimpleJWT · drf-yasg (Swagger) · django-jazzmin · Django Channels · Celery · django-storages/S3 · Pillow · pandas

**Infrastructure** — PostgreSQL 16 · Redis · RabbitMQ · pgAdmin · NSFW classifier · nginx · Docker Compose · Oracle (schema scripts)

---

## Repository layout

| Path | Purpose |
| --- | --- |
| `front/manzoma/` | Vue 3 + Vite web client |
| `backend/nco/` | Django project, REST API and domain apps |
| `backend/nco/apps/` | `person`, `lagna`, `photos`, `report`, `users`, `tanzem`, `uisettings`, `api/v1`, `customadmin` |
| `backend/nco/oracle_*.sql` | Oracle schema, lookup data, UI-settings DDL |
| `backend/docker-compose.yml` | PostgreSQL, Redis, RabbitMQ, pgAdmin, NSFW service |
| `backend/requirement.txt` | Python dependencies (unpinned) |
| `web_server_nginx/` | Edge nginx configuration and sample hosts file |
| `docs/` | Full project documentation |

---

## Quick start

### Prerequisites

- **Node.js** `^20.19.0` or `>=22.12.0`
- **Python** 3.11+ (3.12 matches the checked-in environment)
- **Docker + Compose** — optional, for PostgreSQL/Redis/RabbitMQ/NSFW

### 1. Backend (SQLite — no external services)

```sh
cd backend/nco
pip install -r ../requirement.txt

python manage.py migrate         --settings=nco.settings.sqlite_set
python manage.py createsuperuser --settings=nco.settings.sqlite_set
python manage.py seed_ui_settings --settings=nco.settings.sqlite_set
python manage.py runserver 8000  --settings=nco.settings.sqlite_set
```

> ⚠️ Always pass `--settings=`. `manage.py` defaults to `nco.settings`, an empty package with no database configuration.

### 2. Frontend

```sh
cd front/manzoma
npm install
npm run dev
```

Vite serves **http://localhost:5173**.

Point the client at your backend with `front/manzoma/.env.local`:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MEDIA_BASE_URL=http://localhost:8000
VITE_SOCKET_BASE_URL=localhost:8000/
VITE_WS_PROTOCOL=ws
```

### 3. Supporting services (optional)

```sh
cd backend
docker volume create nco_database
docker compose up -d
```

| Service | Port |
| --- | --- |
| PostgreSQL | `5432` |
| RabbitMQ management | `15672` |
| pgAdmin | `8080` |
| NSFW classifier | `6086` |

### What you get

| URL | Purpose |
| --- | --- |
| http://localhost:5173 | Application |
| http://localhost:8000/api/v1/ | API index |
| http://localhost:8000/api/v1/swagger/ | Swagger UI |
| http://localhost:8000/api/v1/swagger/redoc/ | ReDoc |
| http://localhost:8000/admin/ | Django admin |

---

## Commands

**Frontend** (`front/manzoma/`)

```sh
npm run dev        # dev server with HMR
npm run build      # production build → dist/
npm run preview    # serve the built dist/
npm run test:unit  # Vitest (watch mode; use `npx vitest run` for CI)
npm run format     # Prettier (no semicolons, single quotes, width 100)
```

**Backend** (`backend/nco/`)

```sh
python manage.py check              --settings=nco.settings.sqlite_set
python manage.py migrate            --settings=nco.settings.sqlite_set
python manage.py makemigrations <app> --settings=nco.settings.sqlite_set
python manage.py test               --settings=nco.settings.sqlite_set
python manage.py shell              --settings=nco.settings.sqlite_set
python manage.py seed_ui_settings   --settings=nco.settings.sqlite_set
celery -A nco.celery worker -l info          # background photo processing
daphne -b 0.0.0.0 -p 8080 nco.asgi:application   # ASGI (WebSockets)
```

---

## Configuration

### Settings modules

| Module | Default database | Use for |
| --- | --- | --- |
| `nco.settings.sqlite_set` | SQLite | Zero-dependency local development |
| `nco.settings.dev` | PostgreSQL `localhost:5432` | Local work against Compose |
| `nco.settings.production` | SQLite (+ `postgres`, `oracle` aliases) | Production profile — HSTS, secure cookies, CORS |
| `nco.settings.oracle` | ⚠️ no `default` key | Oracle (needs a fix first) |

`MANAGED_MIGRATIONS` toggles `Meta.managed` on models that map to pre-existing Oracle tables — `False` when the database is owned by an external source, `True` when Django should create tables.

### Frontend variables

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | API base, e.g. `http://localhost:8000/api/v1` |
| `VITE_MEDIA_BASE_URL` | Media/photo host (no trailing slash) |
| `VITE_SOCKET_BASE_URL` | WebSocket host, e.g. `localhost:8000/` |
| `VITE_WS_PROTOCOL` | `ws` or `wss` |

Vite precedence: `.env` → `.env.development` / `.env.production` → `.env.local`.

---

## Documentation

| Guide | Contents |
| --- | --- |
| 📐 [Architecture](docs/architecture.md) | System overview, data flow, realtime topology, data model |
| 🐍 [Backend](docs/backend.md) | Settings, apps, models, auth, views, Celery, photo pipeline |
| 📦 [Frontend](docs/frontend.md) | Env vars, API layer, routing, stores, layouts, components |
| 🔌 [API](docs/api.md) | Endpoints, authentication, permissions, WebSocket protocol |
| 🛠 [Development](docs/development.md) | Local setup, conventions, testing, repo hygiene |
| 🚀 [Deployment](docs/deployment.md) | Docker, nginx, TLS, Oracle scripts, go-live checklist |
| ⚠️ [Troubleshooting](docs/troubleshooting.md) | Known issues with file references |

**[Documentation index →](docs/README.md)**

---

## Deployment

The repository ships supporting services and web-server configuration, but **not** a complete full-stack deployment:

- `backend/docker-compose.yml` starts PostgreSQL, Redis, RabbitMQ, pgAdmin and the NSFW service — it does **not** run Django.
- `front/manzoma/Dockerfile` packages a **prebuilt** `dist/` into an nginx image; run `npm run build` first.
- `web_server_nginx/nginx.conf` is an edge config written for a Windows host (`T:/…` paths).
- The nginx upstream `nco_backend:8080` is referenced everywhere but **defined nowhere** — you must supply the application service.
- TLS certificates are read from `/etc/certs/` and are not included.

See [docs/deployment.md](docs/deployment.md) for the full topology, ports, Oracle scripts and a go-live checklist.

---

## Project status / caveats

This is a working codebase with known rough edges. Before deploying or contributing, read **[docs/troubleshooting.md](docs/troubleshooting.md)** — highlights:

- **Secrets are committed in source** (`SECRET_KEY`, database passwords, S3 keys). Rotate and externalise them.
- **`DEBUG = True`** in the shared base settings.
- **No root `.gitignore`** — a naive `git add .` would commit a ~1.1 GiB SQLite file, a Python virtualenv, `node_modules/`, and `.env` files.
- **`html2canvas` is imported but not declared** in `package.json`.
- **Backend dependencies are unpinned** — record a lock file.
- **No CI** configuration exists.
- Several frontend bugs affect login redirects, WebSocket connections, and query parameters.

---

## Contributing

1. Read [docs/architecture.md](docs/architecture.md), then the guide for your area.
2. Create a root `.gitignore` if one is still missing, and never commit credentials.
3. Frontend: keep URLs in `src/api/modules/`, param shaping in `src/services/`, shared state in `src/stores/`. Run `npm run format`.
4. Backend: always pass `--settings=`; put cross-model logic in `services/`; add model permissions in `Meta`.
5. Verify with:

   ```sh
   npx vitest run                                   # frontend
   python manage.py check --settings=… && python manage.py test --settings=…   # backend
   ```

---

## License

No license file is present in this repository. All rights reserved by the owning organisation unless a licence is added.
