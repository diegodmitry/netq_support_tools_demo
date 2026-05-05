# Acceptance Criteria

## Purpose

This document defines the minimum acceptance criteria required to approve `netq-log-platform` as functionally equivalent and operationally ready.

## Global acceptance criteria

- [ ] All critical legacy flows are documented
- [ ] All critical legacy flows have target acceptance criteria
- [ ] All migrated modules have automated test coverage
- [ ] No critical credential remains hardcoded in source-controlled application code
- [ ] Backend and frontend images build successfully
- [ ] Application runs locally through containers
- [ ] Application runs in Kubernetes test environment
- [ ] Observability and health checks are operational

## Module acceptance criteria

### 1. Authentication and session

- [ ] User can access login screen
- [ ] User can choose domain
- [ ] User can submit username and password
- [ ] Empty credentials are rejected
- [ ] Invalid credentials are rejected
- [ ] Unauthorized users are rejected
- [ ] Valid authorized users can log in
- [ ] Successful login establishes authenticated state with approved timeout policy
- [ ] Authenticated user can access protected pages
- [ ] Non-authenticated user is redirected or blocked appropriately
- [ ] User can log out successfully
- [ ] Logout clears authenticated browser state
- [ ] Session expiration behavior is defined and approved
- [ ] Session keep-alive or equivalent behavior is defined and approved
- [ ] Active user is not logged out unexpectedly during normal operation

#### Authentication API acceptance criteria

- [ ] `POST /api/v1/auth/login` accepts `domain`, `username` and `password` as JSON
- [ ] `POST /api/v1/auth/login` returns `200` with authenticated user and session metadata for valid authorized users
- [ ] `POST /api/v1/auth/login` returns `422` for missing required credentials
- [ ] `POST /api/v1/auth/login` returns `401` for invalid LDAP credentials
- [ ] `POST /api/v1/auth/login` returns `403` for users outside the allowed-user source
- [ ] Login failures do not expose sensitive LDAP or authorization internals in end-user messages
- [ ] Successful login creates a secure server-side session and equivalent of `LOGGED_USERNAME`
- [ ] Session timeout metadata reflects 8 hours of inactivity

#### Session API acceptance criteria

- [ ] `GET /api/v1/auth/session` returns `200` for authenticated sessions
- [ ] `GET /api/v1/auth/session` returns `401` when session is missing or expired
- [ ] `POST /api/v1/auth/keep-alive` renews the inactivity window for authenticated users
- [ ] `POST /api/v1/auth/keep-alive` returns `401` for expired sessions
- [ ] `DELETE /api/v1/auth/session` invalidates the session and clears the session cookie
- [ ] `DELETE /api/v1/auth/session` is idempotent from the user perspective
- [ ] `GET /api/v1/auth/config` returns the supported login domain list

#### Frontend acceptance criteria for auth/session

- [ ] Next.js login screen uses the backend-provided domain list or an approved equivalent source
- [ ] Protected routes use session bootstrap before rendering authenticated content
- [ ] Authenticated users are redirected away from the login screen
- [ ] Unauthenticated users are redirected to login when accessing protected routes
- [ ] Session expiration produces an explicit and recoverable login flow
- [ ] Keep-alive runs every 5 minutes or an approved equivalent cadence
- [ ] Logout navigates the user back to login

### 2. Main navigation

- [ ] Authenticated user sees main application shell
- [ ] Logged user identity is visible
- [ ] User can navigate to Audit Logs
- [ ] User can navigate to SIGRA
- [ ] Logout remains accessible from main navigation

### 3. Audit Logs

- [ ] User can select environment
- [ ] User can select ID type
- [ ] User can submit request ID
- [ ] User can submit SAPA ID
- [ ] Query results are returned and displayed correctly
- [ ] `NETQ` top-level query returns grouped records with id, order type, audit payload and mongo payload
- [ ] Related child records are discovered and displayed correctly
- [ ] Non-`NETQ` query returns the expected single external payload
- [ ] Empty results are handled acceptably
- [ ] External errors are handled acceptably
- [ ] Large payloads remain readable

### 4. Related records behavior

- [ ] NetQ result can show related records
- [ ] Related details are loaded on demand
- [ ] Left-side detail content matches mongo payload behavior
- [ ] Right-side detail content matches audit payload behavior
- [ ] Expand/collapse behavior is approved

### 5. SIGRA

- [ ] User can enter AC
- [ ] Invalid AC format is rejected before request
- [ ] Valid AC triggers backend request
- [ ] Request payload is viewable
- [ ] Response payload is viewable
- [ ] SOAP success path works
- [ ] SOAP error path is handled
- [ ] SOAP timeout path is handled

## Technical acceptance criteria

### Backend

- [ ] FastAPI project follows agreed architecture
- [ ] Domain and infrastructure are separated
- [ ] External integrations are isolated behind adapters
- [ ] Health and readiness endpoints exist
- [ ] Structured logging exists
- [ ] Metrics exist

### Frontend

- [ ] Next.js project follows agreed modular structure
- [ ] Protected routes are implemented
- [ ] UI follows the Vercel-inspired design direction
- [ ] UI remains operationally clear
- [ ] Loading, empty and error states are implemented consistently

### Containers and Kubernetes

- [ ] Backend container image builds
- [ ] Frontend container image builds
- [ ] Kubernetes manifests or chart are complete
- [ ] Readiness probes work
- [ ] Liveness probes work
- [ ] ConfigMaps and Secrets are externalized
- [ ] Rollout strategy is validated in test environment

## Exit criteria for go-live

- [ ] UAT approved
- [ ] Critical parity gaps resolved
- [ ] No blocker in authentication flow
- [ ] No blocker in Audit Logs flow
- [ ] No blocker in SIGRA flow
- [ ] Docker images versioned and published
- [ ] Kubernetes deployment validated
- [ ] Rollback strategy documented
