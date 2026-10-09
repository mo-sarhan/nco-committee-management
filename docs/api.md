# API guide

Base path: **`/api/v1/`** — assembled in `backend/nco/apps/api/v1/urls.py`, mounted from `backend/nco/nco/urls.py`.

## Discovery

| URL | What it is |
| --- | --- |
| `/api/v1/` | DefaultRouter index (browsable list of registered routes) |
| `/api/v1/swagger/` | Swagger UI (drf-yasg) |
| `/api/v1/swagger/redoc/` | ReDoc |
| `/admin/` | Django admin (jazzmin) |

The interactive schema is the source of truth for request/response shapes — viewsets and serializers change more often than this document. Use it for exact fields, filters and available methods.

```sh
python manage.py runserver 8000 --settings=nco.settings.sqlite_set
# then open http://localhost:8000/api/v1/swagger/
```

## Authentication

### Obtain a token

```http
POST /api/v1/login/
Content-Type: application/json

{ "username": "…", "password": "…" }
```

`CustomTokenObtainView` (`apps/users/views.py`) extends the SimpleJWT pair with:

```json
{
  "access": "eyJhbGciOi…",
  "refresh": "eyJhbGciOi…",
  "is_superuser": false,
  "role": ["committee_admin"],
  "info": {
    "id": 1,
    "username": "…",
    "first_name": "…",
    "last_name": "…",
    "email": "…",
    "is_staff": false,
    "is_superuser": false,
    "profile": {
      "mil_no": "…",
      "rank_name": "…",
      "rank_code": 12,
      "job": 3,
      "army_code": "1234",
      "prnt_army_code": "1000",
      "profile_photo": "/images/profiles/…"
    }
  }
}
```

- **`role`** is the list of Django **group names** for the user.
- **`info`** is `UserSerializerBasic` (user + nested `profile`).
- Refresh endpoint: `/api/v1/token/refresh/` is **not** registered — the frontend treats the access token as long-lived and logs out on 401.

### Use a token

```http
GET /api/v1/persons/
Authorization: Bearer <access>
```

| Setting | Value | Where |
| --- | --- | --- |
| Default authentication | `rest_framework_simplejwt.authentication.JWTAuthentication` | `nco/settings/base.py` (`REST_FRAMEWORK`) |
| Header type | `Bearer` | `SIMPLE_JWT.AUTH_HEADER_TYPES` |
| Access lifetime | 7 days | `SIMPLE_JWT.ACCESS_TOKEN_LIFETIME` |
| Refresh lifetime | 1 day | `SIMPLE_JWT.REFRESH_TOKEN_LIFETIME` |
| Algorithm | `HS256`, signed with `SECRET_KEY` | `SIMPLE_JWT` |

### Permissions

Most endpoints require authentication (`IsAuthenticated`); several add object-level checks.

| Permission class | Behaviour |
| --- | --- |
| `IsOwnerOrSuperUser` | Object must belong to the caller, or caller is superuser |
| `AllowToAddOrEditPerson` | ⚠️ view-level check always passes; object-level ownership/superuser only |
| `AllowToVote`, `AllowToSetOpinion` | Caller must be a `LagnaMember` of that committee |
| `AllowToSetReview`, `AllowToSetConf`, `AllowToSetWaitingDate` | Committee member or superuser |
| `HasPermToRejectPhoto` | Superuser or `photos.can_reject_photo` |
| `ReadAnyWriteStaff` | Reads: any authenticated user. Writes: staff/superuser or `uisettings.can_manage_ui_settings` |

Custom model permissions: `person.can_see_all_people`, `lagna.can_see_main_lagna`, lagna review/confirm/waiting-date permissions, `photos.can_reject_photo`, `report.can_see_all_army`, `uisettings.can_manage_ui_settings`.

Grant them at `/admin/` → Users/Groups → Field permissions.

## Conventions

