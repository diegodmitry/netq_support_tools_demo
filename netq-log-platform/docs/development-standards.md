# Development Standards

## Purpose

This document defines the baseline engineering conventions for `netq-log-platform`.

The goal is to keep the migration moving with predictable code quality across FastAPI and Next.js.

## Naming conventions

### Python

- Use `snake_case` for modules, functions and variables
- Use `PascalCase` for classes and Pydantic models
- Prefer names that describe responsibility precisely
- Use `*Gateway` for external/auth integration boundaries
- Use `*Service` for application-layer orchestration

### TypeScript

- Use `kebab-case` for file names
- Use `PascalCase` for React components and exported types that represent domain objects
- Use `camelCase` for functions, variables and utility helpers
- Suffix server-only modules with `.server.ts` when they depend on `next/headers`, cookies or other server runtime APIs

## Formatting and linting

### Backend

- Formatter and linter: `ruff`
- Max line length: `100`
- Import ordering is enforced

### Frontend

- Linter: `eslint`
- Formatter: `prettier`
- Type checking: `tsc --noEmit`

## Testing baseline

### Backend

- Test runner: `pytest`
- API tests should prefer `fastapi.testclient.TestClient`
- Unit tests should focus on service behavior and HTTP contract semantics

### Frontend

- Test runner: `vitest`
- Prefer pure utility tests first
- Add component tests when behavior becomes interactive or stateful enough to justify them

## Suggested commands

### Backend

- `python -m pip install -e .[dev]`
- `ruff check .`
- `ruff format --check .`
- `pytest`

### Frontend

- `npm install`
- `npm run lint`
- `npm run format:check`
- `npm run typecheck`
- `npm run test`
