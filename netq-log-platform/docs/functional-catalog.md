# Functional Catalog

## Purpose

This document catalogs the current legacy system behavior that must be preserved during the migration to `netq-log-platform`.

The goal is to describe what the system does today before redesigning implementation details.

## Current legacy system summary

- Legacy application type: Java web application packaged as WAR
- Runtime: Apache Tomcat
- Backend style: Servlets + JSP
- Frontend style: JSP + jQuery + Foundation
- Main purpose: operational lookup of request/log information by ID and operational query to SIGRA

## Functional modules

### 1. Authentication and session

#### Overview

The user accesses the login page, authenticates against LDAP, and if authorized is redirected to the main menu.

The target platform should preserve the legacy business behavior through a JSON API consumed by Next.js, while replacing JSP redirects with explicit frontend navigation decisions.

#### Current components

- `index.jsp`
- `Login.java`
- `Logout.java`
- `SessionPing.java`

#### Current behavior

- Show login form with:
  - domain selector
  - username
  - password
- Submit authentication to `/login.do`
- Validate user authorization against the permitted users file
- Authenticate against LDAP
- On success:
  - create session
  - store `LOGGED_USERNAME`
  - set session inactivity timeout to 8 hours
  - update the session cookie max-age to 8 hours
  - redirect to `menu.jsp`
- On failure:
  - redirect to `index.jsp?authFailed=true`
- Allow logout through `/logout.do`
- Keep session alive periodically through `/doPing.do`

#### Inputs

- `ldomain`
- `lusername`
- `lpassword`

#### Legacy entry points

- `GET /index.jsp`
- `POST /login.do`
- `GET|POST /logout.do`
- `GET|POST /doPing.do`

#### Outputs

- Redirect to menu on success
- Redirect to login with error on failure

#### Functional rules

- Empty username or password must fail
- Unauthorized user must fail
- LDAP authentication must succeed before access is granted
- Session expiration behavior must be preserved functionally
- Successful login creates a server session attribute named `LOGGED_USERNAME`
- Session inactivity timeout is currently configured to 8 hours in backend logic
- Session cookie lifetime is also refreshed to 8 hours

#### Target API contract

The new backend should expose JSON endpoints under `/api/v1/auth` and keep server-side session behavior with an HttpOnly cookie.

##### `POST /api/v1/auth/login`

Purpose:

- authenticate against LDAP
- validate local authorization
- create authenticated session

Request body:

```json
{
  "domain": "ptportugal",
  "username": "jdoe",
  "password": "secret"
}
```

Success response `200`:

```json
{
  "authenticated": true,
  "user": {
    "username": "jdoe",
    "displayName": "jdoe",
    "domain": "ptportugal",
    "permissions": {
      "allowed": true,
      "roles": ["user"]
    }
  },
  "session": {
    "authenticated": true,
    "expiresInSeconds": 28800,
    "idleTimeoutSeconds": 28800,
    "keepAliveIntervalSeconds": 300
  },
  "redirectTo": "/app"
}
```

Validation failure `422`:

```json
{
  "authenticated": false,
  "error": {
    "code": "AUTH_VALIDATION_ERROR",
    "message": "Credenciais incompletas.",
    "fields": {
      "username": "required",
      "password": "required"
    }
  }
}
```

Invalid credentials `401`:

```json
{
  "authenticated": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Erro na autenticacao."
  }
}
```

Unauthorized user `403`:

```json
{
  "authenticated": false,
  "error": {
    "code": "AUTH_FORBIDDEN",
    "message": "Erro na autenticacao."
  }
}
```

Provider unavailable `503`:

```json
{
  "authenticated": false,
  "error": {
    "code": "AUTH_PROVIDER_UNAVAILABLE",
    "message": "Erro na autenticacao."
  }
}
```

Behavior notes:

- Public error messages should remain intentionally generic to preserve legacy semantics.
- The backend must set an HttpOnly session cookie on success.
- Session state must store the equivalent of `LOGGED_USERNAME`.

##### `GET /api/v1/auth/session`

Purpose:

- load authenticated session state
- bootstrap protected routes in Next.js

Success response `200`:

```json
{
  "authenticated": true,
  "user": {
    "username": "jdoe",
    "displayName": "jdoe",
    "domain": "ptportugal",
    "permissions": {
      "allowed": true,
      "roles": ["user"]
    }
  },
  "session": {
    "authenticated": true,
    "expiresInSeconds": 27480,
    "idleTimeoutSeconds": 28800,
    "keepAliveIntervalSeconds": 300,
    "lastActivityAt": "2026-03-18T10:15:00Z"
  }
}
```

Unauthenticated response `401`:

```json
{
  "authenticated": false,
  "error": {
    "code": "SESSION_NOT_AUTHENTICATED",
    "message": "Sessao expirada ou inexistente."
  }
}
```

