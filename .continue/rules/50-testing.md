---
globs: ["**/*.test.ts", "**/*.spec.ts", "**/*.test.tsx", "**/*.spec.tsx", "**/__tests__/**"]
alwaysApply: false
---
# Testing Standards

## Universal Testing Principles

- **Test Behavior, Not Implementation** — Tests verify observable behavior, not internal structure.
- **Negative Cases Are Mandatory** — Invalid inputs, missing permissions, boundary values — not just happy paths.
- **Arrange → Act → Assert** — One behavior per test. Clear structure.
- **Build Validation Before Commit** — Type-checks, linter, unit tests must pass before commit.
- **Mocks Stay Current** — Update mock factories when APIs/schemas change (common regression source).

## Unit & Integration Testing

### What MUST Be Tested

- **Domain Engines** — Pure functions with business logic
- **Security Contracts** — Auth, authorization checks, input validation
- **Validation Schemas** — Edge cases, malformed data, enum boundaries
- **Scheduler / Timing Logic** — Retry policies, timeouts, cron jobs

### Quality Standards

- Domain logic: 80%+ coverage target
- Integration tests for API endpoints and DB interactions
- Contract tests for external API dependencies
- Testcontainers (or equivalent) for DB/Redis/external services in integration tests

---

## E2E Testing (Playwright) — JF Standard

### Goals & Scope

- **Behavior Tests** — Pages load, forms work, navigation correct
- **UI Audit** — Corporate Design (colors, language), Loading/Empty/Error states present, Accessibility basics
- **Contract Verification** — Frontend forms/options match backend schema (missing fields, stale enum values)
- **Audit Reporting** — Structured summary: what works, where are gaps

### Playwright Configuration (Deterministic CI Defaults)

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,         // Deterministic order
  workers: 1,                   // Single worker for stability
  forbidOnly: !!process.env.CI, // No .only in CI
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  webServer: {
    command: '<DEV_SERVER_COMMAND>',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
    env: { /* E2E-specific env vars */ },
  },
  projects: [{
    name: 'chromium',
    use: { viewport: { width: 1280, height: 720 } },
  }],
});
```

**Rationale:** Single worker avoids race conditions on shared state (DB, auth mocks). Sequential execution enables audit suites that build on each other. `forbidOnly` prevents accidental `.only()` commits.

### Auth Setup — Programmatic Session Injection

**Principle:** Inject session cookies programmatically instead of UI login. Saves 2-5s/test, eliminates auth provider dependency.

```typescript
// e2e/auth-setup.ts — Auth.js / NextAuth v5 pattern
import { EncryptJWT } from 'jose';
import * as hkdf from '@panva/hkdf';
import type { BrowserContext } from '@playwright/test';

const COOKIE_NAME = 'authjs.session-token';
const SECRET = process.env.AUTH_SECRET || 'test-secret-min-32-chars-long!!!';

async function deriveKey(): Promise<Uint8Array> {
  return hkdf.default(
    'sha256', SECRET, '',
    `Auth.js Generated Encryption Key (${COOKIE_NAME})`,
    64  // A256CBC-HS512 needs 64 bytes
  );
}

export async function injectSession(
  context: BrowserContext,
  session: { user: { id: string; name: string; email: string }; [key: string]: unknown }
): Promise<void> {
  const key = await deriveKey();
  const token = await new EncryptJWT({ ...session })
    .setProtectedHeader({ alg: 'dir', enc: 'A256CBC-HS512' })
    .setIssuedAt()
    .setExpirationTime('1h')
    .encrypt(key);

  await context.addCookies([{
    name: COOKIE_NAME, value: token, domain: 'localhost',
    path: '/', httpOnly: true, secure: false, sameSite: 'Lax',
  }]);
}
```

### API Mocking Strategy — Centralized Interception

**Principle:** Centralized `page.route()` interception — tests backend-independent while validating contracts.

```typescript
// Auth endpoints
await page.route('**/api/auth/session', route =>
  route.fulfill({ json: { user: { id: '1', name: 'Test User', email: 'test@example.com' } } })
);
await page.route('**/api/auth/csrf', route =>
  route.fulfill({ json: { csrfToken: 'test-csrf-token' } })
);

