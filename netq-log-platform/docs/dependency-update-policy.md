# Dependency Update Policy

## Purpose

This document defines a small, practical policy for dependency updates in `netq-log-platform`.

The goal is to keep dependencies secure, stable and auditable without introducing unnecessary churn.

## Principles

- Prefer official, widely adopted and actively maintained packages.
- Prefer stable releases over canary, beta, alpha or release-candidate versions.
- Prefer the smallest safe upgrade that removes the identified risk.
- Only accept major-version upgrades when security, support lifecycle or platform compatibility justify them.
- Every dependency update must be followed by quality and test pipeline execution.

## Approved sources

Dependency choices and upgrades should be guided by:

- official project documentation
- official security advisories
- package registry metadata for stable releases
- the project lockfile after successful validation

Examples:

- Next.js blog and upgrade guides
- FastAPI and Pydantic official documentation
- npm audit and Python package advisories

## Version strategy

### JavaScript and TypeScript

- Pin direct runtime dependencies to explicit versions in `package.json`.
- Keep related framework packages aligned on the same compatible line.
- For Next.js upgrades, update together when needed:
  - `next`
  - `eslint-config-next`
  - `react`
  - `react-dom`
  - related type packages

### Python

- Keep application and dev dependencies declared in `pyproject.toml`.
- Use bounded version ranges for libraries where compatibility matters.
- Install in a local virtual environment for development and validation.

## Update rules

### Security updates

- Apply immediately when a dependency has a known critical or high severity vulnerability.
- Prefer patch or minor upgrades first when they fully remediate the issue.
- If remediation requires a major upgrade, document the reason and validate the project end to end before adoption.

### Routine updates

- Batch low-risk routine updates instead of updating packages one by one without reason.
- Avoid opportunistic upgrades during unrelated feature work unless they remove an active risk or unblock the task.

### New dependencies

Before adding a new dependency, check:

- maintainer reputation and ecosystem trust
- recent release activity
- documentation quality
- compatibility with the project stack
- whether the same result can be achieved with existing approved dependencies

## Validation checklist

Every dependency update should include:

- lockfile updated
- lint passing
- formatter check passing
- typecheck passing when applicable
- tests passing
- vulnerability scan rerun when applicable

Current project commands:

- `make quality`
- `make test`
- `npm audit --audit-level=moderate`

## Change documentation

When a meaningful dependency update happens, record:

- what changed
- why it changed
- whether the change was security-driven, compatibility-driven or maintenance-driven
- which pipeline checks were executed

This can be captured in:

- task updates in `tasks.md`
- technical notes in `docs/`
- commit or PR description when available

## Current baseline

The current approved frontend security baseline uses stable Next.js 16 packages and a lockfile validated with the project pipeline.

Future updates should preserve the same decision model:

- official guidance first
- smallest safe stable version when possible
- full pipeline validation before considering the update done