##### `POST /api/v1/auth/keep-alive`

Purpose:

- renew the authenticated session inactivity window
- replace the legacy `doPing.do`

Request body:

```json
{}
```

Success response `200`:

```json
{
  "ok": true,
  "session": {
    "authenticated": true,
    "expiresInSeconds": 28800,
    "idleTimeoutSeconds": 28800,
    "keepAliveIntervalSeconds": 300,
    "refreshedAt": "2026-03-18T10:20:00Z"
  }
}
```

Expired session `401`:

```json
{
  "ok": false,
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "Sessao expirada ou inexistente."
  }
}
```

Behavior notes:

- The frontend should call this endpoint every 300 seconds while authenticated.
- Renewal should extend the inactivity timeout to the equivalent of 8 hours.

##### `DELETE /api/v1/auth/session`

Purpose:

- invalidate authenticated session
- remove browser-authenticated state

Success response `200`:

```json
{
  "ok": true,
  "loggedOut": true,
  "redirectTo": "/login"
}
```

Behavior notes:

- Logout should be idempotent.
- The backend should invalidate the server session and clear the session cookie.

##### `GET /api/v1/auth/config`

Purpose:

- provide login-screen configuration to Next.js

Success response `200`:

```json
{
  "domains": [
    { "value": "ptportugal", "label": "PTPORTUGAL", "default": true },
    { "value": "ptc", "label": "PTC", "default": false },
    { "value": "ptcom", "label": "PTCOM", "default": false },
    { "value": "ptin", "label": "PTIN", "default": false },
    { "value": "ptsi", "label": "PTSI", "default": false },
    { "value": "tmn", "label": "TMN", "default": false }
  ]
}
```

#### Frontend behavior contract

- `/login` should load domain options and submit credentials to `POST /api/v1/auth/login`
- protected pages should call `GET /api/v1/auth/session`
- `401` from protected auth endpoints should redirect to `/login?reason=session-expired`
- authenticated users should not see the login page as their primary destination
- logout should call `DELETE /api/v1/auth/session` and navigate to `/login`
- keep-alive should run every 5 minutes while the user is active in the authenticated shell

#### Session policy

- Session model: server-side session with secure cookie
- Business inactivity timeout: 28800 seconds
- Keep-alive interval: 300 seconds
- Cookie requirements:
  - `HttpOnly`
  - `Secure` in HTTPS environments
  - `SameSite=Lax`
  - `Path=/`
  - `Max-Age=28800`

#### Detailed logout behavior

- Logout is accessible through `/logout.do`
- Both `GET` and `POST` requests are accepted
- The current implementation:
  - sets no-cache headers
  - invalidates the current session
  - attempts to remove the cookie matching the current session id
  - always redirects to `index.jsp`

#### Detailed session keep-alive behavior

- The main page triggers AJAX requests to `/doPing.do?ping=<timestamp>`
- Calls are sent every 300000 ms, which is 5 minutes
- The backend does not return meaningful business payload
- The current keep-alive implementation:
  - searches request cookies for the one matching the current session id
  - rewrites that cookie with the same session id
  - sets cookie max-age to 8 hours
- The keep-alive path appears focused on cookie renewal rather than business response content

### 2. Main navigation

#### Overview

After login, the user lands on the main page and can navigate between operational modules.

#### Current components

- `menu.jsp`

#### Current behavior

- Show top bar with application title and logged user
- Show logout action
- Show off-canvas menu
- Allow navigation to:
  - Audit Logs
  - Pedidos a SIGRA
- Load module content dynamically into the page

#### Functional rules

- User must be authenticated to access the page
- Unauthenticated access must redirect to login

### 3. Audit Logs module

#### Overview

This module lets the user query operational information by environment, ID type, request ID and SAPA ID.

#### Current components

- `netqLogs.jsp`
- `app.js`
- `URLRequest.java`

#### Current behavior

- Show environment selector
- Show ID type selector
- Show request ID input
- Show SAPA ID input
- Trigger lookup by request ID
- Trigger lookup by SAPA ID
- Display response content dynamically
- For some request types, display syntax-highlighted payload content
- For NetQ flows, display related records in left and right panels
- The servlet delegates business behavior to `GetXmlpage.requestManagement(id, req, tid, chld)`
- The frontend clears the previous response before each request
- The frontend clears both ID fields after a successful response
- The frontend shows a SweetAlert loading state before each request
- The frontend uses synchronous AJAX calls with a 5000 ms timeout

#### Inputs

- `amb`
  - `prodMongo`
  - `qaMongo`
- `tipoid`
  - `NETQ`
  - `TIBCO`
  - `NETWIN`
  - `SIGRA`
  - `NA`
- `submitID`
- `sapaID`

#### Legacy request parameters sent to `URLRequest`

