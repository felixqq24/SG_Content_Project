# Engineering Guidelines — SG_Content_Projekt

> Stand: 2026-04-18

Diese Guidelines definieren zentrale Engineering-Prinzipien für SG_Content_Projekt.  
Ziel ist konsistenter, gut testbarer und sicherer Code – insbesondere im Hinblick auf Auth, Datenzugriff und Stabilität im Betrieb.

---

## 1. Ziele und Scope

- **Ziele**
  - Klare, wiederverwendbare Patterns für API, Auth und Datenzugriff.
  - Minimierung von Sicherheitsrisiken.
  - Verlässliche Tests für kritische Pfade.
- **Scope**
  - Code-Style & Struktur (High-Level)
  - API-Design & Fehlerbehandlung
  - Testing-Strategie
  - Security
  - Logging & Observability

Detaillierte Architektur-Entscheidungen stehen in `docs/architecture.md`.

---

## 2. Code-Style & Struktur

### 2.1. Allgemein

- Sprache: **TypeScript (strict)**, keine `any`-„Abkürzungen" ohne Begründung.
- Bevorzugt werden **kleine, fokussierte Module** statt „God-Services".
- Funktionen sollten reine Funktionen bevorzugen; Side Effects (DB, Netzwerk, Logging) klar gekapselt.

### 2.2. Benennung

<!-- TODO: Projektspezifische Pfade und Konventionen ergänzen -->
- **Routen**: `<!-- TODO: z. B. src/routes/<domain>.ts -->`
- **Middleware**: `authMiddleware`, `errorHandler` etc.
- **DB-Objekte**: <!-- TODO: ORM-spezifische Konventionen, z. B. Prisma-Modelle, Drizzle-Tabellen -->

### 2.3. Fehlerbehandlung

- Keine „stillen" `catch`-Blöcke ohne Logging.
- Fehler werden möglichst früh und nah an der Ursache behandelt.
- Erwartbare Fehler (Validation, Auth) sind keine 500er, sondern 4xx mit klarer Message.

---

## 3. API-Design & Fehlerbehandlung

### 3.1. API-Konventionen

- Basis-URL: `/api/v1/*`.
- RESTful Endpoints:
  - Ressourcen: `GET /resources`, `POST /resources`, `GET /resources/:id`, `PATCH /resources/:id`.
  - Sub-Ressourcen: `GET /resources/:id/children`, `POST /resources/:id/children`.
- Responses sind immer JSON.

### 3.2. Response-Shape

Standard-Shape:

```json
{
  "data": { ... },
  "error": null,
  "meta": { ... }
}
```

