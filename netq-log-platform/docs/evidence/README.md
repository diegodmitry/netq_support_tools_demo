# Legacy Evidence Index

## Purpose

This directory tracks captured legacy evidence used to protect functional parity during the migration.

## Screenshot location

Legacy screenshots are stored in the repository root under:

- `screenshots/`

## Current screenshot inventory

| Flow | Evidence | Status | Notes |
|---|---|---|---|
| Login screen | `screenshots/login.png` | Captured | Initial login view |
| Login screen variant | `screenshots/login1.png` | Captured | Alternate login capture |
| Post-login shell | `screenshots/after_login.png` | Captured | Main authenticated state |
| Side menu | `screenshots/side_menu.png` | Captured | Navigation menu evidence |
| Audit Logs loaded | `screenshots/after_click_Audit_Logs.png` | Captured | Module opened from menu |
| Audit Logs full screen | `screenshots/full_screen_Audit_Logs.png` | Captured | Broader Audit Logs layout |
| SIGRA loaded | `screenshots/after_click_Pedidos_a_SIGRA.png` | Captured | Module opened from menu |

## Remaining evidence to capture

- request/response samples for authentication and session
- request/response samples for Audit Logs:
  - `NETQ`
  - external ID
  - `SAPA`
  - related detail left/right
- request/response samples for SIGRA
- user-visible error messages and timeout behavior
- session-expired behavior evidence

## Suggested next additions

- `auth-session/requests/`
- `auth-session/responses/`
- `audit-logs/requests/`
- `audit-logs/responses/`
- `sigra/requests/`
- `sigra/responses/`
- `messages/`

## Directory structure created

- `auth-session/requests/`
- `auth-session/responses/`
- `audit-logs/requests/`
- `audit-logs/responses/`
- `sigra/requests/`
- `sigra/responses/`
- `messages/`

## Template files created

- `auth-session/requests/login-valid.md`
- `auth-session/requests/login-invalid.md`
- `auth-session/requests/logout.md`
- `auth-session/responses/login-valid.md`
- `auth-session/responses/login-invalid.md`
- `auth-session/responses/logout.md`
- `auth-session/responses/session-expired.md`
- `audit-logs/requests/netq-main.md`
- `audit-logs/requests/module-load.md`
- `audit-logs/requests/external-id.md`
- `audit-logs/requests/sapa.md`
- `audit-logs/requests/related-detail-left.md`
- `audit-logs/requests/related-detail-right.md`
- `audit-logs/responses/module-load.md`
- `audit-logs/responses/netq-main.md`
- `audit-logs/responses/external-id.md`
- `audit-logs/responses/sapa.md`
- `audit-logs/responses/related-detail-left.md`
- `audit-logs/responses/related-detail-right.md`
- `sigra/requests/valid-ac.md`
- `sigra/responses/valid-ac.md`
- `sigra/responses/invalid-ac.md`
- `messages/authentication-error.md`
- `messages/sigra-invalid-ac.md`

## Capture template

For each captured case, prefer one markdown file with:

- case name
- date/time
- source screen or action
- request parameters or payload
- response body or rendered message
- expected legacy behavior
- linked screenshot file, when available
