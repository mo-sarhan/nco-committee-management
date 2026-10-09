# Documentation

Start here.

| Guide | What it covers |
| --- | --- |
| [Architecture](architecture.md) | System overview, components, data flow, realtime topology, data model |
| [Backend](backend.md) | Django settings, apps, models, auth, views, Celery, management commands, photo pipeline |
| [Frontend](frontend.md) | Vue stack, env vars, API layer, routing, stores, layouts, components, WebSockets |
| [API](api.md) | Endpoint catalogue, authentication, permissions, WebSocket protocol, cURL examples |
| [Development](development.md) | Local setup, run commands, conventions, testing, version-control hygiene |
| [Deployment](deployment.md) | Docker Compose, nginx, ports, TLS, Oracle scripts, go-live checklist |
| [Troubleshooting](troubleshooting.md) | Known issues and bugs, grouped by area, with file references |

## Suggested reading order

**New to the project** → [architecture.md](architecture.md) → [development.md](development.md) → run the stack.

**Working on a feature** → [architecture.md](architecture.md) → the stack guide for your area ([backend.md](backend.md) / [frontend.md](frontend.md)) → [api.md](api.md).

**Shipping to production** → [deployment.md](deployment.md) → [troubleshooting.md](troubleshooting.md).

**Something is broken** → [troubleshooting.md](troubleshooting.md) first, then the relevant stack guide.

## Repository map

```
nco_manzoma/
├── README.md              # project overview and quick start
├── docs/                  # ← you are here
├── front/manzoma/         # Vue 3 single-page application
├── backend/               # Django project, API, Oracle scripts, Compose file
└── web_server_nginx/      # edge nginx configuration
```
