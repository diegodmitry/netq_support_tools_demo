# Backend

Minimal FastAPI foundation for the authentication and session module.

## Scope implemented

- versioned API under `/api/v1`
- auth contract routes:
  - `POST /api/v1/auth/login`
  - `GET /api/v1/auth/session`
  - `POST /api/v1/auth/keep-alive`
  - `DELETE /api/v1/auth/session`
  - `GET /api/v1/auth/config`
- health endpoints:
  - `/health`
  - `/ready`
- layered structure:
  - `domain`
  - `application`
  - `infrastructure`
  - `api`

## Notes

- LDAP is currently represented by an in-memory mock gateway.
- Session persistence is currently in-memory and intended only as a scaffold.
- Configuration is loaded through environment variables via `app.core.config.Settings`.
- A safe starting template is available at `backend/.env.example`.
- Sensitive values should be provided through mounted secret files referenced by env vars such as `NETQ_LDAP_USER_DB_PASSWORD_FILE`.

## Quality workflow

- Install dev dependencies with `python -m pip install -e .[dev]`
- Run lint with `ruff check .`
- Run format check with `ruff format --check .`
- Run tests with `pytest`
