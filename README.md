# Support Tools Modernization Demo

This repository is a sanitized portfolio case study about modernizing a legacy internal support tool into a cleaner, safer, and more maintainable platform.

The original system mixed server-rendered Java/JSP pages, LDAP authentication, direct integrations, and HTML assembled in backend code. The modernization effort introduces explicit APIs, a modern frontend, clearer architecture boundaries, and stronger security thinking.

My work here focused on translating a real operational workflow into a safer migration path: understanding legacy behavior, shaping the target architecture, implementing parts of the new platform, documenting trade-offs, and using security review to influence engineering priorities rather than treating it as a separate afterthought.

## What this project demonstrates

- Migrating a legacy operational tool without losing critical business behavior
- Converting implicit server behavior into explicit API contracts
- Reworking authentication and session handling for a modern web stack
- Improving developer experience with typed backend/frontend code and automated tests
- Identifying security risks early instead of treating them as post-launch cleanup

## The problem I was solving

The legacy workflow made technical investigation slower than it needed to be. Operators had to retrieve payloads manually, copy them into external tools, format them by hand, and mentally reconstruct what the system was doing.

That creates three problems:

- operational friction
- avoidable human error
- architecture that becomes harder to evolve over time

The modernization goal was not just to refresh the UI. It was to preserve operational usefulness while reducing hidden behavior, local configuration coupling, and long-term maintenance cost.

That distinction matters because this was not a greenfield product problem. It was a migration problem in a support-sensitive context, where breaking a familiar flow can be more damaging than shipping slowly.

## Repository structure

```text
.
|-- NetQTools/          # Legacy Java/JSP implementation used as functional reference
|-- netq-log-platform/  # Modern platform in progress
|   |-- backend/        # FastAPI backend
|   |-- frontend/       # Next.js frontend
|   |-- k8s/            # Deployment manifests and config examples
|   `-- docs/           # Migration, parity, auth, and design notes
|-- screenshots/        # UI reference images from the legacy flow
`-- SECURITY_REPORT.md  # Public-facing summary of key security findings
```

## Architecture direction

The target architecture separates responsibilities clearly:

- `frontend`: Next.js application for authenticated operational workflows
- `backend`: FastAPI service exposing explicit JSON contracts
- `auth`: server-managed session model with secure cookie semantics
- `integrations`: isolated adapters for external systems
- `deployment`: container-first packaging with Kubernetes-friendly configuration

This design direction reflects principles I care about in real delivery work:

- business workflows should not depend on hidden UI-side behavior
- integration logic should not be mixed with presentation
- security boundaries should be enforced on the server, not only in the browser

In practice, that meant I was not only replacing frameworks. I was also making the system easier to reason about for future developers, operators, and reviewers.

## Why these technical choices matter

### Legacy kept as reference, not as target

I kept the legacy implementation in the repository because migrations fail when teams rewrite behavior they have not fully understood. The old system acts as a behavioral specification, even when the code quality is not something to preserve.

This also shaped how I validated the work: screenshots, captured behavior, migration notes, and parity-oriented documentation were all used to reduce the risk of "modernizing" away something operationally important.

### Explicit backend contracts

The legacy application assembled HTML in backend code. The modern version moves toward explicit API contracts, which makes testing, observability, and frontend iteration much safer.

One of the main trade-offs here is speed versus clarity. It is often faster to keep backend-generated fragments during a migration, but cleaner contracts pay off quickly once testing, reviewability, and maintainability become priorities.

### Server-owned authentication state

For an internal operational tool, I favored a server-managed session model over browser-owned tokens. That keeps invalidation simpler, reduces exposure to client-side storage misuse, and stays closer to the business expectations of the legacy tool.

That was a deliberate trade-off rather than a default preference. The goal was to optimize for operational predictability, revocation simplicity, and lower accidental exposure in the browser.

### Security as part of design, not just audit

A recurring theme in this project is that modernization is not complete if it only changes frameworks. It also has to challenge trust assumptions, secret handling, request boundaries, and session enforcement.

Some of the most valuable findings were not glamorous bugs. They were architecture-level issues: backend routes that relied too much on frontend protections, legacy trust assumptions around transport and certificates, and repository hygiene problems that would have become long-term liabilities if ignored.

## Current state

The repository reflects a migration in progress rather than a finished product.

- the legacy implementation is preserved as a functional reference
- the modern backend and frontend foundations are present
- authentication and session strategy are defined and partially implemented
- security review has already influenced the public shape of the repository
- some end-to-end operational flows still belong in the "next iteration" category

I prefer to show that state honestly because it says more about engineering judgment than presenting every project as if it were already complete.

## Screenshots

The `screenshots/` directory preserves selected reference images from the legacy flow. I use them as migration anchors to compare behavior, interaction patterns, and operator ergonomics during redesign work.

## What this project opens up technically

This project naturally opens discussion around:

- how to migrate legacy systems incrementally without losing business behavior
- how to choose between parity and redesign
- how to model auth/session for internal tools
- how to identify risky backend assumptions hidden behind frontend route guards
- how to sanitize and present real project work responsibly in public

It also shows the kind of work I enjoy most: the space between product behavior, backend architecture, frontend usability, and security realism.

## Security perspective

This repository includes a sanitized security review summary in [SECURITY_REPORT.md](SECURITY_REPORT.md).

The most important takeaway is that framework migration alone does not remove risk. Some of the highest-value work in projects like this comes from:

- removing secrets from source control
- enforcing authorization in the backend
- validating transport security assumptions
- reducing XSS-prone rendering patterns

## What I would improve next

- finish end-to-end parity for the remaining operational modules
- harden backend authorization around business routes
- improve test coverage around XML rendering and integration contracts
- further reduce internal naming and operational coupling in public-facing artifacts
- package the public version as a cleaner standalone demo

## Notes

- This is a sanitized portfolio repository, not a production deployment repository.
- Sensitive values, environment-specific details, and internal infrastructure references were intentionally removed or replaced.
- Some names remain in source paths because the repo documents a real migration shape, but the public presentation is intentionally generalized.
