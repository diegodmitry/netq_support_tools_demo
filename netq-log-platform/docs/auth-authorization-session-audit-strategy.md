# Authentication, Authorization, Session and Audit Strategy

## Purpose

This document defines the target strategy for authentication, authorization, session handling and security auditing in `netq-log-platform`.

It is based on:

- the legacy Java/JSP implementation in `NetQTools`
- the captured evidence in `docs/evidence/auth-session`
- the current FastAPI and Next.js scaffolding already present in this repository

The goal is to decide the production approach early, reduce parity risk, and guide the next implementation tasks.

## Legacy behavior that must be preserved

### Authentication

- Login requires:
  - `domain`
  - `username`
  - `password`
- Access is granted only when both conditions are true:
  - the username exists in the allowed-user source
  - LDAP bind succeeds for the submitted credentials
- Public failure semantics are intentionally generic:
  - invalid credentials and unauthorized user both appear as authentication failure to the operator

### Session

- Successful login creates a server-side session
- Session stores `LOGGED_USERNAME`
- Session inactivity timeout is `28800` seconds
- The session cookie lifetime is also refreshed to `28800` seconds
- The browser sends a keep-alive request every `300` seconds
- Logout invalidates the session, clears the cookie and returns the user to login

### Access control

- Protected pages check session existence before rendering
- Unauthenticated access is redirected to login

## Decisions

### 1. Authentication model

The target model is:

- LDAP authentication through a dedicated backend adapter
- local authorization check before granting application access
- server-managed authenticated session after successful login

Why this is the chosen model:

- it preserves the exact legacy business rule
- it avoids exposing LDAP details to the browser
- it fits the current FastAPI contract already documented under `/api/v1/auth`
- it avoids the complexity and extra risk of issuing browser-owned bearer tokens for an internal operational tool

### 2. Authorization model

Authorization will be split into two layers.

#### Layer A: application access

This is the legacy rule and remains mandatory:

- user must be present in the allowed-user source
- user must authenticate successfully in LDAP

Initial source of truth:

- a file or mounted secret/config resource managed outside the image

Target operational form:

- Kubernetes-mounted file or equivalent external configuration

Rationale:

- it keeps parity with `usrPerm`
- it is simpler and lower-risk than introducing a new database table now
- it can later be replaced by a central IAM or RBAC source without breaking the API contract

#### Layer B: application roles

The new platform should introduce explicit roles in session state even if phase 1 uses only a minimal set.

Initial roles:

- `user`: can access operational modules already available in the legacy tool
- `admin`: reserved for future operational and support capabilities

Rules for now:

- every allowed authenticated user receives `user`
- `admin` is optional and can come from a separate configured list

Why now:

- it keeps the API honest about authorization
- it prevents role retrofitting later
- it prepares the platform for admin-only diagnostics or configuration screens

### 3. Session model

The chosen production session strategy is:

- opaque server-side session id in a secure `HttpOnly` cookie
- session state owned by the backend
- browser treated only as session holder, never as source of truth

This means:

- no JWT access token in browser storage
- no refresh-token flow for phase 1
- no client-side authorization state as the primary gate

Why this is preferred:

- closest parity with `JSESSIONID`
- lower XSS exposure than local/session storage tokens
- simpler invalidation semantics for logout and forced expiry
- cleaner fit for server actions and middleware in Next.js

## Target session contract

### Cookie policy

The backend session cookie must be:

- `HttpOnly`
- `Secure` in non-local environments
- `SameSite=Lax`
- `Path=/`
- max-age aligned with the inactivity window

Cookie name:

- keep `netq_session` in the new platform

### Session contents on the backend

Each active session should contain at least:

- `session_id`
- `username`
- `domain`
- `roles`
- `authenticated_at`
- `last_activity_at`
- `expires_at`
- `source_ip_hash` or request fingerprint when approved
- `user_agent_hash` when approved
- correlation metadata for auditing

Parity field:

- keep an equivalent logical field for `LOGGED_USERNAME`

### Timeout policy

The approved phase 1 policy is:

- inactivity timeout: `8` hours
- keep-alive cadence: `5` minutes while the user is active in the protected shell

Clarification:

- this is an inactivity timeout, not a hard maximum absolute lifetime
- keep-alive renews the inactivity window

## Session storage decision

### Development

- in-memory session store is acceptable only for local development and tests

### Production

Use a shared external session store, preferably Redis.

Why Redis:

- works across multiple backend pods
- avoids session loss on pod restart
- supports TTL naturally
- keeps logout and expiry behavior deterministic in Kubernetes

