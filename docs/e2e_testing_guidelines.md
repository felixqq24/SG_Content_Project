# E2E Testing Guidelines — SG_Content_Projekt

> Stand: 2026-04-18

Diese Guidelines standardisieren den E2E-Testansatz mit Playwright.  
E2E-Tests sind hier nicht nur Regressionstests, sondern ein **Hybrid aus Behavior-Tests, UI-Audit und Backend/Frontend-Contract-Prüfung**.

> **Referenz-Implementierung:** Die E2E-Suite des [JF PM-Tools](https://github.com/jf-hospitality/pm_modul) setzt diesen Standard vollständig um.

---

## 1. Ziele & Scope

- **Behavior-Tests:** Seiten laden, Formulare funktionieren, Navigation ist korrekt.
- **UI-Audit:** Corporate Design (Farben, Sprache), Loading/Empty/Error States vorhanden, Barrierefreiheit-Basics.
- **Contract-Prüfung:** Frontend-Formulare/Optionen stimmen mit Backend-Schema überein (fehlende Felder, veraltete Enum-Werte).
- **Audit-Reporting:** Strukturierte Zusammenfassung am Ende: was funktioniert, wo gibt es Lücken.

---

## 2. Playwright-Konfiguration

### 2.1. Deterministische CI-Defaults

```typescript
// playwright.config.ts — Standard-Pattern
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,         // Deterministische Reihenfolge
  workers: 1,                    // Single-Worker für Stabilität
  forbidOnly: !!process.env.CI,  // Kein .only in CI
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  webServer: {
    command: '<!-- TODO: Dev-Server-Command, z. B. "pnpm dev" -->',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
    env: {
      // TODO: E2E-spezifische Environment-Variablen
    },
  },
  projects: [
    {
      name: 'chromium',
      use: { viewport: { width: 1280, height: 720 } },
    },
  ],
});
```

### 2.2. Rationale

- **Single Worker:** Vermeidet Race Conditions bei Shared State (DB, Auth-Mocks).
- **`fullyParallel: false`:** Tests laufen in definierter Reihenfolge — wichtig für Audit-Suites die aufeinander aufbauen.
- **`forbidOnly` in CI:** Verhindert versehentlich committed `.only()`-Tests.
- **`webServer`:** Playwright startet die App automatisch — kein manuelles Starten nötig.

---

## 3. Auth-Setup-Strategie

**Prinzip:** Programmatische Session-Injection statt UI-Login. Spart ~2-5s pro Test und eliminiert Abhängigkeit vom Auth-Provider.

### 3.1. Auth.js / NextAuth v5 (Standard)

```typescript
// e2e/auth-setup.ts — Pattern
import { EncryptJWT } from 'jose';
import * as hkdf from '@panva/hkdf';
import type { BrowserContext } from '@playwright/test';

const COOKIE_NAME = 'authjs.session-token';
const SECRET = process.env.AUTH_SECRET || 'test-secret-min-32-chars-long!!!';

async function deriveKey(): Promise<Uint8Array> {
  return hkdf.default(
    'sha256',
    SECRET,
    '',
    `Auth.js Generated Encryption Key (${COOKIE_NAME})`,
    64  // A256CBC-HS512 braucht 64 Bytes
  );
}

export async function injectSession(
  context: BrowserContext,
  session: { user: { id: string; name: string; email: string }; /* ... */ }
): Promise<void> {
  const key = await deriveKey();
  const token = await new EncryptJWT({ ...session })
    .setProtectedHeader({ alg: 'dir', enc: 'A256CBC-HS512' })
    .setIssuedAt()
    .setExpirationTime('1h')
    .encrypt(key);

  await context.addCookies([{
    name: COOKIE_NAME,
    value: token,
    domain: 'localhost',
    path: '/',
    httpOnly: true,
    secure: false,  // localhost
    sameSite: 'Lax',
  }]);
}
```

### 3.2. Andere Auth-Provider

<!-- TODO: Für andere Auth-Provider (Keycloak, ZITADEL direkt, Authentik, etc.) -->
<!-- entsprechende Token-/Cookie-Generierung hier dokumentieren. -->
<!-- Pattern: Token programmatisch erzeugen, als Cookie/Header in den BrowserContext injizieren. -->

---

## 4. API-Mocking-Strategie

**Prinzip:** Zentralisierte `page.route()`-Interception — Tests sind backend-unabhängig bei gleichzeitiger Contract-Validierung.

### 4.1. Auth-Endpoint-Mocking

```typescript
// Auth-Endpoints zufriedenstellen (NextAuth/Auth.js)
await page.route('**/api/auth/session', route =>
  route.fulfill({ json: { user: { id: '1', name: 'Test User', email: 'test@example.com' } } })
);
await page.route('**/api/auth/csrf', route =>
  route.fulfill({ json: { csrfToken: 'test-csrf-token' } })
);
await page.route('**/api/auth/providers', route =>
  route.fulfill({ json: {} })
);
```

### 4.2. Backend-API-Mocking

```typescript
// Regex-basierte Interception mit Method-Branching
await page.route(/\/api\/v1\/resources/, async (route) => {
  const method = route.request().method();

  if (method === 'GET') {
    return route.fulfill({
      status: 200,
      json: { data: [/* TODO: Schema-konforme Mock-Daten */], error: null },
    });
  }

  if (method === 'POST') {
    return route.fulfill({
      status: 201,
      json: { data: { id: 'new-id', /* ... */ }, error: null },
    });
  }

  return route.fulfill({ status: 200, json: { data: null, error: null } });
});
```

### 4.3. Mock-Daten-Konventionen

- Mock-Payloads MÜSSEN dem tatsächlichen Backend-Schema entsprechen (gleiche Feldnamen, Typen, Enums).
- Werden Mock-Daten veraltet, bricht der Contract-Test — das ist gewünscht.
- Mock-Daten zentral am Anfang der Test-Datei oder in eigenen Fixtures definieren.

---

## 5. CSP-Handling

Next.js Dev-Mode setzt Content-Security-Policy-Header, die Playwright-injizierten Scripts blockieren können.

```typescript
// beforeEach: CSP-Header strippen
await page.route('**/*', async (route) => {
  const response = await route.fetch();
  const headers = { ...response.headers() };
  delete headers['content-security-policy'];
  delete headers['content-security-policy-report-only'];
  await route.fulfill({ response, headers });
});
```

**Wann nötig:** Nur wenn Next.js im Dev-Mode läuft. In Production-Builds oder anderen Frameworks ggf. nicht erforderlich.

---

## 6. Test-Struktur & Konventionen

### 6.1. Domain-getriebene Describe-Blöcke

```typescript
test.describe('1. Login & Auth', () => { /* ... */ });
test.describe('2. Navigation & Sidebar', () => { /* ... */ });
test.describe('3. Ressourcen-Liste', () => { /* ... */ });
test.describe('4. Ressourcen-Detail', () => { /* ... */ });
// ...
test.describe('N. Cross-Cutting: Corporate Design & Standards', () => { /* ... */ });
```

### 6.2. beforeEach-Composition

Jeder Test beginnt mit derselben Komposition:

```typescript
test.beforeEach(async ({ page, context }) => {
  // 1. Auth-Session injizieren
  await injectSession(context, testSession);

  // 2. CSP-Header strippen (falls Next.js)
  await page.route('**/*', stripCspHeaders);

  // 3. API-Mocks registrieren
  await registerAllMocks(page);
});
```

### 6.3. Contract-aware Tests

Tests prüfen nicht nur „Seite lädt", sondern:

```typescript
test('Formular hat alle Backend-Schema-Felder', async ({ page }) => {
  await page.goto('/resources/new');
  // Prüfe: Jedes Feld aus dem Backend-Schema hat ein entsprechendes UI-Element
  await expect(page.locator('label:has-text("Titel")')).toBeVisible();
  await expect(page.locator('label:has-text("Status")')).toBeVisible();
  await expect(page.locator('label:has-text("Priorität")')).toBeVisible();
  // TODO: Projektspezifische Felder ergänzen
});
```

---

## 7. Audit-Reporting

### 7.1. Findings sammeln

```typescript
const auditFindings: Array<{ category: string; status: 'pass' | 'warning' | 'info'; message: string }> = [];

// In Tests:
auditFindings.push({ category: 'UI', status: 'pass', message: 'Login-Seite zeigt alle Elemente' });
auditFindings.push({ category: 'Contract', status: 'warning', message: 'Feld "dueDate" im Backend vorhanden, aber kein UI-Input' });
```

### 7.2. Zusammenfassung am Suite-Ende

```typescript
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

---

## 8. CI-Integration

<!-- TODO: CI-Job-Konfiguration für Playwright ergänzen -->
<!-- Beispiel für GitHub Actions: -->
<!--
```yaml
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
-->

---

## 9. Scripts

Standard-Konvention für `package.json`:

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

---

## 10. Pflege

- Neue Seiten/Features bekommen sofort mindestens einen „Seite lädt + Grundelemente vorhanden"-Test.
- Mock-Daten werden bei Backend-Schema-Änderungen aktualisiert (Contract-Tests brechen absichtlich).
- Audit-Findings mit Status `warning` werden in der nächsten Iteration bearbeitet oder bewusst als `info` (accepted gap) markiert.
