# Frontend

Minimal Next.js auth shell for the migration.

## Scope implemented

- `/login` page wired to the FastAPI auth contract
- `/app` protected route guarded by middleware
- logout action returning the user to `/login`
- keep-alive route and client loop for authenticated shell
- shared auth client for:
  - `/auth/config`
  - `/auth/login`
  - `/auth/session`
  - `/auth/keep-alive`
  - `/auth/session` logout

## Notes

- The middleware currently guards access by the presence of the session cookie.
- The frontend mirrors the backend session token into a browser cookie and forwards it on server-side requests.

## Local Mock Mode

Use the existing environment flags to test the frontend without a real login and with a mocked `NETQ` flow:

- `NETQ_SKIP_AUTH=true`
  - bypasses login and redirects `/login` straight to `/app`
  - uses a local authenticated session shape in the frontend
- `NETQ_USE_MOCKS=true`
  - returns fixture data only for `NETQ` queries
  - does not mock `SAPA`, `NA`, `SIGRA`, `NETWIN` or `TIBCO`

Example:

```bash
NETQ_SKIP_AUTH=true NETQ_USE_MOCKS=true npm run dev
```

Expected behavior in this mode:

- `/app` opens without real authentication
- `NETQ` queries use local mock data
- non-`NETQ` queries still call the configured backend

## Quality workflow

- Install dependencies with `npm install`
- Run lint with `npm run lint`
- Run formatting check with `npm run format:check`
- Run type checks with `npm run typecheck`
- Run tests with `npm run test`
