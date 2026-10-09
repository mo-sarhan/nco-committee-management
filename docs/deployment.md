# Deployment

This describes the topology the repository ships with, and the gaps you must fill for a real deployment.

## What exists

| Artefact | Purpose |
| --- | --- |
| `backend/docker-compose.yml` | Supporting services only (PostgreSQL, Redis, RabbitMQ, pgAdmin, NSFW). **No application container.** |
| `backend/.db.env` | PostgreSQL credentials for Compose (local file) |
| `front/manzoma/Dockerfile` + `docker/` | nginx image serving a **prebuilt** `dist/` |
| `web_server_nginx/nginx.conf` | Edge nginx config (written for a Windows host) |
| `web_server_nginx/hosts` | Sample `hosts` entries for local name resolution |
| `backend/nco/oracle_*.sql` | Oracle DDL and seed data |

**Missing:** an application Dockerfile/Compose service for Django/Daphne (the upstream `nco_backend` is referenced by both nginx configs but never defined), CI config, a root `.gitignore`, and TLS certificates.

## Ports

| Port | Protocol | Service | Defined in |
| --- | --- | --- | --- |
| 5173 | HTTP | Vite dev server | Vite default |
| 8000 | HTTP/WS | Django dev server (`runserver`) | docs/commands |
| 8080 | TCP | **pgAdmin** UI (`8080:80`) | `backend/docker-compose.yml` |
| 8080 (internal) | TCP | **Application upstream** `nco_backend:8080` | both nginx configs |
| 5432 | TCP | PostgreSQL 16.2 | `backend/docker-compose.yml` |
| 6086 | TCP | NSFW classification service | `backend/docker-compose.yml` |
| 5672 / 15672 | TCP | RabbitMQ AMQP / management UI | `backend/docker-compose.yml` |
| 80 | TCP | nginx HTTP → `301` to HTTPS | `web_server_nginx/nginx.conf`, `front/manzoma/docker/nginx.conf` |
| 443 | TCP/TLS | nginx HTTPS | both nginx configs |
| 1521 | TCP | Oracle listener | connect strings in `oracle_schema.sql` |

⚠️ Host port **8080 is taken by pgAdmin**, not by the app. If you publish the Django app on the host at 8080, change the pgAdmin mapping first.

## Docker Compose

```sh
cd backend
docker volume create nco_database      # declared as `external: true`
docker compose up -d
```

| Service | Image | Container | Ports | Restart |
| --- | --- | --- | --- | --- |
| `db` | `postgres:16.2` | `nco_db` | 5432:5432 | — |
| `cache` | `redis` (unpinned) | `nco_cache` | none | — |
| `nsfw` | `helloz/nsfw` | `nsfw` | 6086:6086 | — |
| `broker` | `rabbitmq:4.2-management` | `nco_broker` | 5672, 15672 | `always` |
| `pgadmin` | `dpage/pgadmin4` | `fastapi_pgadmin_nco` | 8080:80 | `always` |

- Only `db` reads `env_file: .db.env`.
- Network: `nco_network` (default bridge). Volume: `nco_database` (external).
- pgAdmin ships **hard-coded default credentials** in the compose file — change them before exposing the host.
- The NSFW service has a placeholder `TOKEN=your_token_here`, which must match `apps/photos/services/check_nsfw_photo.py`.
- Compose does **not** build or run Django or the frontend.

```sh
docker compose up -d db        # just the database
docker compose ps
docker compose down            # stop (data persists in the volume)
```

## Application runtime

Run Django behind an ASGI server (WebSockets require it):

```sh
# development
python manage.py runserver 0.0.0.0:8080 --settings=nco.settings.production

# production-style
daphne -b 0.0.0.0 -p 8080 nco.asgi:application
```

Plus a Celery worker for photo processing:

```sh
celery -A nco.celery worker -l info
```

The application must be resolvable as **`nco_backend`** from nginx — either run it on the Docker network, or add it to the host file (see below).

## Frontend image

```sh
cd front/manzoma
npm install
npm run build          # produces dist/
docker build -t manzoma-web .
docker run -p 80:80 -p 443:443 manzoma-web
```

`Dockerfile` (single stage, **does not build the SPA**):

| Line | Instruction | Issue |
| --- | --- | --- |
| 1 | `from nginx` | unpinned base image |
| 2 | `copy ./dist /user/share/nginx/html` | ⚠️ typo: `/user` vs `/usr` — mismatches the vhost root map |
| 3 | `copy docker/static /static/` | Django/admin/DRF/jazzmin static + bundled media |
| 4 | `copy docker/nginx.conf /etc/nginx/conf.d/default.conf` | vhost |
| 9–10 | `copy docker/entrypoint.sh …` + `chmod +x` | entrypoint has **no shebang** |
| 12 | `cmd ["/entrypoint.sh"]` | starts nginx, `wait`s on it (no signal trap) |