- **Pagination** — `PAGE_SIZE = 20` is configured as a setting, but no default pagination *class* is registered, so each viewset supplies its own (`CustomPaginator`, `AccountCustomPaginators`, `CustomReportPaginator`). Check the response envelope per resource.
- **Dates** — request and response date format is `YYYY-MM-DD` (`DATETIME_FORMAT`, `DATETIME_INPUT_FORMATS`).
- **Soft deletes** — committee rows (`LagnaPersons`, `Lagna`, `LagnaAfrSnapData`, photo rows) are usually flagged rather than removed; use `all_objects`-backed admin endpoints or filtered queries to see inactive rows.
- **Content type** — the frontend's axios default is `multipart/form-data`; JSON endpoints must set `Content-Type: application/json` explicitly.
- **Soft-caps** — `army/` limits dynamic filtering to 10 results.

## Endpoint catalogue

### Core / auth

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| POST | `/api/v1/login/` | `CustomTokenObtainView` | JWT + extended claims |
| GET | `/api/v1/swagger/` | drf-yasg | Schema UI (`AllowAny`) |
| GET | `/api/v1/swagger/redoc/` | drf-yasg | ReDoc (`AllowAny`) |

### Personnel

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| GET/POST | `/api/v1/persons/` | `AfrPersonView` | List/create; dynamic filtering by army codes |
| GET/PUT/PATCH/DELETE | `/api/v1/persons/<mil_ser>/` | `AfrPersonView` | Detail |
| *nested* | `/api/v1/persons/<mil_ser>/units/…`, `/photos/…`, `/psychologic/…`, `/security/…` | mixins on `AfrPersonView` | Unit history, photos, psychological reports, security situation |

### Photos

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/photo/` | `UploadImageView` | Returns photo types |
| POST | `/api/v1/photo/` | `UploadImageView` | Multipart upload (`file`, `photo_type`, `photo_family_serial` …) |
| GET | `/api/v1/rejection-reasons/` | `RejectImageView` | Rejection reason lookup |
| POST | `/api/v1/rejection-reasons/` | `RejectImageView` | Accept or reject a photo |

### Reports

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/photo/report/` | `PhotoReportViewSet` | Photo coverage report; totals on the last page |
| GET | `/api/v1/photo/report/<prnt_army_code>/units` | `PhotoReportViewSet` | Units within a parent army |
| GET | `/api/v1/photo/report/<prnt_army_code>/units/<unit>/persons` | `PhotoReportViewSet` | Persons within a unit |
| GET | `/api/v1/photo/report/<prnt_army_code>/persons` | `PhotoReportViewSet` | Person-level coverage |
| GET | `/api/v1/report/lagna/` | `LagnaAfrReportViewSet` | Committee statistics with totals |

### Committees (lagna)

| Method | Path | View |
| --- | --- | --- |
| GET/POST | `/api/v1/lagna/` | `LagnaViewSet` |
| GET/PUT/PATCH/DELETE | `/api/v1/lagna/<code>/` | `LagnaViewSet` |
| GET | `/api/v1/lagna/main?committe_category=2` | `LagnaViewSet` (main committees) |
| GET | `/api/v1/lagna/get-lagna-type/` | `LagnaViewSet` |
| GET | `/api/v1/lagna/get-lagna-category/` | `LagnaViewSet` |
| *nested* | `/api/v1/lagna/<code>/lagna-spacific/…` | `LagnaViewSet` + mixins |
| GET/POST | `/api/v1/lagna-persons/` | `LagnaPersonsViewSet` |
| GET/POST | `/api/v1/lagna-member/` | `LagnaMemberViewSet` |
| GET/POST | `/api/v1/lagna-persons-opinion/` | `LagnaPersonsOpinionViewSet` |
| GET/POST | `/api/v1/lagna-spacific/` | `LagnaTypeSpacificViewSet` |
| GET | `/api/v1/opinion-types/` | `LagnaOpinionsViewSet` |
| GET | `/api/v1/pons-cons/` | `ConsPonsViewSet` |
| GET | `/api/v1/benefit/` | `BenefitTypeViewSet` |
| GET | `/api/v1/commander-job/` | `CommanderJobTypeViewSet` |
| GET | `/api/v1/person-status/` | `LagnaAfrStatusViewSet` |

**Nested actions under `/api/v1/lagna/<code>/lagna-spacific/<id>/`** (the bulk of the workflow) include:

| Segment | Purpose |
| --- | --- |
| `persons/`, `persons/add/`, `persons/<pid>/`, `persons/<pid>/delete/` | Person placement |
| `persons/<pid>/snap/` (GET/POST) | Snapshot of the person for this session |
| `persons/<pid>/status/` | Status transitions |
| `persons/<pid>/decision/` (+ `add`, `delete`) | Final decision |
| `persons/<pid>/opinions/` (+ `add`, `…/delete/`) | Opinions |
| `persons/<pid>/reasons/` (+ `add`, `…/delete/`) | Reasons |
| `persons/<pid>/add-reason/` (GET/PATCH) | The single "why is this person here" reason |
| `persons/<pid>/show/` | Presentation-screen payload |
| `members/`, `members/add/`, `members/<mid>/delete/` | Membership |
| `report`, `photo-report` | Session statistics |
| `ready` | Readiness check |
| `event/` | Push an event to the presentation screen |

⚠️ Exact sub-paths vary with the `@action(url_path=…)` declarations in `apps/lagna/mixins.py` — verify against Swagger before integrating.

### Accounts

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| GET | `/api/v1/accounts/` | `AccountViewSet` | Returns `[request.user]` (paginated via `AccountCustomPaginators`) |
| GET | `/api/v1/accounts/comm/` | `AccountViewSet.comm` | Committees the user is a member of (`detail=False`, so **no** username segment) |

### Reference data

| Method | Path | View |
| --- | --- | --- |
| GET | `/api/v1/army/` | `ArmyCodeViewSet` (dynamic filter, capped at 10) |
| GET | `/api/v1/rank/` | `RankViewSet` |

### UI settings

| Method | Path | View | Notes |
| --- | --- | --- | --- |
| GET/POST | `/api/v1/ui-settings/sections/` | `UiSectionViewSet` | `ReadAnyWriteStaff`; filter with `?page_key=` |
| GET/PUT/PATCH/DELETE | `/api/v1/ui-settings/sections/<id>/` | `UiSectionViewSet` | |
| POST | `/api/v1/ui-settings/sections/reorder/` | `UiSectionViewSet.reorder` | Ordered array payload |
| GET/POST | `/api/v1/ui-settings/fields/` | `UiFieldViewSet` | Filter with `?section=` |
| GET/PUT/PATCH/DELETE | `/api/v1/ui-settings/fields/<id>/` | `UiFieldViewSet` | |
| POST | `/api/v1/ui-settings/fields/reorder/` | `UiFieldViewSet.reorder` | Ordered array payload |
| GET | `/api/v1/ui-settings/pages/<page_key>/` | `UiPageConfigView` | Full page layout (sections + fields) |

Seeded with `python manage.py seed_ui_settings`.

## Gaps: frontend calls with no backend route

The following paths are requested by `front/manzoma/src/api/modules/*` but are **not registered** in `apps/api/v1/urls.py` and have no `@action`/`path()` anywhere. They will return **404** (the UI usually fails silently or logs an error).

| Frontend call | Requested path | Where |
| --- | --- | --- |
| `authApi.logout()` | `POST /api/v1/logout` | `src/api/modules/auth.js:7` |
| `authApi.getProfile()` / `getProfileCancelable()` | `GET /api/v1/me` | `auth.js:8,13` |
| `getUnits()` | `GET /api/v1/units/` | `src/api/modules/persons.js:4` (unit history is actually at `persons/<pk>/units/`) |
| `getImagesReport()` | `GET /api/v1/get_images_report/` | `persons.js:5` |
| `getPersonDetails(mil_ser, op)` | `GET /api/v1/person/<mil_ser>/` | `persons.js:6` (actual detail route is `persons/<mil_ser>/`) |
| `postAttendance()` | `POST /api/v1/attend_person/<mil_ser>/` | `persons.js:10` |
| `getVote()` | `GET /api/v1/vote/<mil_ser>/` | `persons.js:12` |
| `getLagnaStatistics()` | `GET /api/v1/get_lagna_statistics/` | `persons.js:13` |
| `getUploadedImagesReport()` / `getReviewedImagesReport()` | `GET /api/v1/report/` | `persons.js:17-18` — only `/api/v1/report/lagna/` is registered, and both functions are identical anyway |

