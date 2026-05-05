# Parity Matrix

## Purpose

This matrix tracks the required functional equivalence between the legacy application and `netq-log-platform`.

## Status legend

- `Pending`
- `In Progress`
- `Ready for Validation`
- `Validated`
- `Blocked`

## Module parity matrix

| Module | Legacy behavior | Target behavior | Priority | Status | Notes |
|---|---|---|---|---|---|
| Authentication | LDAP login with domain, username and password | Same business behavior through FastAPI auth flow | Critical | Pending | Must preserve failure and redirect semantics functionally |
| Authorization | Access depends on allowed-user list and LDAP success | Same access rules with explicit authorization layer | Critical | Pending | Need to catalog permission source and fallback behavior |
| Session creation | Session created after successful login, stores `LOGGED_USERNAME`, sets 8h inactivity timeout | Equivalent secure session strategy with same business outcome | Critical | Pending | Decide cookie/session model early |
| Login API contract | Form POST to `/login.do` with redirect-based outcomes | `POST /api/v1/auth/login` with JSON request/response plus secure session cookie | Critical | Pending | Public error semantics should remain generic |
| Session bootstrap | JSP checks session server-side before rendering pages | `GET /api/v1/auth/session` determines authenticated state for Next.js | Critical | Pending | Must preserve access blocking on missing session |
| Session keep-alive | Browser calls `/doPing.do?ping=<timestamp>` every 5 minutes and refreshes cookie lifetime to 8h | Equivalent session preservation or explicit expiration policy | High | Pending | Must avoid unexpected logout regressions |
| Keep-alive API contract | Ping endpoint has no business payload and refreshes cookie/session lifetime | `POST /api/v1/auth/keep-alive` returns explicit session renewal metadata | High | Pending | 5-minute cadence should stay explicit |
| Logout | Invalidates session, clears matching session cookie, sets no-cache headers and redirects to login | Same business outcome | High | Pending | Redirect target is `index.jsp` in legacy |
| Logout API contract | `GET|POST /logout.do` always ends in login redirect | `DELETE /api/v1/auth/session` invalidates session and returns `redirectTo=/login` | High | Pending | Keep user-visible result idempotent |
| Main navigation | Menu loads Audit Logs and SIGRA content | Next.js shell with same module access | High | Pending | UI can change visually, not functionally |
| Audit Logs main query | Query by env + type + ID, with branch logic by `req` and `tid` | Same lookup capability through API + UI | Critical | Pending | Most important operational flow |
| SAPA query | Separate lookup by SAPA ID through `req=sapa` | Same lookup flow | Critical | Pending | Should remain accessible inside Audit Logs module |
| NETQ combined query | Combines audit payload, mongo payload, order type and recursive related ids | Equivalent structured response and UI behavior | Critical | Pending | Highest-risk parity area in operational module |
| External ID query | For `TIBCO`, `NETWIN`, `SIGRA`, `NA`, performs single audit lookup | Same single-payload behavior | High | Pending | QA path URL-encodes `#` to `%23` |
| NetQ related records | Lazy expansion of related content discovered recursively from mongo response | Equivalent expandable details | Critical | Pending | Sensitive parity area |
| Left/right panels | Left panel shows mongo payload, right panel shows audit payload | Equivalent UX structure | High | Pending | Visual redesign allowed, semantic behavior must remain |
| Payload viewing | XML/JSON shown with syntax highlighting | Equivalent readable code viewer | Medium | Pending | No need to preserve exact library |
| SIGRA validation | Validate AC format before request | Same validation rule | Critical | Pending | Preserve format constraints |
| SIGRA SOAP request | Build and send SOAP request | Same external behavior | Critical | Pending | Must validate request envelope and timeout behavior |
| SIGRA response view | Show request and response payloads | Same business outcome in new UI | High | Pending | Readability matters for operators |
| Logging and observability | Legacy logging exists through Log4j | Structured logs and metrics in new stack | High | Pending | New implementation can improve internals |
| Configuration loading | Files under `catalina.base/conf/NetQTools` | Env vars + ConfigMaps + Secrets | Critical | Pending | Must preserve environment-specific behavior |
| Container execution | Not container native today | Must run in Docker and Kubernetes | Critical | Pending | New requirement |

## Validation checklist by module

### Authentication

- [ ] Valid domain can be submitted
- [ ] Empty username fails
- [ ] Empty password fails
- [ ] Unauthorized user fails
- [ ] Invalid LDAP credentials fail
- [ ] Valid authorized user succeeds
- [ ] Successful login creates authenticated session state
- [ ] Successful login applies approved session timeout policy
- [ ] Session keep-alive behavior is implemented or intentionally replaced with approved equivalent
- [ ] Logout returns user to non-authenticated state
- [ ] Session expiration behavior is approved

### Audit Logs

- [ ] Query by environment works
- [ ] Query by each ID type works
- [ ] Query by request ID works
- [ ] Query by SAPA ID works
- [ ] `prodMongo + NETQ` combined query matches expected behavior
- [ ] `qaMongo + NETQ` combined query matches expected behavior
- [ ] Non-`NETQ` query returns single payload behavior
- [ ] QA non-`NETQ` query preserves `#` encoding behavior where applicable
- [ ] Empty result handling is approved
- [ ] Timeout/error handling is approved
- [ ] Related records load correctly
- [ ] Left/right detail behavior is approved

### SIGRA

- [ ] AC input validation matches legacy rule
- [ ] Successful SOAP request works
- [ ] Error SOAP response is handled
- [ ] Timeout behavior is handled
- [ ] Request/response payloads are visible and readable

### Platform and operations

- [ ] Backend health endpoint works
- [ ] Frontend starts correctly
- [ ] Docker images build successfully
- [ ] Application deploys to Kubernetes
- [ ] Readiness and liveness probes work
- [ ] Logs and metrics are available