// Backend API — method-branching regex interception
await page.route(/\/api\/v1\/resources/, async (route) => {
  const method = route.request().method();
  if (method === 'GET') {
    return route.fulfill({ status: 200, json: { data: [{ /* schema-compliant */ }], error: null } });
  }
  if (method === 'POST') {
    return route.fulfill({ status: 201, json: { data: { id: 'new-id', /* ... */ }, error: null } });
  }
  return route.fulfill({ status: 200, json: { data: null, error: null } });
});
```

**Mock Data Conventions:**
- Mock payloads MUST match actual backend schema (field names, types, enums)
- Stale mocks break contract tests — this is intentional
- Define mocks centrally at test file top or in fixtures

### CSP Handling (Next.js Dev Mode)

```typescript
// Strip CSP headers that block Playwright-injected scripts
await page.route('**/*', async (route) => {
  const response = await route.fetch();
  const headers = { ...response.headers() };
  delete headers['content-security-policy'];
  delete headers['content-security-policy-report-only'];
  await route.fulfill({ response, headers });
});
```

### Test Structure Conventions

```typescript
// Domain-driven describe blocks
test.describe('1. Login & Auth', () => { /* ... */ });
test.describe('2. Navigation & Sidebar', () => { /* ... */ });
test.describe('3. Resource List', () => { /* ... */ });
test.describe('4. Resource Detail', () => { /* ... */ });
test.describe('N. Cross-Cutting: Corporate Design & Standards', () => { /* ... */ });

// beforeEach composition — every test gets same setup
test.beforeEach(async ({ page, context }) => {
  await injectSession(context, testSession);   // 1. Auth
  await page.route('**/*', stripCspHeaders);   // 2. CSP
  await registerAllMocks(page);                // 3. API mocks
});

// Contract-aware tests
test('Form has all backend schema fields', async ({ page }) => {
  await page.goto('/resources/new');
  await expect(page.locator('label:has-text("Titel")')).toBeVisible();
  await expect(page.locator('label:has-text("Status")')).toBeVisible();
  await expect(page.locator('label:has-text("Priorität")')).toBeVisible();
  // Add project-specific fields
});
```

### Audit Reporting

```typescript
const auditFindings: Array<{ category: string; status: 'pass' | 'warning' | 'info'; message: string }> = [];

// In tests
auditFindings.push({ category: 'UI', status: 'pass', message: 'Login page shows all elements' });
auditFindings.push({ category: 'Contract', status: 'warning', message: 'Field "dueDate" in backend but no UI input' });

// afterAll summary
test.afterAll(() => {
  console.log('\n══════════════════════════════════════');
  console.log('       UI AUDIT — ZUSAMMENFASSUNG');
  console.log('══════════════════════════════════════\n');
  const passed = auditFindings.filter(f => f.status === 'pass');
  const warnings = auditFindings.filter(f => f.status === 'warning');
  const infos = auditFindings.filter(f => f.status === 'info');
  console.log(`✅ Passed: ${passed.length}`);
  console.log(`⚠️  Warnings: ${warnings.length}`);
  console.log(`ℹ️  Info: ${infos.length}`);
  warnings.forEach(f => console.log(`  ⚠️  [${f.category}] ${f.message}`));
  infos.forEach(f => console.log(`  ℹ️  [${f.category}] ${f.message}`));
});
```

### CI Integration

```yaml
# GitHub Actions example
e2e:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: 20 }
    - run: npx playwright install --with-deps chromium
    - run: pnpm install
    - run: pnpm test:e2e
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: playwright-report
        path: playwright-report/
```

### Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

### Maintenance

- New pages/features → immediate "page loads + basic elements" test
- Mock data updated when backend schema changes (contract tests break intentionally)
- `warning` findings addressed in next iteration or explicitly marked `info` (accepted gap)

---

## Reference Implementation

Full reference: [JF PM-Tool E2E Suite](https://github.com/jf-hospitality/pm_modul)
