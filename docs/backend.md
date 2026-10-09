# Backend (Django)

Django project root: `backend/nco/`

```
backend/
├── requirement.txt          # Python dependencies (unpinned)
├── docker-compose.yml       # PostgreSQL, Redis, RabbitMQ, pgAdmin, NSFW service
├── .db.env                  # PostgreSQL credentials (local, not for VCS)
└── nco/
    ├── manage.py            # entry point (defaults to DJANGO_SETTINGS_MODULE=nco.settings)
    ├── nco/                 # project package
    │   ├── settings/        # base + per-environment modules
    │   ├── urls.py          # /admin/ and /api/v1/
    │   ├── asgi.py          # HTTP + Channels (WebSocket) routing
    │   ├── wsgi.py
    │   ├── celery.py        # Celery application
    │   ├── refrence.py      # stale scratch file (not imported)
    │   └── db.sqlite3       # local dev database (large; keep out of VCS)
    ├── apps/                # domain applications (see below)
    ├── utilts/              # shared converters/filters (note the spelling)
    └── oracle_*.sql         # Oracle DDL + lookup data
```

## Quick start

```sh
cd backend/nco
python -m venv ../nco_env && source ../nco_env/bin/activate      # or your own env
pip install -r ../requirement.txt

python manage.py check      --settings=nco.settings.sqlite_set
python manage.py migrate    --settings=nco.settings.sqlite_set
python manage.py createsuperuser --settings=nco.settings.sqlite_set
python manage.py runserver 8000 --settings=nco.settings.sqlite_set
```

Then open:

| URL | Purpose |
| --- | --- |
| `http://localhost:8000/api/v1/` | API root (DefaultRouter browsable index) |
| `http://localhost:8000/api/v1/swagger/` | Swagger UI |
| `http://localhost:8000/api/v1/swagger/redoc/` | ReDoc |
| `http://localhost:8000/admin/` | Django admin (jazzmin theme) |