Also worth knowing:

- `apps/person/urls.py` is an **empty file** — the person routes come entirely from the `DefaultRouter` in `apps/api/v1/urls.py`.
- `getUploadedImagesReport` and `getReviewedImagesReport` hit the same URL with the same body, so they cannot return different data.
- The photo report lives under **`/api/v1/photo/report/`** (not `/api/v1/report/`), because `report_router` is included at `path('photo/', …)`.

See [troubleshooting.md](troubleshooting.md#frontend-endpoint-mismatches).

## WebSockets

WebSockets are served by the **ASGI** application (`nco/asgi.py`) and mounted under two prefixes:

| Service | Mount | Route | Consumer |
| --- | --- | --- | --- |
| Reports | `report/` | `/report/wss/photo/report/` | `PrntPhotoReportConsumer` |
| Committee screen | `lagna/` | `/lagna/ws/lagna/` | `LagnaShowConsumer` |

### Authentication

Both accept the JWT as a **query parameter**, not an `Authorization` header:

```
ws://host/ws/lagna/?token=<access-token>&lagna=<committee_code>
/report/wss/photo/report/?token=<access-token>
```

`JWTAuthMiddleware` (`apps/report/middleware.py`) validates the token and sets `scope["user"]`; anonymous connections are closed.

### Committee screen (`LagnaShowConsumer`)

On connect the consumer:

1. reads `lagna` from the query string,
2. verifies the user is a `LagnaMember` of that committee (`user.lagna_member`),
3. determines `member_type` (`head` when `member_type_code == 1`, otherwise `voter`; superusers without a membership row are treated as `head`),
4. joins `comm_<code>` and `comm_<code>_<member_type>`,
5. sends `settings`, then any cached `comm_<code>` payload.

Server → client events:

| Event | Payload | Meaning |
| --- | --- | --- |
| `settings` | `{ event, settings: { socket_group, open_final_decision } }` | Member-type capabilities for this client |
| `show_person` | `event.data` | Person pushed to the screen |
| `send_votes` | `event.data` | Vote tallies |
| `show_comm_report` | `event.data` | Live committee statistics |
| `notify` | `message`/`data`/`event` | Generic notification |

Helper: `apps/lagna/utilts.py` → `send_websocket_data(data, group, type)`.

### Photo report (`PrntPhotoReportConsumer`)

Groups:

- superuser **or** `report.can_see_all_army` → `photo_report`
- otherwise → `photo_report_<user.profile.prnt_army_code_id>`

On connect it pushes the current report (`services/generate_photo_report.generate_photo_report(...)`); later updates arrive as `report_update` events whenever `calculate_person_photos` recomputes coverage.

### Client side

The Vue client builds URLs in `src/composables/useSocket.js` and manages connections in `src/stores/useWebSocketStore.js` (see [frontend.md](frontend.md#websockets)). Nginx proxies `/wss/` to the backend — see [deployment.md](deployment.md#websocket-proxying).

## Error handling

Errors follow DRF's standard shape:

```json
{ "detail": "…" }
```

or field-level:

```json
{ "field_name": ["…"] }
```

Some endpoints add a `message` / `details` key that the frontend reads (`src/utils/handleApiError.js`, `src/api/http.js`). On **401** the frontend clears `localStorage` and routes to `/login`.

## Quick cURL examples

```sh
# Login
curl -s -X POST http://localhost:8000/api/v1/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"…"}'

# Authenticated list
curl -s http://localhost:8000/api/v1/persons/ \
  -H "Authorization: Bearer $TOKEN"

# Committee detail
curl -s http://localhost:8000/api/v1/lagna/CODE/ \
  -H "Authorization: Bearer $TOKEN"

# UI page config
curl -s http://localhost:8000/api/v1/ui-settings/pages/profile/ \
  -H "Authorization: Bearer $TOKEN"

# WebSocket (needs wscat)
npx wscat -c "ws://localhost:8000/lagna/ws/lagna/?token=$TOKEN&lagna=CODE"
```

## Related

- [backend.md](backend.md) — models, settings, permissions
- [architecture.md](architecture.md) — system overview
