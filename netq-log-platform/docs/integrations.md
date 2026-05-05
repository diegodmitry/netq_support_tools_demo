# Integrations Catalog

## Purpose

This document catalogs all external dependencies and integration points that the new system must preserve or replace safely.

## Integration inventory

### 1. LDAP / Active Directory

#### Purpose

Authenticate users during login.

#### Legacy usage

- Implemented in `Login.java`
- Uses UnboundID LDAP SDK

#### Current behavior

- Uses configured LDAP server, port, service account DN and password
- Binds using selected domain plus username and submitted password
- Grants access only when user is both:
  - present in allowed users list
  - successfully authenticated in LDAP

#### Data points already identified

- `ldap_server`
- `ldap_port`
- `ldap_user_dn`
- `ldap_user_db_password`

#### Migration notes

- Wrap LDAP logic in dedicated authentication adapter
- Avoid exposing LDAP implementation to route handlers
- Use secrets for service account credentials
- Provide mockable interface for tests

#### Risks

- Corporate network dependency
- Certificate or SSL behavior differences
- Hard-to-test failure conditions

### 2. Allowed users file

#### Purpose

Restrict application access to a known list of permitted users.

#### Legacy usage

- Loaded from `catalina.base/conf/NetQTools/usrPerm`

#### Migration notes

- Decide whether this remains:
  - a file
  - a ConfigMap
  - a database table
  - an external identity/authorization source

#### Risks

- File not versioned with application logic
- Drift between environments

### 2.1 Session and browser interaction

#### Purpose

Preserve authenticated browser session behavior during normal operation.

#### Legacy usage

- Login sets session timeout and updates cookie max-age to 8 hours
- Menu page calls `/doPing.do?ping=<timestamp>` every 5 minutes
- SessionPing refreshes the cookie max-age for the cookie matching current session id
- Logout invalidates session and removes the matching session cookie

#### Migration notes

- Decide early between:
  - secure server-side session cookie
  - token-based auth with refresh strategy
- Preferred target for parity: secure server-side session cookie
- Preserve the business expectation that active users should not be logged out unexpectedly during normal use
- Define explicit frontend behavior for expired session during active module usage
- Preserve the 8-hour inactivity window and 5-minute keep-alive cadence unless explicitly approved otherwise

#### Risks

- Different browser cookie behavior in the new stack
- Session renewal semantics may differ from servlet container behavior
- Silent session expiry could change operator experience

#### Target contract notes

- FastAPI should issue a secure HttpOnly cookie for the authenticated session
- Next.js should treat auth state as server-backed session state, not as client-owned credentials
- Auth/session endpoints should be exposed under `/api/v1/auth`
- End-user error messages should remain generic for invalid credentials and forbidden users

### 3. Audit-related HTTP endpoints

#### Purpose

Query operational data used in Audit Logs flow.

#### Config keys identified

- `mongoProd`
- `mongoProdBasicAuth`
- `mongoProdBasicAuthUser`
- `mongoProdBasicAuthPass`
- `auditProd`
- `auditProdBasicAuth`
- `auditProdBasicAuthUser`
- `auditProdBasicAuthPass`
- `mongoQA`
- `auditQA`
- `auxURL`
- `auxURLaudit`

#### Legacy usage

- Used by logic behind `URLRequest.java`
- Exact downstream call patterns still need detailed discovery

#### Migration notes

- Create dedicated API clients per integration type
- Define timeout, retry and error mapping strategy
- Capture sample requests and responses from legacy
- Move all credentials to secrets
- Preserve routing rules by environment and `tid`
- Preserve current dual-call behavior for `NETQ`:
  - one audit call
  - one mongo call
- Preserve current single-call behavior for non-`NETQ`

#### Risks

- Hidden differences between PROD and QA behavior
- Basic auth inconsistency per endpoint
- Non-obvious response formatting rules
- Recursive related-id expansion may create hidden edge cases
- Audit and mongo payloads are semantically assigned to different UI panels

### 4. SAPA HTTP integration

#### Purpose

Lookup data based on SAPA ID.

#### Config key identified

- `sapaUrl`

#### Legacy usage

- Accessed through Audit Logs UI path

#### Migration notes

- Treat as separate use case inside the Audit Logs module
- Document payload expectations and error conditions
- Preserve the current dedicated route behavior driven by `req=sapa`

### 5. SIGRA / TIBCO SOAP integration

#### Purpose

Perform operational request by AC and show request/response payloads.

#### Config keys identified

- `sigraApp`
- `sigraCodeApp`
- `sigraUrl`
- `sigraAction`
- `sigraTimeout`

#### Legacy usage

- Implemented behind `URLRequestSigra.java`
- SOAP logic delegated to `CallSigraAC`

#### Migration notes

- Capture real SOAP envelopes and namespace requirements
- Define timeout and retry policy carefully
- Preserve operator-facing visibility of request and response

#### Risks

- SOAP namespace sensitivity
- Timeout behavior differences
- Upstream instability or undocumented fault responses

### 6. Configuration files

#### Purpose

Provide environment-specific values for endpoints, auth and logging.

#### Legacy usage

- `app.json`
- `app_DEV.json`
- `app_PRD.json`
- `log4j.xml`

#### Migration notes

- Replace with:
  - environment variables
  - Kubernetes ConfigMaps
  - Kubernetes Secrets
- Keep a configuration matrix per environment

#### Risks

- Divergence between current files and real deployed values
- Sensitive data already present in repository history

### 7. Logging

#### Purpose

Record operational events and application behavior.

#### Legacy usage

- Uses Log4j configuration from external path

#### Migration notes

- Use structured logs in JSON where possible
- Include request correlation id
- Define operational fields for traceability

## Environment mapping checklist

- [ ] DEV configuration identified
- [ ] PRD configuration identified
- [ ] Effective runtime values confirmed
- [ ] Secret values removed from code and files
- [ ] ConfigMap/Secret target model approved

## Discovery checklist per integration

- [ ] Endpoint or host identified
- [ ] Authentication method identified
- [ ] Request format identified
- [ ] Response format identified
- [ ] Timeout behavior identified
- [ ] Retry behavior identified
- [ ] Error cases identified
- [ ] Test strategy defined