- `id`
- `req`
- `tid`
- `chld`
- `div`

#### Request targets

- `URLRequest`

#### Outputs

- For `SAPA`:
  - heading with queried id
  - one formatted payload block
- For non-`NETQ` external systems:
  - heading with queried id and target system
  - one formatted payload block
- For top-level `NETQ`:
  - left collapse button
  - right collapse button
  - two accordion columns
  - hidden input carrying `req`
- For child `NETQ` detail:
  - one formatted payload block injected into the chosen accordion panel

#### Functional rules

- Request lookup must support different behaviors based on environment and ID type
- SAPA lookup must be treated as a separate query flow
- Successful results must be rendered immediately in the UI
- Empty or invalid results must still preserve the current user journey
- The legacy frontend does not define an explicit AJAX error callback for timeout or transport failure
- Highlighting is re-applied after successful payload rendering
- `NETQ` rendering depends on backend-produced HTML structure, not just data

#### Behavior by `req`

##### `req = prodMongo`

- If `tid = NETQ`:
  - call production audit endpoint using `auditProd + id + auxURLaudit`
  - call production mongo endpoint using `mongoProd + id + auxURL`
  - build a combined result from both calls
  - if `chld = 0`, recursively discover related order ids from mongo response
  - for each related id, repeat the same pair of calls and append to response
  - return a flattened 4-field sequence per record:
    - order id
    - order type
    - audit payload
    - mongo payload
- If `tid != NETQ`:
  - call production audit endpoint using `auditProd + tid + "/" + id`
  - return a single payload response

##### `req = qaMongo`

- If `tid = NETQ`:
  - call QA audit endpoint using `auditQA + id + auxURLaudit`
  - call QA mongo endpoint using `mongoQA + id + auxURL`
  - build a combined result from both calls
  - if `chld = 0`, recursively discover related order ids from mongo response
  - for each related id, repeat the same pair of calls and append to response
  - return a flattened 4-field sequence per record:
    - order id
    - order type
    - audit payload
    - mongo payload
- If `tid != NETQ`:
  - call QA audit endpoint using `auditQA + tid + "/" + id.replace("#", "%23")`
  - return a single payload response

##### `req = sapa`

- ignore `tid` for routing purposes
- call SAPA endpoint using `sapaUrl + id`
- return a single payload response

#### Behavior by `tid`

##### `tid = NETQ`

- This is the most complex flow
- The system combines:
  - audit payload
  - mongo payload
  - derived order type
  - related child order ids
- The mongo response is parsed to extract:
  - `orderType`
  - child order ids from repeated `<order><id>...`
- The system avoids re-adding the original id when parsing related ids
- If `chld = 0`, the top-level response includes all discovered related ids recursively
- If `chld != 0`, the response is used only to fill a single expanded detail panel
- Related ids are extracted by regex from `<order><id>...</id>`
- `orderType` is extracted by regex and falls back to `COCO` when not found
- Recursive discovery prepends newly found child ids, creating a depth-biased traversal order

##### `tid != NETQ`

- Covers external systems such as:
  - `TIBCO`
  - `NETWIN`
  - `SIGRA`
  - `NA`
- The system performs a single audit call
- No recursive related-order expansion exists for these flows
- The UI displays one formatted payload only

#### Behavior by `chld`

##### `chld = 0`

- Used for main searches from submit buttons
- `NETQ` builds the two-panel accordion UI
- `SAPA` and non-`NETQ` flows return a single formatted payload view

##### `chld = 1`

- Used only for lazy-loaded `NETQ` detail expansion
- Requires `div = left` or `div = right`
- Backend returns a 3-item list:
  - order id
  - audit payload
  - mongo payload
- Left panel uses mongo payload
- Right panel uses audit payload

#### Dependencies

- `netqLogs.jsp`
- `app.js`
- `URLRequest.java`
- `GetXmlpage.java`
- configured HTTP endpoints from `app.json`
- jQuery
- SweetAlert2
- Highlight.js

#### Known legacy error and ambiguity points

- `URLRequest` returns `text/html` rather than structured error payloads
- Upstream non-2xx HTTP responses throw exceptions in the backend
- XML formatting assumes parseable XML and may fail for malformed or non-XML payloads
- The frontend timeout/error experience is undefined because there is no AJAX error callback
- Missing request parameters are not validated before branching
- Top-level `NETQ` semantics depend on positional list ordering rather than named fields

#### Current response shape from `GetXmlpage.requestManagement`

##### For `NETQ` top-level query with `chld = 0`

The result is a flat list grouped in blocks of 4:

1. order id
2. order type
3. audit payload
4. mongo payload

Additional related ids are appended as extra 4-item groups in the same order.

##### For `NETQ` child detail query with `chld != 0`

The result is a flat list with:

1. order id
2. audit payload
3. mongo payload