`docker/entrypoint.sh`:

```sh
nginx -g "daemon off;" &
NGINX_PID=$!
wait $NGINX_PID
```

- No `#!/bin/sh` → can fail with `ENOEXEC` on strict runtimes.
- No `trap` → `docker stop` falls back to SIGKILL after the grace period.

**Certs are not baked into the image.** Both nginx configs read `/etc/certs/cert.pem` and `/etc/certs/key.pem`, so you must bind-mount or secret-mount them or nginx will not start on 443.

There is no `.dockerignore`, so the build context includes `node_modules/` — add one.

## nginx

Two nearly identical configurations with different path styles:

| File | Target |
| --- | --- |
| `web_server_nginx/nginx.conf` | Bare-metal edge server with **Windows paths** (`T:/…`) |
| `front/manzoma/docker/nginx.conf` | Container vhost (`/usr/share/nginx/html/…`) |

### Structure (both files)

- `upstream nco { server nco_backend:8080; }`
- `map $host $frontend_root` — picks the SPA root per hostname:

| Host | `web_server_nginx/nginx.conf` | `front/manzoma/docker/nginx.conf` |
| --- | --- | --- |
| `afrad.oma.mil.eg` | `T:/app_backup/…/production_dist/out/dist/` | `/usr/share/nginx/html/out/dist/` |
| `afrad.mil.eg` | `T:/app_backup/…/production_dist/dist/` | `/usr/share/nginx/html/` |
| `www.afrad.mil.eg` | `/dist/` | `/usr/share/nginx/html/dist/` |
| default | `T:/app_backup/…/production_dist/dist/` | `/usr/share/nginx/html/` |

- **HTTP `:80`** → `return 301 https://$host$request_uri;`
- **HTTPS `:443`** → `ssl_certificate /etc/certs/cert.pem` (+key), `client_max_body_size 5M`, `X-Content-Type-Options: nosniff`, HSTS commented out, `root $frontend_root`.

### Locations

| Location | Behaviour |
| --- | --- |
| `/admin/` | `proxy_pass http://nco;` with `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` |
| `/` | `try_files $uri $uri/ /index.html;` — SPA fallback |
| `/api/` | `proxy_pass http://nco;` + `proxy_http_version 1.1` + `Upgrade $http_upgrade` (⚠️ `Connection` header not set) |
| `/wss/` | WebSocket proxy: `Upgrade $http_upgrade` + `Connection "upgrade"` (⚠️ `proxy_http_version 1.1` not set) |
| `/static/` | `alias /static/;` — served from the `docker/static` tree |
| `~ ^/images/\s+(.*)$` | `return 301 /images/$1;` — whitespace normaliser |
| `/images/` | `alias T:/app_photo/media/;` ⚠️ **Windows path inside the container image** |

### Hostnames

```
localhost  10.2.92.92  www.afrad.mil.eg  afrad.mil.eg  *.afrad.mil.eg
afrad.*  *.afrad.*  afrad.oma.eg  afrad.oma.mil  *.afrad.oma.mil  afrad.oma.mil.eg
```

Django `ALLOWED_HOSTS` must include every hostname you serve (set in `nco/settings/production.py`).

### WebSocket proxying

The public paths are **`/wss/`** (edge) and the backend mounts at `/lagna/ws/lagna/` and `/report/wss/photo/report/`. Both nginx configs forward `/wss/` with a plain `proxy_pass http://nco;` (no rewrite), so the forwarded path keeps the `/wss/` prefix. Confirm your ASGI mount matches the public path, or add a rewrite:

```nginx
location /wss/ {
    proxy_pass http://nco/wss/;     # strip /wss/ …
    # or: proxy_pass http://nco/;   # …depending on your mount points
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 86400s;
    proxy_send_timeout 86400s;
}
```

The frontend's socket URL comes from `VITE_SOCKET_BASE_URL` + `VITE_WS_PROTOCOL` — make them agree with this block.

### Recommended nginx fixes

| Issue | Fix |
| --- | --- |
| `client_max_body_size 5M` rejects larger photo uploads | Raise it (e.g. `20m`) on `/api/` at minimum |
| `/api/` sets `Upgrade` but not `Connection` | Set `proxy_set_header Connection "upgrade";` (only when upgrading) or drop the `Upgrade` header |
| `/wss/` missing `proxy_http_version 1.1` | Add it |
| No timeouts | Set `proxy_read_timeout` for long-lived WebSockets |
| No gzip | Enable `gzip` for text/js/css/json |
| HSTS commented out | Uncomment once HTTPS is verified |
| `T:/…` aliases in the container config | Replace with the Linux media path |
| No cache headers for `/assets/` | Add immutable caching for hashed assets |