Bei Fehlern:

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Benutzerfreundliche Fehlermeldung.",
    "details": { ... }
  }
}
```

- **Validation-Fehler**: `400 BAD_REQUEST`, `code: "VALIDATION_ERROR"`.
- **Auth-Fehler**: `401 UNAUTHORIZED` (kein/ungültiges Token), `403 FORBIDDEN` (rollentechnisch verboten).
- **Nicht gefunden**: `404 NOT_FOUND`.
- **Serverfehler**: `500 INTERNAL_SERVER_ERROR` (immer mit korrelierbarem Log-Eintrag).

### 3.3. Versionierung

- Breaking Changes an der API nur mit:
  - Anpassung der Version (`/api/v2/...`) oder
  - klar dokumentierter Migration inkl. interner Abstimmung.
- Deprecated Endpoints in der Doku markieren und möglichst mit Sunset-Datum versehen.

---

## 4. Testing-Strategie

### 4.1. Testarten

- **Unit-Tests**
  - Für reine Logik (z. B. Berechnungen, Status-Transitions, Validierungs-Funktionen).
  - Keine echten DB-/Netzwerkzugriffe.
- **Integrationstests**
  - <!-- TODO: Framework -->-Routen gegen eine Test-DB (z. B. lokales PostgreSQL mit Test-Schema).
  - Fokus: Auth- und Rollen-Logik.
- **E2E-Tests (Playwright)**
  - Siehe `docs/e2e_testing_guidelines.md` für vollständige E2E-Konventionen.
  - Ausführung: `pnpm test:e2e` (headless), `pnpm test:e2e:ui` (mit Playwright UI).

### 4.2. „Done"-Definition für Backend-Features

Ein Backend-Feature gilt als „done", wenn:

- Positive und negative Pfade getestet sind (inkl. Auth/Rollen).
- `/health` weiterhin grün ist und CI-Pipeline Build + Tests erfolgreich ist.

### 4.3. Externe API-Spec-Validierung (Contract-Tests)

Bei Projekten mit **externen API-Integrationen** (Drittanbieter-APIs, SaaS-Dienste) gilt der **Test-First-Ansatz**:

1. **OpenAPI-Definitionen lokal cachen** — Spec-Datei als JSON-Fixture im Test-Ordner ablegen (`__fixtures__/`). Kein Netzwerkzugriff im Test.
2. **Mapper-Output gegen Schema validieren** — Rekursiv alle Properties des generierten Payloads gegen die API-Defintion prüfen. Unbekannte Properties werden als Fehler gemeldet (verhindert `400 Bad Request` durch unbekannte Felder in Production).
3. **Datenformat-Tests** — Edge-Cases der DB→API-Transformation absichern:
   - Datum: PostgreSQL liefert ISO-Timestamps (`2026-06-30T22:00:00.000Z`), APIs erwarten oft `YYYY-MM-DD`
   - Zahlen vs. Strings: Viele APIs erwarten `folioView` als Integer, `amount` als String etc.
   - Nested Structures: Envelope-Patterns (z. B. `addressInfo[].address.{}`) prüfen
4. **Reihenfolge: Spec-Test → Mapper → Deploy** — Niemals deploy-debug-fix-Zyklen als Testmethode. Erst den Spec-Test schreiben, dann den Mapper implementieren, dann deployen.
5. **Aktualisierung** — Bei API-Spec-Änderungen des Drittanbieters: Fixture aktualisieren, Tests laufen lassen, Mapper anpassen.

> **Pattern:** `<mapper>-spec.test.ts` + `__fixtures__/<api>-definitions.json`

<!-- Optional: Multi-Tenancy Tests -->
<!--
### 4.3. Tenant-Isolation-Tests (Pflicht für Multi-Tenant-Projekte)

Für Multi-Tenant-Routen gilt:

- Tests müssen sicherstellen, dass:
  - Ein User mit validem Token für Tenant A nicht auf Daten von Tenant B zugreifen kann.
  - Host-Tenant-Mismatch → `403`.
  - `search_path` korrekt gesetzt ist (indirekt überprüfbar über Data-Visibility).
-->

---

## 5. Security

### 5.1. Auth & Rollen

- Standard: Jede Route ist hinter Auth, außer explizit dokumentierte Ausnahme (z. B. `/health`).
- Rollenprüfung:
  <!-- TODO: Projektspezifische Rollen definieren, z. B.: -->
  <!-- - `admin`: systemweite Admin-Aufgaben -->
  <!-- - `member`: Arbeit innerhalb zugewiesener Bereiche -->
  <!-- - `guest`: eingeschränkter Zugriff -->

<!-- Diesen Abschnitt entfernen wenn Single-Tenant -->
### 5.2. Tenant-Kontext (nur Multi-Tenant-Projekte)

- Der Tenant wird **niemals** aus Request-Body oder Queryparametern bestimmt.
- Tenant-Kontext kommt ausschließlich aus:
  - Validiertem Access-Token und
  - Host-Header (Subdomain-Mapping).
- Die `tenantMiddleware`:
  - Prüft Konsistenz Host ↔ Token.
  - Setzt den DB-Kontext auf das korrekte Schema.

### 5.3. Datenzugriff

- DB-Queries erfolgen immer im korrekten Scope (z. B. Tenant-Schema bei Multi-Tenant).
- IDs sind **nur innerhalb ihres Kontexts** eindeutig; keine Cross-Scope-Annäherungen.

### 5.4. Sensitive Daten

- Access Tokens werden nie geloggt.
- Personendaten werden im Log nur pseudonymisiert oder stark minimiert (z. B. User-ID statt E-Mail).
- Error-Responses an den Client enthalten keine internen Stacktraces oder SQL-Snippets.

### 5.5. Rate Limiting

- **Jeder API-Endpunkt** ist rate-limited (Baseline-Schutz).
- Standard-Limits (anpassen an Projektanforderungen):
  - Global API: 100 Requests/Min pro IP.
  - Auth-intensive Routen: 20 Requests/Min pro IP.
  - Write-Operationen: 30 Requests/Min pro IP.
- Rate Limit-Responses: HTTP `429` mit `Retry-After`-Header und `X-RateLimit-Remaining`.
- Implementierung: In-Memory Sliding Window für Single-Instance. Bei Skalierung auf Multi-Instanz: Redis-backed Limiter erforderlich.

### 5.6. Secrets at Rest

Gilt für alle Projekte die Drittanbieter-Credentials in der DB speichern (OAuth Client Secrets, API-Keys externer Dienste, Webhook-Secrets).

- **Reversible Verschlüsselung (AES-256-GCM)** — Drittanbieter-Secrets die zum Aufruf externer APIs benötigt werden, MÜSSEN verschlüsselt in der DB liegen. Eigene API-Keys → Einweg-Hash (SHA-256). Drittanbieter-Secrets → `encrypt()`/`decrypt()`.
- **Encrypt-on-Write** — Jeder Codepfad der Credentials in die DB schreibt (Route-Handler POST/PUT, Seed-Scripts, Import-Jobs) MUSS `encrypt()` aufrufen.
- **Decrypt-on-Read** — Jeder Codepfad der Credentials liest und an externe Dienste weitergibt (API-Calls, Token-Requests, Sync-Jobs) MUSS `decrypt()` aufrufen.
- **Backward-Compat Guard** — Vor `decrypt()` mit `isEncrypted()` prüfen, ob der Wert tatsächlich verschlüsselt ist (Migration bestehender Klartext-Werte).
- **Cache-Invalidierung** — Nach Credential-Updates: Token-Cache, Session-Cache etc. invalidieren.
- **Checkliste bei neuem Credential-Feld:**
  1. Schema/Migration: DB-Spalte anlegen (kein spezieller Typ nötig, `text` reicht)
  2. Write-Path: `encrypt()` vor `INSERT`/`UPDATE`
  3. Read-Path: `decrypt()` + `isEncrypted()`-Guard an JEDER Stelle die das Feld liest
  4. Cache: Token-/Session-Cache nach Update invalidieren
  5. Test: Roundtrip-Test (encrypt → store → load → decrypt → verify)

---

## 6. Logging & Observability

### 6.1. Logging-Grundregeln

- Jeder Request erhält eine **Request-ID** (z. B. aus Header oder generiert), die in allen Logs auftaucht.
- Log-Level:
  - `info`: normale Operationen (Start/Ende von Jobs, wichtige Statusänderungen).
  - `warn`: ungewöhnliche, aber nicht kritische Zustände (z. B. Retry).
  - `error`: unerwartete Fehler, die untersucht werden müssen.
- Keine personenbezogenen Daten im Log, wo nicht unbedingt nötig.

### 6.2. Was mindestens geloggt wird

- Auth-Fehlschläge (`401/403`) mit Grund (z. B. „token_invalid").
- Unerwartete Fehler (`500`), inkl. Stacktrace im internen Log (nicht im Response).
- Kritische Aktionen:
  <!-- TODO: Projektspezifische kritische Aktionen ergänzen, z. B.: -->
  <!-- - Ressourcen-Erstellung/-Löschung -->
  <!-- - Admin-Operationen -->
  <!-- - Schema-Migrationsergebnisse -->

---

## 7. Pflege der Guidelines

- Änderungen an diesen Guidelines erfolgen per Pull Request (`docs/engineering_guidelines.md`).
- Neue Patterns werden ergänzt, sobald sie stabil sind.
- Abweichungen von den Guidelines sollen im PR begründet werden.

Diese Guidelines sind ein lebendes Dokument und sollen pragmatisch dabei helfen, Qualität, Sicherheit und Wartbarkeit sicherzustellen.