The UI then decides:

- left panel uses item `3` from the list
- right panel uses item `2` from the list

##### For non-`NETQ` query

The result is:

1. queried id
2. formatted payload

##### For `SAPA` query

The result is:

1. queried id
2. formatted payload

### 4. Related records and detail expansion

#### Overview

For the NetQ flow, the system supports dynamic expansion of related records on left and right sections.

#### Current components

- `app.js`
- `URLRequest.java`

#### Current behavior

- Main query returns grouped result structure
- UI renders accordions
- Clicking an accordion item triggers a child request
- Left side displays one kind of detail
- Right side displays another kind of related information
- Buttons allow collapsing left and right panels

#### Exact current semantics

- For the top-level `NETQ` search:
  - each accordion row is backed by a 4-item block
  - left accordion title uses `id + orderType`
  - right accordion title uses the same `id + orderType`
- When the operator clicks the left accordion item:
  - frontend sends `div=left`
  - backend returns the mongo payload from list position `3`
- When the operator clicks the right accordion item:
  - frontend sends `div=right`
  - backend returns the audit payload from list position `2`
- This means:
  - left side is "Registo do pedido"
  - right side is "Pedidos a sistemas externos relacionado"
- The naming in the current code is easy to misunderstand, so this mapping must be preserved carefully

#### Functional rules

- Child requests are lazy loaded
- Left/right behavior must remain understandable and equivalent in the new UI
- The distinction between left and right payload content must be preserved

### 5. SIGRA module

#### Overview

This module validates an area code and performs a SOAP request to SIGRA/TIBCO.

#### Current components

- `sigra.jsp`
- `app.js`
- `URLRequestSigra.java`

#### Current behavior

- Show input for area central
- Validate format before request
- Accepted format: `00XX00`
- Submit query to `URLRequestSigra`
- Display:
  - outgoing request payload
  - TIBCO response payload
- Enforce `maxlength="6"` in the input field
- Clear the AC field after a successful response
- Show SweetAlert loading state before sending the request
- Use synchronous AJAX with a 5000 ms timeout

#### Inputs

- `submitAC`
- request parameter `ac`

#### Outputs

- heading `Pedido SIGRA com AC = <ac>`
- formatted SOAP request payload
- heading `Resposta TIBCO`
- formatted SOAP response payload

#### Functional rules

- The AC must match the current validation rule before submission
- Validation error must be visible to the user
- Request and response payloads must be viewable in a readable way
- Invalid AC shows `A area central terá que ter o formato "00XX00"`
- Lowercase letters do not pass client validation
- The backend assumes the request already passed frontend validation

#### Backend SOAP construction rules

- `SOAPAction` header comes from configuration
- Header contains:
  - `npu`
  - `creationTime`
  - `timeout`
  - credentials with `systemCode`
- Body contains:
  - operation timestamp
  - `Accao = 2`
  - `AreaCentral = <ac>`
  - `Aplicacao = <configured app>`
- Both request and response are formatted and HTML-escaped before rendering

#### Dependencies

- `sigra.jsp`
- `app.js`
- `URLRequestSigra.java`
- `CallSigraAC.java`
- SOAP endpoint and headers from `app.json`
- jQuery
- SweetAlert2
- Highlight.js

#### Known legacy error and ambiguity points

- No explicit AJAX error callback is defined for timeout or request failure
- `CallSigraAC` catches broad exceptions and prints stack traces instead of returning a stable error contract
- Request/response formatting assumes valid XML payloads
- `createTime()` uses `new Date(System.nanoTime())`, which is unusual and may produce unexpected timestamps
- `URLRequestSigra` reads `div` from the request but does not use it

## Cross-cutting behavior

### Session behavior

- Session is required for protected pages
- Session keep-alive exists in the current system
- Session timeout and user experience on expiration must be defined explicitly in the new system
- The legacy system sets session inactivity to 8 hours at login time
- The legacy UI sends a keep-alive ping every 5 minutes from the menu page
- Session protection in JSP currently relies on checking `LOGGED_USERNAME` in session

### Error behavior

- Login failure results in redirect with query parameter
- External integration failures may currently appear as empty, timed-out or partial UI responses
- These behaviors must be documented case by case during discovery

### Response rendering

- The current backend sometimes returns HTML fragments
- The new system should replace this with explicit JSON contracts
- Visual behavior must remain functionally equivalent

## Open questions for discovery

- Exact output structure returned by `GetXmlpage`
- Exact SOAP envelope contract and error cases for SIGRA
- Full permission model based on `usrPerm`
- Confirm which cookie name is used in each runtime environment
- Confirm what the user sees when the session expires during an active screen
- Confirm whether duplicate related ids can occur in recursive traversal
- Confirm expected behavior when audit call succeeds and mongo call fails, or vice versa
