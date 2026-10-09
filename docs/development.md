# Development guide

How to run, change and verify the project locally.

## Prerequisites

| Tool | Version |
| --- | --- |
| Node.js | `^20.19.0` or `>=22.12.0` (see `front/manzoma/package.json`) |
| npm | bundled with Node |
| Python | 3.12 is what the checked-in `nco_env` uses; 3.11+ should work |
| Docker + Compose | optional, for PostgreSQL/Redis/RabbitMQ/NSFW services |
| Oracle client | only if you target Oracle |

### Backend dependencies

`backend/requirement.txt` exists but every line is **unpinned**:

```sh
cd backend
python -m venv nco_env
source nco_env/bin/activate       # Windows: nco_env\Scripts\activate
pip install -r requirement.txt
```

Because nothing is pinned, record what you actually installed before sharing an environment:

```sh
pip freeze > requirement.lock.txt
```

If your team has a known-good lock file, prefer that — the checked-in list is a starting point.

## Repository layout

```
nco_manzoma/
├── README.md
├── docs/                      # this documentation
├── front/manzoma/             # Vue 3 SPA
├── backend/
│   ├── requirement.txt
│   ├── docker-compose.yml     # db, cache, nsfw, broker, pgadmin
│   ├── .db.env                # Postgres credentials (local)
│   └── nco/                   # Django project
├── web_server_nginx/          # edge nginx config + sample hosts file
└── .claude/                   # editor/agent permissions (not app config)
```

## Running the frontend

```sh
cd front/manzoma
npm install
npm run dev
```

Vite serves `http://localhost:5173` with HMR.