**Always pass `--settings=`.** `manage.py`, `wsgi.py` and `asgi.py` all default to `nco.settings`, which is an **empty package `__init__.py`** — bare invocation has no `DATABASES` and will fail. See [troubleshooting.md](troubleshooting.md#settings-package-is-empty).

## Settings modules

Located in `backend/nco/nco/settings/`. Each does `from .base import *` and then overrides.

| Module | Default DB | Other DB aliases | `DEBUG` | `MANAGED_MIGRATIONS` | Intended use |
| --- | --- | --- | --- | --- | --- |
| `base.py` | *(none defined)* | — | `True` | — | Shared config only; never used alone |
| `dev.py` | **PostgreSQL** `localhost:5432/nco` | `sqlite` | `True` | `True` | Local Postgres development |
| `sqlite_set.py` | **SQLite** `nco/db.sqlite3` | `oracledb` | `True` | `True` | Zero-dependency local development |
| `production.py` | **SQLite** `nco/db.sqlite3` | `postgres`, `oracle` | `False` | `True` | Production profile (CORS, HSTS, secure cookies on) |
| `oracle.py` | ⚠️ **none** | `oracledb`, `sqlite` | `False` | `False` | Oracle — but has no `default` key, see below |
| `dump.py` | — | — | — | — | Utility settings for data dumps |
| `__init__.py` | — | — | — | — | **Empty** |

> ⚠️ `oracle.py` defines `DATABASES` without a `default` entry, so Django cannot resolve a default connection with that module. Prefer `sqlite_set.py`/`dev.py`, or add a `default` key before using it.

### What `base.py` configures

| Area | Setting |
| --- | --- |
| Security | `SECRET_KEY` **hardcoded**, `DEBUG = True`, `ALLOWED_HOSTS = ['localhost','afrad.oma.mil','192.9.202.46']` |
| Apps | jazzmin, `apps.users`, DRF, SimpleJWT, django.contrib.*, drf-yasg, corsheaders, storages, then `apps.api.v1`, `customadmin`, `person`, `report`, `lagna`, `photos`, `tanzem`, `uisettings` |
| Middleware | `corsheaders.middleware.CorsMiddleware` first, then the standard Django stack |
| REST Framework | `DEFAULT_AUTHENTICATION_CLASSES = JWTAuthentication`, `PAGE_SIZE = 20`, `DATETIME_FORMAT = "%Y-%m-%d"`, `DATETIME_INPUT_FORMATS = ["%Y-%m-%d"]`. No default pagination class is set — each viewset supplies its own paginator. |
| JWT (`SIMPLE_JWT`) | access **7 days**, refresh **1 day**, `HS256` signed with `SECRET_KEY`, `AUTH_HEADER_TYPES = ("Bearer",)`, `UPDATE_LAST_LOGIN = True`, `ROTATE_REFRESH_TOKENS = False` |
| Channels | `CHANNEL_LAYERS = InMemoryChannelLayer` (single-process only) |
| Cache | Redis `redis://cache:6379/1`, `KEY_PREFIX='nco'`, `TIMEOUT=300` |
| Celery | `CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"` |
| Storage | `STORAGES['default']` = `S3Storage` with **placeholder test credentials** and endpoint `http://localhost:4566` (LocalStack-style) |
| Static/media | `STATIC_URL`, `MEDIA_URL = '/images/'` — `STATIC_ROOT`/`MEDIA_ROOT` are set per environment module |
| Misc | `DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000`, `APPEND_SLASH = True`, `X_FRAME_OPTIONS = 'SAMEORIGIN'`, `SILENCED_SYSTEM_CHECKS = ['security.W019']` |

**`production.py`** additionally enables `SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`, one-year HSTS, `SECURE_CONTENT_TYPE_NOSNIFF`, `SESSION_COOKIES_HTTPONLY`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, sets `ALLOWED_HOSTS`/`CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS` to `www.afrad.mil.eg`, and sets `MEDIA_ROOT` to a Windows path.

**Treat every credentials string in these files as sensitive.** `SECRET_KEY`, database passwords, and S3 keys are committed in source — rotate them and move them to environment variables before any real deployment.

## Applications

Registered in `base.py`. `apps/api/v1` is the URL assembly layer and has no models.

### `apps.tanzem` — reference / lookup data

| Model | Table | Purpose |
| --- | --- | --- |
| `ArmyCode` | `COD_ARMY_CODE` (`"HAYAA"."COD_ARMY_CODE"` on Oracle) | Unit/army codes (`army_code` PK, `army_name`, `army_chk`) |
| `Rank` | `RANK_CODE` | Ranks with sort order |
| `ArmyParentChild` | `CH_PAR_ARMY_CODE` | Parent/child unit hierarchy |
| `Jobs` | `JOBS` | Job titles with order and active/delete flags |
| `FamilyDegreeCode` | `FAMILY_DEGREE_CODE` | Family relationship degree lookup |

Table names are chosen conditionally: Oracle engine → `HAYAA.<TABLE>`, otherwise the bare name. All are `managed = getattr(settings, 'MANAGED_MIGRATIONS', False)`.

### `apps.users` — accounts

| Model | Table | Notes |
| --- | --- | --- |
| `Profile` | `USERS_PROFILE` | `OneToOneField(User, related_name='profile')`; `mil_no`, `rank_name`, `rank_code` → `Rank`, `job` → `Jobs`, `army_code`/`prnt_army_code` → `ArmyCode`, `profile_photo` (uploads to `profiles/<username>/<ts>/`) |

- `apps/users/signals.py` — `post_save` on `User` creates or saves the `Profile`.
- Custom model permission conventions are used across the project rather than a custom user model (`AUTH_USER_MODEL` is unchanged).

### `apps.person` — personnel records

Core model **`AfrPerson`** (`AFR_PER_DATA`, PK `mil_ser`, unique `mil_no`):

- Two managers: `objects = ActiveManager()` (filters `person_status_code` in `(1, 2)`) and `all_objects`.
- FK to `AfrDegree` (`degree_code`), custom permission `can_see_all_people`.
- `Meta.managed` follows `MANAGED_MIGRATIONS`.

Related models:

| Model | Table | Notes |
| --- | --- | --- |
| `AfrDegree` | lookup | Degree/rank groupings, `degree_order` |
| `Family` | `AFR_SEG_FAMILY` | FK `mil_ser`; father/mother/wives/children rows |
| `FamilyStatistic` | `MV_FAMILY_STATISTIC` | Read-only statistic (DB view) |
| `AfrPunishment` | — | Discipline records with composite unique constraint |
| `AfrTagdedHistroy` | `AFR_TAGDED_TARAKY_DATA` | Career progression history |
| `PersonEffecincy`, `PersonEffecincyL3Y`, `PersonEffecincyAvg` | views | Efficiency metrics |
| `PunishmentStatistics`, `MedicalLagnaResultLookUp`, `MedicalHistory` | — | Aggregates and medical history |
| `AfrEducation` | — | Education/qualification records |
| `AfrUnits` | — | Unit postings history, composite unique |
| `AfrTravel`, `AfrVacation` | — | Travel and leave records |
| `AfrPsychologicalReport` | — | `attach` image → `…/psychological_report/<ts>/`, FK `person`, FK `user` |
| `AfrSecuritySituation` | — | `sec_attach` image → `…/security/<ts>/`; `SecurityActiveManager` + `all_objects` |

`FamilyManager` (in `models.py`) declares helper querysets for relations; some filter lists are placeholders and are incomplete.

### `apps.lagna` — committees (largest app)

Lookups: `LagnaStatusType`, `LagnaType`, `LagnaCategory`, `VoteType`, `LagnaMemberType` (carries `socket_group` and `open_final_decision`), `LagnaVoteOpinoin`, `LagnaAfrStatus`, `CommanderJobType`, `BenefitType`, `PonsConsType`.

| Model | Purpose |
| --- | --- |
| `Lagna` | A committee. Self FKs (`parent`, `root`) distinguish main vs sub committees; `ActiveManager`/`all_objects`; unique constraints per category; permission `can_see_main_lagna`. Date validation in `clean()`. |
| `LagnaTypeSpacific` | A *specific session* of a committee; FK `lagna`, self FK `parent_spacific`; session dates must fall inside the parent's. |
| `LagnaMember` | Membership with `member_type` (head/voter) and `army_code`; unique constraint so only one head per committee. |
| `LagnaPersons` | A person placed before a committee; `LagnaPersonManager`; status via `lagna_afr_status`, soft delete; permissions for review/confirmation/waiting date. |
| `OpinionType` | Opinion template with `lagna_type` and `job`; opinion-related permissions. |
| `LagnaPersonVotes` | Votes: FK `lagna_person`, `vote_type`, `opinion_type`, `user`. |
| `LagnaAfrSnapData` | **Snapshot** of a person for a committee (unique on person + root committee + type); `add_reason` free text; `attach` image → `comm_attach/<root>/snaps/<mil_no>/<ts>/`. `AfrSnapActiveManager`. |
| `LagnaPersonReasons` | Reasons attached to a snap; attach path `comm_attach/<committe>/<type>/<person>/<ts>/`. |
| `AfrSnapOpinion` | Opinions on a snap (unique active per snap + opinion type); attach path `comm_attach/<root>/opinions/<mil_no>/<ts>/`. |
| `AfrSnapFinalDecition` | Final decision recorded on a snap. |
| `LagnaCommanderData`, `LagnaCommSnapDetail` | Commander records and snap↔commander links. |
| `LagnaPersonPonsCons`, `LagnaPersonsOpinions` | Per-person pons/cons and person-level opinions. |

Signals (`apps/lagna/signals.py`): creating a `LagnaPersons` row seeds snap opinion placeholders.

Most of the business logic lives in `apps/lagna/mixins.py` (~1,678 lines) mixed into `LagnaViewSet`, and in `services/create_lagna_services.py` / `services/get_or_create_snap.py`.

### `apps.photos` — photo intake

| Model | Purpose |
| --- | --- |
| `PhotoType` | Photo kinds (small/tall/family) with sort order, soft delete |
| `PhotoStatusType` | Review status lookup; default `0` |
| `PhotoInfo` | The photo row: `photo_path` → `<army_code>/<mil_no>/<ts>/<file>`, FK person/type/status/degree, `create_user`, `review_user`, `is_nsfw`, `photo_family_serial` (validated 1–4 in `clean()`), custom managers, permission `can_reject_photo`. `save()` derives degree from the person. |
| `RejectPhotoReason` | Rejection reason lookup |
| `RejectPhotoInfo` | Rejection history: photo, person, reason, `review_user` |

Upload flow is described under [Photo pipeline](#photo-pipeline).

### `apps.report` — aggregates and live reports

Read-only models mapped to views: `PrntPhotoReport` (`V_PER_PHOTO_ST_PRNT`, permission `can_see_all_army`), `UnitPhotoReport` (`V_PER_PHOTO_ST_UNIT`), `LagnaAfrReport` (`V_COMM_PER_STATUS`), `LagnaAfrOpinionsReport` (`V_COMM_PER_OPINIONS`), plus writable `AfrPhotoReport` (`AFR_PHOTO_CH_INOF`, OneToOne to `AfrPerson`, `AfrPhotoActiveManager`).

Also holds the report WebSocket stack: `consumers.py`, `routing.py`, `middleware.py`, `middleware_stack.py`.

### `apps.uisettings` — runtime UI configuration

| Model | Purpose |
| --- | --- |
| `UiSection` | A section on a page: `page_key` + `section_key` (unique pair), ordering, soft delete, styling fields from abstract `StyleMixin`, permission `can_manage_ui_settings` |
| `UiField` | A field inside a section: FK `section` (related name `fields`), `field_key`, ordering, styling; unique `(section, field_key)` |

Both use `ActiveManager` (hide soft-deleted). Seeded by `python manage.py seed_ui_settings`.

### `apps.api.v1` — route assembly only

No models. `urls.py` (142 lines) registers every router and the Swagger schema. See [api.md](api.md).

### `apps.customadmin` — admin extras

- `admin.py` registers Django's `Permission` model.
- Management commands: `dumps` (bulk data migration out of Oracle with chunking and FK ordering), `upload_opinions` (Excel import of committee persons, reasons and opinions).
- ⚠️ `apps/customadmin/management/__init___.py` has **three** trailing underscores — the package init is effectively missing, which can prevent `manage.py` from discovering these commands.

### `apps.schadule` — placeholder

Empty models/views; `apps/schadule/celery.py` creates a second Celery app with `DJANGO_SETTINGS_MODULE="project.settings"` (a non-existent module). Not installed in `INSTALLED_APPS`, so it is inert but misleading.

## Authentication and authorization

### Login

`POST /api/v1/login/` → `CustomTokenObtainView` (`apps/users/views.py`), a `TokenObtainPairView` whose serializer (`CustomTokenObtainPairSerializer`) extends the standard payload with:

```json
{
  "access": "…", "refresh": "…",
  "is_superuser": false,
  "role": ["<group name>", "…"],
  "info": { "…user + nested profile…" }
}
```

Roles come from Django **group names** (`user.groups.all().values_list('name', flat=True)`). There is no custom role table.

### Requests

```http
Authorization: Bearer <access-token>
```

Access tokens live 7 days; there is **no refresh endpoint wired up** in the frontend — an expired token results in a 401 and a redirect to `/login`.

### Permission classes

| Class | File | Rule |
| --- | --- | --- |
| `IsOwnerOrSuperUser` | `apps/lagna/permissions.py` | Object-level: owner or superuser |
| `AllowToAddOrEditPerson` | `apps/lagna/permissions.py` | ⚠️ `has_permission()` returns `True` unconditionally; object check only |
| `AllowToVote`, `AllowToSetOpinion` | `apps/lagna/permissions.py` | Caller must be a `LagnaMember` of that committee |
| `AllowToSetReview`, `AllowToSetConf`, `AllowToSetWaitingDate` | `apps/lagna/permissions.py` | Committee member **or** superuser |
| `HasPermToRejectPhoto` | `apps/photos/permissions.py` | Superuser or `photos.can_reject_photo` |
| `ReadAnyWriteStaff` | `apps/uisettings/permissions.py` | Read: any authenticated user. Write: staff/superuser or `uisettings.can_manage_ui_settings` |

### Custom model permissions

`person.can_see_all_people`, `lagna.can_see_main_lagna`, `lagna` review/confirm/waiting-date permissions, `photos.can_reject_photo`, `report.can_see_all_army`, `uisettings.can_manage_ui_settings`.

Grant them via the Django admin (`/admin/`) under Groups or Users.

## Views and endpoints

Router registrations live in `apps/api/v1/urls.py`. Main viewsets:

| Viewset | App | Notes |
| --- | --- | --- |
| `AfrPersonView` | `person` | `ModelViewSet` + `AfrSecurityMixin`, `AfrPsychologicalReportMixin`, `AfrPersonPhotosMixin`, `AfrPersonUnitMixin`; `CustomPaginator`; dynamic filtering by army/prnt army |
| `LagnaViewSet` | `lagna` | The largest: main list, `get_lagna_type`, `get_lagna_category`, `controler`, SSE-style `cache_lagna_person`/`event_stream`, plus nested `lagna-spacific/<id>/…` actions for persons, members, reasons, snaps, status, votes, decisions and reports |
| `LagnaPersonsViewSet` | `lagna` | Person placement; `destroy` is a soft delete |
| `LagnaMemberViewSet` | `lagna` | Members, with `GetVoteMemberMixin` |
| `LagnaPersonsOpinionViewSet`, `LagnaOpinionsViewSet` | `lagna` | Opinions on persons / opinion type lookup |
| `LagnaTypeSpacificViewSet` | `lagna` | Specific sessions |
| `ConsPonsViewSet`, `BenefitTypeViewSet`, `CommanderJobTypeViewSet`, `LagnaAfrStatusViewSet` | `lagna` | Lookups |
| `UploadImageView`, `RejectImageView` | `photos` | APIViews: GET returns the lookup list, POST performs upload / accept-reject |
| `PhotoReportViewSet` | `report` | Photo coverage report; aggregates totals on the final page |
| `LagnaAfrReportViewSet` | `report` | Committee statistics; aggregates totals |
| `AccountViewSet` | `users` | Account info; `@action(detail=True, methods=['get'], url_path='comm')` returns the committees the user belongs to; lookup by `username` |
| `ArmyCodeViewSet`, `RankViewSet` | `tanzem` | Read-only; `ArmyCode` supports dynamic filtering capped at 10 rows |
| `UiSectionViewSet`, `UiFieldViewSet`, `UiPageConfigView` | `uisettings` | CRUD + `reorder` actions + full page layout |

Pagination classes live alongside their apps: `apps/person/paginator.py`, `apps/users/paginators.py`, `apps/report/paginators.py`.

## Realtime

### Consumers

| Consumer | Mount | Query params | Groups | Outgoing events |
| --- | --- | --- | --- | --- |
| `PrntPhotoReportConsumer` (`apps/report/consumers.py`) | `/report/wss/photo/report/` | `token` | `photo_report` or `photo_report_<prnt_army_code>` | photo report payload on connect, then `report_update` |
| `LagnaShowConsumer` (`apps/lagna/consumers.py`) | `/lagna/ws/lagna/` | `lagna`, `token` | `comm_<code>` + `comm_<code>_head|voter` | `settings`, `show_person`, `send_votes`, `show_comm_report`, `notify` |

Authentication: `apps/report/middleware.py` (`JWTAuthMiddleware`) reads the `token` query parameter, validates it, and sets `scope["user"]`; wrapped by `JWTAuthMiddlewareStack` in `apps/report/middleware_stack.py`. Anonymous sockets are rejected.

Helpers: `apps/lagna/utilts.py` — `send_websocket_data(data, group, type)` and `get_web_socket_group(...)`.

### ASGI

`backend/nco/nco/asgi.py` builds a `ProtocolTypeRouter` with `http` → Django and `websocket` → `JWTAuthMiddlewareStack(URLRouter(report_routing + lagna_routing))`.

Run with an ASGI server for WebSockets:

```sh
python manage.py runserver 8000 --settings=nco.settings.sqlite_set
# or
daphne -b 0.0.0.0 -p 8080 nco.asgi:application
```

## Celery

`backend/nco/nco/celery.py`:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nco.settings.production')
app = Celery('nco')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

⚠️ `nco/__init__.py` has the `from .celery import app as celery_app` line **commented out**, so `manage.py runserver` does not auto-load the Celery app. Import it explicitly in a worker entrypoint.

```sh
celery -A nco.celery worker -l info
```

Broker: `amqp://guest:guest@localhost:5672//` (RabbitMQ from Compose). Flower is listed in `requirement.txt` for monitoring: `celery -A nco.celery flower`.

There is no beat schedule in the repository.

## Management commands

| Command | App | Purpose |
| --- | --- | --- |
| `python manage.py seed_ui_settings` | `uisettings` | Populate `UiSection`/`UiField` defaults (required before the Settings screen shows anything). Options: `--reset` (overwrite title/display_order of existing rows), `--page <key>` (seed only `afr_person_profile` or `lagna_presenting`) |
| `python manage.py change_user_army_code` | `users` | Copy `army_code` → `prnt_army_code` for every profile |
| `python manage.py upload_image` | `photos` | Bulk import photos from CSV |
| `python manage.py upload_rejected_photo` | `photos` | Bulk import rejections from CSV |
| `python manage.py upload_users` | `photos` | Bulk update user/profile army codes from CSV |
| `python manage.py upload_acceptable_photo` | `photos` | Bulk-mark photos accepted |
| `python manage.py create_afr_photo_report` | `photos` | ⚠️ Empty stub |
| `python manage.py dumps` | `customadmin` | Chunked data migration out of Oracle with FK-safe ordering |
| `python manage.py upload_opinions` | `customadmin` | Import committee persons/reasons/opinions from Excel |

Run any command with an explicit settings module, e.g. `--settings=nco.settings.sqlite_set`.

## Photo pipeline

1. **Upload** — `POST /api/v1/photo/` → `UploadImageView` → `apps/photos/services/upload_image_services.upload_photo(request)`:
   - validates the file and its type,
   - deactivates an existing photo of the same `(type, family_serial)`,
   - creates `PhotoInfo`, writing the file to `<army_code>/<mil_no>/<timestamp>/<filename>`,
   - broadcasts the photo report over WebSockets.
2. **Signals** — `apps/photos/signals.py` `post_save(PhotoInfo)` dispatches:
   - `calculate_person_photos.delay(photo_id)` — recomputes coverage flags (`completed_flag`, `checked_flag`, `approved_flag`), upserts `AfrPhotoReport`, pushes the report to `photo_report` / `photo_report_<prnt>`.
   - `check_photo_nsfw.delay(photo_id)` — calls the classifier.
3. **NSFW check** — `apps/photos/services/check_nsfw_photo.py` POSTs the file to `http://localhost:6086/api/upload_check` with `Authorization: Bearer <token>` (token is a placeholder), using a reused `requests.Session` with retry/backoff; result stored in `PhotoInfo.is_nsfw`.
4. **Review** — `POST /api/v1/rejection-reasons/` accepts or rejects, writing `RejectPhotoInfo`.
5. **Reporting** — `POST/GET` on the report routers plus `services/generate_photo_report.py` / `generate_lagna_report.py`, pushed live by `PrntPhotoReportConsumer`.

### Media layout

| Content | Path template |
| --- | --- |
| Profile photo | `profiles/<username>/<timestamp>/<file>` |
| Person photo | `<army_code>/<mil_no>/<timestamp>/<file>` |
| Psychological report | `<army_code>/<mil_no>/psychological_report/<timestamp>/<file>` |
| Security attachment | `<army_name>/<mil_no>/security/<timestamp>/<file>` |
| Committee snap | `comm_attach/<root_committe>/snaps/<mil_no>/<timestamp>/<file>` |
| Committee reason | `comm_attach/<committe>/<type>/<person>/<timestamp>/<file>` |
| Committee opinion | `comm_attach/<root_committe>/opinions/<mil_no>/<timestamp>/<file>` |

Storage backend is `STORAGES['default']` (S3 in `base.py`, with placeholder credentials). `MEDIA_URL` is `/images/`, which nginx serves from disk.

## Testing

`apps/*/tests.py` exist for `api/v1`, `customadmin`, `lagna`, `person`, `photos`, `report`, `schadule`, `tanzem`, `users` — most are Django boilerplate stubs.

```sh
python manage.py test --settings=nco.settings.sqlite_set
```

## Dependencies

`backend/requirement.txt` (all **unpinned** — record a lock file before deploying):

| Group | Packages |
| --- | --- |
| Web / admin | `django`, `django-jazzmin` |
| REST | `djangorestframework`, `djangorestframework_simplejwt`, `drf_yasg` |
| Async / ASGI | `daphne`, `uvicorn`, `channels-redis` (brings `channels`) |
| Tasks | `celery`, `flower` |
| Cache | `redis`, `django-redis` |
| Storage | `django-storages`, `boto3` |
| HTTP | `requests`, `urllib3` |
| CORS | `django-cors-headers` |
| Database | `psycopg` (PostgreSQL) |
| Data / images | `pandas`, `pillow` |

Notes:

- `django-filter` is **not** installed even though some views reference filtering helpers — check imports before relying on them.
- Oracle needs a driver (`oracledb`/`cx_Oracle`) that is not listed.
- `channels` is only pulled in transitively via `channels-redis`.

## Related

- [api.md](api.md) — endpoint catalogue, authentication, WebSocket protocol
- [development.md](development.md) — local workflows and commands
- [deployment.md](deployment.md) — nginx, Docker, database scripts
- [troubleshooting.md](troubleshooting.md) — known issues in the backend
