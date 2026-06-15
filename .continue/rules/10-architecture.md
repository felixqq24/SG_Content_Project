---
alwaysApply: true
---
# Architecture Standards

## Universal Architecture Principles

- **Layered Architecture** — Presentation → Application → Domain → Infrastructure. No direct DB access from presentation layer.
- **Thin API Layer** — Endpoints orchestrate only: Auth → Params → Business Logic → Response. No business logic in route handlers.
- **Feature Modules Isolated** — Cohesive domain logic grouped together. Coupling only via defined interfaces and shared layer.
- **Multi-Tenancy First** — Every data access must respect tenant context. IDOR/Object-Level Authorization mandatory: roles alone insufficient, must verify `resource.ownerId === session.userId` or explicit scope.

## Database Architecture

- **Minimal Reads** — Select only needed fields. Full relations only for detail views and reports.
- **Parallel Queries** — Independent queries via `Promise.all()` / `asyncio.gather()`.
- **No N+1 Queries** — Load relations via `include`/`joinedload`, not per-item loops.
- **Transactions for Atomic Writes** — Related writes in single transaction. Rollback on any failure.
- **Idempotent Upserts** — Sync writes via upsert on compound keys, not check-then-insert.
- **Batch Operations** — `createMany`, `bulk_insert` over loops with single operations.
- **Connection Singleton** — One DB client per app, lazy initialized. Never new client per request.
- **Indexes on Access Paths** — Frequently filtered fields need indexes. Compound unique constraints for business logic.
- **Cascade Consciously** — `onDelete: Cascade` only for true lifecycle dependencies.
- **Migrations Append-Only** — Never edit existing migrations. New migration for schema changes.

## API Design

- **Consistent Error Format** — `{ "error": "User-friendly message" }`. No stack traces, DB details, internal paths.
- **Pagination Required** — List endpoints must paginate. No unbounded result returns.
- **Versioning** — External APIs versioned (`/v1/` prefix or header). Breaking changes only in new major versions.
- **Minimal Response** — Return only needed fields. No over-fetching full DB records.
- **HTTP Semantics** — Correct status codes: 200, 201, 400, 401, 403, 404, 409, 422, 429, 500.

## Network & Deployment

- **TLS Everywhere** — All communication over TLS 1.2+. HTTP without redirect forbidden.
- **Security Headers** — Minimum: HSTS, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, CSP.
- **CORS Explicit** — Explicit allowlist origins. `Access-Control-Allow-Origin: *` forbidden.
- **Container Non-Root** — Docker containers run as non-root user. Localhost-only port binding in production.
- **Health Endpoints** — Every deployable app must expose `/health` or `/api/health` (no auth).

## Error Handling

- **Result/Union Types** — `{ success, data } | { error }` for expected errors. Exceptions only for unexpected states.
- **Soft Delete Preferred** — Archive business entities instead of hard delete. Hard delete only for true cleanup.
- **Fail-Soft Side Effects** — Logging, notifications, analytics may fail without blocking main flow.

## Documentation Requirements

Each project maintains living architecture docs covering:
- System overview (ASCII diagram or description)
- Network topology table
- Tech stack table with versions
- Auth flow description
- Data model overview (entities, relations, ORM)
- Deployment process and rollback reference