Point the client at your backend — create `front/manzoma/.env.local`:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MEDIA_BASE_URL=http://localhost:8000
VITE_SOCKET_BASE_URL=localhost:8000/
VITE_WS_PROTOCOL=ws
```

The checked-in `.env` targets a LAN host; `.env.development` targets `localhost:8080`. Vite precedence is `.env` → `.env.development` (dev) / `.env.production` (build) → `.env.local`.

Other commands:

```sh
npm run build        # production build → dist/
npm run preview      # serve dist/ locally
npm run test:unit    # Vitest watch mode
npx vitest run       # single pass (CI)
npm run format       # prettier --write src/
```

> Build the SPA before building the frontend Docker image — the Dockerfile only copies `dist/`.

## Running the backend

Always pass a settings module. `manage.py` defaults to `nco.settings`, which is an empty package and has no database.

### Option A — SQLite (no external services)

```sh
cd backend/nco
python manage.py check        --settings=nco.settings.sqlite_set
python manage.py migrate      --settings=nco.settings.sqlite_set
python manage.py createsuperuser --settings=nco.settings.sqlite_set
python manage.py seed_ui_settings --settings=nco.settings.sqlite_set
python manage.py runserver 8000 --settings=nco.settings.sqlite_set
```

### Option B — PostgreSQL via Docker

```sh
cd backend
# create the credentials file first (see below)
docker volume create nco_database       # the compose file declares it as external
docker compose up -d db
```

Create `backend/.db.env` (not committed) with:

```dotenv
POSTGRES_DB=nco
POSTGRES_USER=nco
POSTGRES_PASSWORD=<your-password>
```

Then run Django with `nco.settings.dev` (its default database is PostgreSQL on `localhost:5432`):

```sh
cd backend/nco
python manage.py migrate --settings=nco.settings.dev
python manage.py runserver 8000 --settings=nco.settings.dev
```

`nco.settings.dev` hardcodes its own database credentials — edit them to match `.db.env`.

### Which settings module?

| Module | Default DB | Use when |
| --- | --- | --- |
| `nco.settings.sqlite_set` | SQLite | Zero-dependency local work |
| `nco.settings.dev` | PostgreSQL `localhost:5432` | Local work against Compose Postgres |
| `nco.settings.production` | SQLite (+ `postgres`, `oracle` aliases) | Production profile: HSTS, secure cookies, CORS |
| `nco.settings.oracle` | ⚠️ no `default` key | Oracle — fix the module before use |

You can export it instead of repeating the flag:

```sh
export DJANGO_SETTINGS_MODULE=nco.settings.sqlite_set
python manage.py migrate
python manage.py runserver 8000
```

### Useful backend commands

```sh
python manage.py check --settings=…            # sanity check
python manage.py makemigrations <app> --settings=…
python manage.py migrate --settings=…
python manage.py test --settings=…             # run app tests
python manage.py shell --settings=…
python manage.py dumpdata <app> --indent 2 --settings=… > data.json
python manage.py seed_ui_settings --settings=…
python manage.py change_user_army_code --settings=…
python manage.py upload_opinions <file.xlsx> --settings=…
python manage.py dumps --help                  # bulk data migration out of Oracle
```

## Database choices

| Backend | Settings | Notes |
| --- | --- | --- |
| SQLite | `sqlite_set`, `dev.sqlite`, `production.default` | `backend/nco/nco/db.sqlite3` (⚠️ ~1.1 GiB — do not commit) |
| PostgreSQL 16 | `dev` | Started by `backend/docker-compose.yml` |
| Oracle | `oracle` / aliases in `sqlite_set`, `production` | Schema scripts in `backend/nco/oracle_*.sql` |

Migrations live in `apps/*/migrations/`. `MANAGED_MIGRATIONS` toggles `Meta.managed` on models that map to pre-existing Oracle tables/views — **turn it off** when your database is already populated by an external system, **on** when Django should create the tables.

Order for a fresh Oracle database:

```sh
sqlplus user/pass@//host:1521/service @oracle_schema.sql
sqlplus user/pass@//host:1521/service @oracle_lookup_data.sql
sqlplus user/pass@//host:1521/service @oracle_ui_settings.sql
# only if upgrading an existing DB that predates the column:
sqlplus user/pass@//host:1521/service @oracle_alter_add_reason.sql
```

Details in [deployment.md](deployment.md#oracle-scripts).

## Running the realtime + background pieces

WebSocket endpoints require an ASGI server:

```sh
python manage.py runserver 8000 --settings=nco.settings.sqlite_set   # dev ASGI
# or
daphne -b 0.0.0.0 -p 8080 nco.asgi:application
```

Celery workers (needed for photo processing):

```sh
celery -A nco.celery worker -l info
```

⚠️ `nco/__init__.py` has the Celery import commented out, so `-A nco.celery` is the safe form. Broker is RabbitMQ at `amqp://guest:guest@localhost:5672//` (`docker compose up -d broker`).

Optional monitoring:

```sh
celery -A nco.celery flower          # UI on :5555
```

## Full local stack

```sh
# 1. supporting services
cd backend && docker volume create nco_database && docker compose up -d

# 2. backend
cd nco
python manage.py migrate --settings=nco.settings.dev
python manage.py createsuperuser --settings=nco.settings.dev
python manage.py seed_ui_settings --settings=nco.settings.dev
python manage.py runserver 8000 --settings=nco.settings.dev

# 3. celery worker (separate terminal)
cd backend/nco && celery -A nco.celery worker -l info

# 4. frontend (separate terminal)
cd front/manzoma && npm run dev
```

| Service | URL |
| --- | --- |
| Frontend | http://localhost:5173 |
| API / Swagger | http://localhost:8000/api/v1/ · /api/v1/swagger/ |
| Admin | http://localhost:8000/admin/ |
| RabbitMQ UI | http://localhost:15672 (guest/guest) |
| pgAdmin | http://localhost:8080 |
| NSFW service | http://localhost:6086 |

## Working conventions

### Backend

- Put URL wiring in `apps/api/v1/urls.py`; keep app-level `urls.py` for app-specific routes.
- Business logic that spans models goes in `services/` (e.g. `apps/lagna/services/`), not in views.
- Prefer the app's `ActiveManager`/`all_objects` pair for soft-deleted rows.
- Add model `permissions = [...]` in `Meta` rather than inventing ad-hoc checks.
- New tables → `makemigrations` + `migrate`; Oracle-managed tables → keep `managed = getattr(settings, 'MANAGED_MIGRATIONS', False)` and update `oracle_schema.sql`.

### Frontend

- URLs belong in `src/api/modules/`, never in views.
- Wrap query params as `{ params }` inside `src/services/`, not in components.
- Shared state → Pinia store; page-local state → `ref`/`reactive`.
- Reusable markup → `src/components/` (`BaseTable`, `BaseModalForm`, `TablePagination`, `ModalOverlay`).
- Use the `@/` alias; run `npm run format` before committing.

### Style

- Frontend: no semicolons, single quotes, 100 columns (`.prettierrc.json`).
- Backend: follow the surrounding Django/DRF style; there is no linter config checked in.

## Testing and verification

```sh
# Frontend
cd front/manzoma
npx vitest run
npm run build

# Backend
cd backend/nco
python manage.py check --settings=nco.settings.sqlite_set
python manage.py test  --settings=nco.settings.sqlite_set
```

There is **no CI configuration** in this repository (no `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, `Makefile` or root `Makefile` equivalent). If you add CI, the two blocks above are the natural entry points.

## Version control hygiene

⚠️ There is **no root `.gitignore`** (only `front/manzoma/.gitignore`). Before the first `git add .`, create one at the repository root that covers at least:

```gitignore
# Python
__pycache__/
*.py[cod]
*.sqlite3
nco_env/
venv/

# Node
node_modules/
front/manzoma/dist/

# Secrets & env
.env
.env.local
backend/.db.env
*.pem
*.key

# Logs / OS
*.log
.DS_Store
```

Currently at risk of being committed: `backend/nco/nco/db.sqlite3` (~1.1 GiB), `backend/nco_env/` (a full virtualenv), `backend/.db.env`, `front/manzoma/.env*`, and `node_modules/`.

**Never commit** database passwords, `SECRET_KEY`, S3 keys, TLS certificates, or production `.env` files. Several of those are already present in the source — see [troubleshooting.md](troubleshooting.md#hardcoded-secrets-in-source).

## Related

- [architecture.md](architecture.md) — how the parts fit together
- [backend.md](backend.md) / [frontend.md](frontend.md) — per-stack reference
- [deployment.md](deployment.md) — production topology
- [troubleshooting.md](troubleshooting.md) — known issues