## Name resolution

`web_server_nginx/hosts` maps the application hostname:

| IP | Names |
| --- | --- |
| `127.0.1.1`, `172.17.0.1` | `nco_backend` |
| `127.0.0.1` | `localhost` |
| `192.168.1.13` | `mosarhan.com`, `www.oma.mil`, `afrad.oma.mil`, `gitlab.local` … |
| `172.16.110.x` | `server-1…5`, `ubuntu-*` |

If nginx runs on the Docker network, `nco_backend` resolves automatically; otherwise add the entry to the host's `/etc/hosts`. `172.17.0.1` is the default Docker bridge gateway.

## TLS

- Active certs: `/etc/certs/cert.pem` + `/etc/certs/key.pem` (outside the repo).
- Commented alternates in both configs reference `../new_cert/` and `../certification/`.
- No `ssl_protocols`, `ssl_ciphers`, or session settings are configured — add a modern baseline.
- HSTS is present but commented out.

## Oracle scripts

Run with SQLcl/SQL\*Plus/SQL Developer in **UTF-8** (`NLS_LANG=.AL32UTF8`).

| Script | Contents | When |
| --- | --- | --- |
| `oracle_schema.sql` | 1,816 lines · **67 tables** · 122 indexes · 145 `ALTER TABLE` · no data | First. Sections: optional DBA user, HAYAA reference tables, Django framework tables, AFRAD source views (as tables), application tables, constraints, FKs, indexes, function-based unique indexes, optional drops. |
| `oracle_lookup_data.sql` | 134 `INSERT`s across 17 lookup tables + identity realignment | After the schema. Fills only reference data (ranks, degrees, committee types, opinion types, photo statuses…). Does **not** copy bulk personnel data — that comes from the source feed. |
| `oracle_ui_settings.sql` | 2 tables (`UI_PAGE_SECTION`, `UI_SECTION_FIELD`) + 4 indexes | After the schema, if you use the UI settings feature. |
| `oracle_alter_add_reason.sql` | 1 `ALTER TABLE` adding `AFR_SNAP_DATA."ADD_REASON"` | Upgrades only; fresh installs already have the column. |

Tables in the schema use **quoted case-sensitive identifiers** — always reference them as `"AFR_PER_DATA"`, not `afr_per_data`.

Apply only to the intended database after review; take a backup first.

```sh
sqlplus hayaa_web/<password>@//host:1521/service @oracle_schema.sql
sqlplus hayaa_web/<password>@//host:1521/service @oracle_lookup_data.sql
sqlplus hayaa_web/<password>@//host:1521/service @oracle_ui_settings.sql
```

## Deployment checklist

**Before go-live**

- [ ] Move `SECRET_KEY`, database passwords, S3 keys and the NSFW token to environment variables; rotate the committed values.
- [ ] Set `DEBUG = False` (it is `True` in `base.py`, which every module inherits from).
- [ ] Verify `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` for your domain.
- [ ] Provide an application container/service resolvable as `nco_backend:8080`.
- [ ] Run with an ASGI server; confirm `/wss/` reaches the Channels consumers.
- [ ] Mount `/etc/certs/{cert,key}.pem`; enable `ssl_protocols`/ciphers and HSTS.
- [ ] Raise `client_max_body_size` for photo uploads.
- [ ] Replace the `T:/…` media alias with the real Linux media path, or point `MEDIA_ROOT` at S3 properly (the placeholder S3 credentials in `base.py` are test values).
- [ ] Start Celery workers; confirm `broker` and `cache` are reachable.
- [ ] Match the NSFW service token with `apps/photos/services/check_nsfw_photo.py`.
- [ ] Decide `MANAGED_MIGRATIONS` for your database, then run `migrate` accordingly.
- [ ] Seed UI settings: `python manage.py seed_ui_settings`.
- [ ] Create an admin: `python manage.py createsuperuser`.
- [ ] Add a root `.gitignore`; confirm no secrets/DB/venv are tracked.
- [ ] Pin backend dependencies (`pip freeze`) and record the frontend lock file.

**Operational**

- [ ] Back up the database and the media store.
- [ ] Configure logging (the `LOGGING` block in `base.py` is commented out).
- [ ] Set up monitoring for Daphne, Celery and Redis (Flower is available).
- [ ] Rotate JWT signing material on a schedule (`SECRET_KEY` currently signs tokens).

## Related

- [architecture.md](architecture.md) — system overview
- [development.md](development.md) — local workflows
- [troubleshooting.md](troubleshooting.md) — known issues