Explicit non-goal:

- do not rely on per-process memory for production sessions

## Frontend strategy

### Route protection

Protected routes must be enforced in two places:

- lightweight middleware gate by cookie presence for fast redirect behavior
- authoritative server-side bootstrap using `/api/v1/auth/session`

Important rule:

- cookie presence alone is never sufficient to trust authentication

### Login flow

The browser submits credentials to the Next.js login action, which calls the backend auth API.

Production rule:

- Next.js must forward the backend `Set-Cookie` semantics cleanly
- the frontend must not invent or own session contents

Current scaffold gap to close:

- the frontend currently extracts the session token and sets its own cookie manually

Target adjustment:

- centralize cookie issuance semantics so backend and frontend do not diverge on flags, TTL or rotation behavior

### Keep-alive behavior

Keep-alive remains explicit because it is part of the legacy operator experience.

Approved behavior:

- protected shell sends keep-alive every `300` seconds
- backend refreshes `last_activity_at` and cookie TTL
- `401` from keep-alive redirects to login with recoverable session-expired state

### Logout behavior

Logout must:

- invalidate the backend session
- clear the browser cookie
- return the user to `/login`
- be idempotent from the user perspective

## LDAP strategy

LDAP integration will live behind a dedicated adapter interface.

Required responsibilities:

- bind using configured LDAP host, port and service account when needed
- authenticate using selected domain plus username and submitted password
- map provider failures to generic operator-facing errors
- expose internal failure reason only to logs

Operational rules:

- LDAP credentials and connection settings must come from secrets
- TLS verification behavior must be explicit and environment-specific
- trust-all SSL behavior from the legacy code must not be copied to production by default

## Authorization source strategy

Phase 1 approved source:

- mounted allowed-users file managed per environment

Implementation direction:

- load at startup and support reload by restart
- fail closed when the authorization source is unavailable or malformed
- normalize usernames consistently before lookup

Future-ready extension:

- abstract the source behind an authorization repository so a database or IAM group lookup can replace the file later

## Audit strategy

This section refers to security and operational auditing, not the business "Audit Logs" lookup module.

### What must be audited

Record structured audit events for:

- login attempt started
- login succeeded
- login failed due to invalid credentials
- login denied due to authorization policy
- login failed due to provider error
- session loaded
- session keep-alive renewed
- session expired
- logout requested
- logout completed
- access denied to protected resource

### Mandatory audit fields

Every auth audit event should include:

- `event_name`
- `event_time`
- `result`
- `username_submitted` when available
- `username_effective` when authenticated
- `domain`
- `session_id` or a non-sensitive session identifier
- request correlation id
- route or action name
- client ip in approved/anonymized form
- user agent in approved/truncated or hashed form

### Logging rules

- logs must be structured JSON
- credentials must never be logged
- raw LDAP errors must not be exposed in end-user responses
- sensitive identifiers should be masked or hashed when not required in clear text

### Retention and operations

Recommended baseline:

- auth audit logs shipped to centralized logging
- retention defined by operations and compliance requirements
- alerts added for repeated authentication failures and provider unavailability

## Recommended backend shape

Suggested responsibilities:

- `AuthService`: orchestrates login, session, keep-alive and logout use cases
- `LdapAuthGateway`: authenticates against LDAP
- `AllowedUserRepository`: resolves whether a user is authorized
- `SessionRepository`: persists and renews server-side sessions
- `AuditLogger`: emits structured security audit events

This keeps authentication, authorization, session persistence and auditing independently testable.

## Recommended rollout order

1. Replace `InMemoryAuthGateway` with split adapters for LDAP, allowed users and session repository.
2. Introduce Redis-backed session persistence.
3. Add structured auth audit logging with correlation ids.
4. Remove frontend-owned cookie duplication and align cookie handling with backend policy.
5. Add role-aware authorization helpers for future module restrictions.
6. Validate all auth/session acceptance criteria against captured legacy evidence.

## Explicit non-decisions

The following are intentionally out of scope for this phase:

- SSO migration
- OAuth2 or OpenID Connect browser flows
- MFA changes
- replacing LDAP as corporate identity provider
- fine-grained per-screen RBAC beyond the initial role model

## Summary of approved strategy

- Authentication: LDAP via backend adapter plus local allowed-user check
- Authorization: external allowed-user source now, explicit roles in session from day one
- Session: opaque server-side cookie session, Redis-backed in production
- Keep-alive: keep the 5-minute active-session renewal behavior
- Audit: structured security audit events for login, session and access-control lifecycle
