<!-- JF-Hospitality — Universelle AI Coding Standards -->
<!-- Diese Datei wird automatisch von GitHub Copilot / AI-Agenten geladen. -->
<!-- Verbindlich für ALLE JF-Projekte. Keine Ausnahmen. -->
<!-- Projekt-spezifische Erweiterungen: am Ende dieser Datei ergänzen. -->

## Projekt

{{PROJEKT}} — <!-- TODO: Kurzbeschreibung einfügen -->

## Kontext-Quellen

- `.github/instructions/project-knowledge.instructions.md` — **Living Knowledge Base** (Infrastruktur, Architektur, Business-Kontext — wird automatisch geladen)

> **Hinweis für Entwickler:** Falls Copilot die Knowledge Base nicht automatisch lädt, manuell in VS Code aktivieren:
> `Settings → github.copilot.chat.codeGeneration.useInstructionFiles → true`
> Oder die Datei zu Beginn einer Chat-Session manuell als Kontext hinzufügen.

---

## 1 — Grundprinzipien

Diese Prinzipien gelten ausnahmslos für jede Codeänderung.

- **Secure by Default** — Jede Konfiguration und Schnittstelle ist im Ausgangszustand sicher. Unsichere Optionen müssen bewusst und dokumentiert aktiviert werden.
- **Zero Trust** — Keine Komponente wird implizit vertraut. Jede Anfrage wird authentifiziert, autorisiert und validiert — unabhängig vom Ursprung.
- **Fail Secure** — Bei Fehlern oder unerwarteten Zuständen fällt das System in einen sicheren Zustand. Fehler dürfen **niemals** Zugriff gewähren, der ohne den Fehler nicht bestünde.
- **Least Privilege** — Jeder Benutzer, Dienst und Prozess erhält ausschließlich die Berechtigungen, die für die spezifische Aufgabe erforderlich sind.
- **Input ist feindlich** — Alle externen Eingaben (User-Daten, API-Responses, Dateien, Webhooks) werden als potenziell bösartig behandelt und vor Verarbeitung validiert.
- **Defense in Depth** — Sicherheit hängt nie von einer einzelnen Maßnahme ab. Auth, Validierung, Netzwerk und Monitoring bilden unabhängige Schutzschichten.

---

## 2 — Security Standards

### 2.1 Authentication & Authorization

- **Auth an jeder Systemgrenze** — Jeder Endpunkt und jede Server Action beginnt mit einem Auth-Guard. Keine Ausnahmen außer explizit definierte Public-Routen (Health-Checks, Login).
- **IDOR/Object-Level Authorization** — Rollen-Check allein reicht NICHT. Jeder Zugriff auf eine Ressource MUSS prüfen, ob der anfragende User Eigentümer oder berechtigt ist (`resource.ownerId === session.userId` oder explizite Scope-Prüfung).
- **Rollenbasierte Zugriffssteuerung** — Admin-Operationen erfordern explizite Admin-Prüfung. Niemals nur Frontend-basierte Zugriffskontrolle.
- **Session-Security** — Serverseitige Sessions bevorzugen (DB-Sessions statt JWT wo möglich). Sessions mit definierten Lebenszeiten, HttpOnly/Secure/SameSite Cookie-Flags.

### 2.2 Input-Validierung & Injection-Prävention

- **Schema-Validierung an jeder Grenze** — Alle Eingaben via Zod (TS), Pydantic (Python) o.ä. validieren BEVOR Verarbeitung stattfindet. Unvalidierter Input darf nie an DB/Services weitergegeben werden.
- **Parametrisierte Queries** — ORM-Methoden oder parametrisierte Statements verwenden. Niemals String-Konkatenation in Queries.
- **Command Injection** — Kein `exec()`, `spawn()`, `os.system()` o.ä. mit User-Input. Shell-Ausführungen nur über Allowlists.
- **XSS-Prävention** — Framework-Escaping nutzen. Kein `dangerouslySetInnerHTML` / `set:html` / `|safe` ohne explizite Sanitisierung.
- **File-Upload-Validierung** — Mehrstufig: Dateigröße → MIME-Type → Magic-Byte-Validierung → Filename-Sanitization.

### 2.3 Fail Secure & Error Handling

- **Deny by Default** — Wenn ein Auth-Check, eine Validierung oder ein Daten-Lookup fehlschlägt → Zugriff verweigern. Niemals bei Fehlern Zugriff gewähren.
- **Error Response Sanitization** — Production-Responses dürfen KEINE Stacktraces, DB-Schema-Details, interne Dateipfade oder Server-Versionen enthalten. Benutzerfreundliche Fehlermeldungen ohne technische Details.
- **Keine leeren Catches** — Try-Catch-Blöcke dürfen sicherheitskritische Fehler nicht verschlucken. Errors loggen, sicher behandeln, niemals ignorieren.

### 2.4 Infrastructure & Production Hardening

- **Security Headers** — Jede Web-Applikation MUSS mindestens setzen: `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy` (angemessen restriktiv).
- **CORS** — Explizite Allowlist für erlaubte Origins. `Access-Control-Allow-Origin: *` ist verboten.
- **TLS everywhere** — Alle Kommunikation über TLS 1.2+. HTTP ohne Redirect ist verboten.
- **Production Hardening** — Debug-Modi, Hot-Reload-Endpoints, Source Maps und Dev-Tools dürfen in Production NICHT aktiviert sein.
- **Container als non-root** — Docker-Container laufen als non-root User. Localhost-only Port-Binding in Production.
- **Keine Secrets im Code** — Alle Secrets via Environment-Variablen oder Secret-Management. `.env` in `.gitignore`. Keine Secrets in Logs.

### 2.5 Rate Limiting & Abuse Prevention

- **Rate Limiting ist Baseline** — Alle API-Endpunkte MÜSSEN Rate Limiting haben. Nicht "abwägen", sondern Standard.
- **Ressourcenintensive Operationen** — Imports, Bulk-Writes, Report-Generierung: explizite Throttling-Mechanismen.
- **Bounded Processing** — Queue-Verarbeitung mit konfigurierbarer Batch-Größe, kein unbegrenztes Processing.

### 2.6 Least Privilege

- **DB-Credentials** — Applikationen nutzen DB-User mit minimalen Rechten. Keine Admin/Root-Credentials in App-Config.
- **Service-Accounts** — Jeder Dienst bekommt eigene Credentials mit Scope-Einschränkung.
- **API-Keys** — Kryptografisch generiert, SHA-256-gehasht in DB gespeichert, nur einmal bei Erstellung sichtbar.

### 2.7 Audit Trail

- **Activity Logging** — Sicherheitsrelevante Aktionen (Auth-Events, Datenmutationen, Admin-Operationen) werden protokolliert: Wer, was, wann, welche Entität.
- **Logging ist fire-and-forget** — Logging-Fehler blockieren nie den Hauptflow, werden aber als Warning geloggt.
- **Keine sensiblen Daten in Logs** — Passwords, API-Keys, Tokens, PII niemals loggen. Nur IDs und Aktionstypen.

### 2.8 Secrets at Rest

- **Drittanbieter-Credentials in DB verschlüsseln** — Secrets die wieder auslesbar sein müssen (OAuth Client Secrets, API-Keys externer Dienste) werden mit AES-256-GCM verschlüsselt gespeichert. Niemals Klartext. Eigene API-Keys → SHA-256-Hash (§ 2.6). Drittanbieter-Secrets → reversible Verschlüsselung.
- **Encrypt-on-Write / Decrypt-on-Read** — Jeder Codepfad der Drittanbieter-Secrets in die DB schreibt MUSS `encrypt()` aufrufen. Jeder Codepfad der sie liest und weitergibt (z.B. an externe APIs) MUSS `decrypt()` aufrufen. Das gilt für ALLE Stellen: Route-Handler, Background-Jobs, Sync-Prozesse.
- **Integritätsprüfung** — Vor dem Decrypt prüfen ob der Wert verschlüsselt ist (z.B. `isEncrypted()`), um Abwärtskompatibilität bei Migration bestehender Klartext-Werte zu gewährleisten.
- **Cache-Invalidierung** — Nach Credential-Updates MÜSSEN betroffene Caches (Token-Cache, Session-Cache) invalidiert werden.

---

## 3 — DSGVO & Datenschutz

- **PII-Minimierung** — Nur personenbezogene Daten erheben und speichern, die für den konkreten Zweck erforderlich sind. Keine Vorratsspeicherung.
- **Zweckbindung** — Daten nur für den erhobenen Zweck verwenden. Keine Zweckentfremdung ohne neue Rechtsgrundlage.
- **Löschpflichten** — Löschfristen definieren und technisch umsetzen. Right-to-Erasure (Art. 17 DSGVO) muss implementierbar sein.
- **Keine PII in Logs/Error-Reports** — Namen, E-Mail-Adressen, IPs, Zahlungsdaten gehören nicht in Log-Dateien, Error-Tracker oder Analytics.
- **Datenexport** — Systeme müssen perspektivisch Nutzerdaten exportieren können (Art. 20 DSGVO — Datenportabilität).
- **Einwilligungsmanagement** — Wo Einwilligung die Rechtsgrundlage ist, muss diese dokumentiert und widerrufbar sein.

---

## 4 — Saubere Architektur

- **Schichtenarchitektur** — Presentation → Application → Domain → Infrastructure. Keine direkten DB-Zugriffe aus der Presentation-Schicht.
- **Thin API Layer** — Endpunkte sind reine Orchestrierung: Auth → Params → Business Logic → Response. Keine Geschäftslogik in Route-Handlern.
- **Error-Handling** — Result/Union Types (`{ success, data } | { error }`) statt Exceptions für erwartete Fehler. Exceptions nur für unerwartete Zustände.
- **Soft Delete bevorzugen** — Geschäftsrelevante Entitäten archivieren statt löschen. Destruktive Löschung nur bei echten Cleanup-Fällen.
- **Fail-soft für Side Effects** — Logging, Notifications, Analytics dürfen fehlschlagen ohne den Hauptflow zu blockieren.
- **Feature-Module isoliert** — Zusammengehörige Logik pro Domain. Kopplung nur über definierte Interfaces und Shared Layer.

---

## 5 — Performante Datenbank-Nutzung

- **Minimale Reads** — Nur benötigte Felder laden (`select`). Vollständige Relations nur für Detail-Ansichten und Reports.
- **Parallele Queries** — Unabhängige Abfragen via `Promise.all()` / `asyncio.gather()` parallelisieren.
- **Keine N+1 Queries** — Relations per `include`/`joinedload` laden, nicht per Loop einzeln abfragen.
- **Transactions für atomare Writes** — Zusammengehörige Writes in einer Transaction. Bei Fehler → komplett Rollback.
- **Idempotente Upserts** — Sync-Writes via Upsert auf Compound Keys statt check-then-insert.
- **Batch-Operationen** — `createMany`, `bulk_insert` statt Loops mit Einzeloperationen.
- **Connection Singleton** — Einen DB-Client pro App, lazy initialisiert. Niemals pro Request einen neuen Client erstellen.
- **Indexes auf Access-Paths** — Häufig gefilterte Felder brauchen Indexes. Compound Unique Constraints für Business-Logik.
- **Cascade bewusst wählen** — `onDelete: Cascade` nur bei echten Lifecycle-Abhängigkeiten. Migrations sind append-only.

---

## 6 — Testing-Standards

- **Was MUSS getestet werden:** Domain-Engines (reine Funktionen), Security-Contracts (Auth, Zugriffsprüfung), Validierungs-Schemas (Edge Cases), Scheduler/Timing-Logik.
- **Negative Cases sind Pflicht** — Nicht nur Happy Path testen. Ungültige Eingaben, fehlende Berechtigungen, Grenzwerte.
- **Test-Pattern:** Arrange → Act → Assert. Ein Verhalten pro Test.
- **Build-Validation vor Commit** — Type-Checks und Linter müssen grün sein bevor Code committed wird.
- **Mocks aktuell halten** — Bei API/Service-Erweiterungen alle Mock-Fabriken aktualisieren (häufige Fehlerquelle).

---

## 7 — Moderne, barrierefreie User Interfaces

- **Accessibility: WCAG AA Minimum** — Keyboard-Navigation, Screen-Reader-Kompatibilität, ausreichende Kontraste, Focus-Indicators.
- **Strukturierte Eingaben** — Datepicker, Dropdowns, Toggles statt Freitext wo möglich. Freitext nur ergänzend.
- **Loading & Error States** — Jede interaktive Aktion braucht visuelles Feedback (Loading-Spinner, Success-Toast, Error-Meldung).
- **Corporate Design** — JF-Hospitality Farbtokens: Primary `#5676ad`, Background `#f4f2ee`, Text `#333333`. Alle Farben als CSS Custom Properties.
- **Icons:** `lucide-react` (TS/React) oder vergleichbar konsistentes Icon-Set.
- **Sprache:** Code auf Englisch, UI-Texte auf Deutsch. Fehlermeldungen benutzerfreundlich, ohne technische Details.

---

## 8 — Observability & Monitoring

- **Strukturiertes Logging** — JSON-Format bevorzugen. Log-Levels konsequent nutzen: ERROR (Systemfehler), WARN (unerwartetes Verhalten), INFO (geschäftsrelevante Events), DEBUG (Entwicklung).
- **Keine PII/Secrets in Logs** — Nur IDs, Aktionstypen und technische Metadaten loggen.
- **Health-Endpoints** — Jede deploybare App MUSS einen `/health` oder `/api/health` Endpoint haben (ohne Auth).
- **Error Tracking** — Production-Apps SOLLTEN ein Error-Tracking-Tool nutzen (Sentry o.ä.), damit Fehler nicht nur durch User-Beschwerden entdeckt werden.
- **Request-Correlation** — Bei Microservice-Architekturen: Correlation-IDs über Service-Grenzen mitführen.

---

## 9 — API-Design Standards

- **Konsistentes Error-Format** — Alle API-Fehler folgen einem einheitlichen Format: `{ "error": "Benutzerfreundliche Nachricht" }`. Keine Stacktraces, DB-Details oder interne Pfade.
- **Pagination** — Listen-Endpoints MÜSSEN paginiert sein. Kein unbegrenzter Result-Return.
- **Versionierung** — Externe APIs mit Versionierung (URL-Prefix `/v1/` oder Header). Breaking Changes nur in neuen Major-Versionen.
- **Minimale Response** — Nur benötigte Felder zurückgeben. Kein Over-Fetching von vollständigen DB-Records.
- **HTTP-Semantik** — Korrekte Status-Codes: 200 (OK), 201 (Created), 400 (Client-Fehler), 401 (Unauthenticated), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Validation), 429 (Rate Limited), 500 (Server-Fehler).

---

## 10 — AI-gestützte Entwicklung

- **KI-Output ist untrusted** — Jeder KI-generierte Code wird behandelt wie Output eines Junior-Entwicklers: nicht vertrauenswürdig bis reviewed.
- **Phantom-Dependency-Schutz** — KI halluziniert Paketnamen. Jede vorgeschlagene Dependency MUSS gegen die offizielle Registry verifiziert werden: existiert es? Wer ist der Maintainer? Bekannte Vulnerabilities?
- **Review-Fokus bei KI-Code** — Besondere Aufmerksamkeit auf: Input-Validierung, Auth-Logik, neue Dependencies, Business-Logic-Alignment.
- **Known Pitfalls pflegen (PFLICHT)** — JEDER Bugfix der durch eine externe API-Fehlermeldung, ein falsches Feldnamen-Mapping, ein unerwartetes Framework-Verhalten oder einen Datenstruktur-Fehler verursacht wurde MUSS SOFORT als Pitfall-Eintrag dokumentiert werden — BEVOR der Task als abgeschlossen gemeldet wird. Format: `**[Titel]**: Symptom → Lösung. (Bereich)`. Eintrag in BEIDE Dateien: `.github/copilot-instructions.md` (Projekt-spezifische Known Pitfalls) UND `.github/instructions/project-knowledge.instructions.md` (passende Sektion). Agent-Workflow: Vor Debugging die Pitfalls-Sektion ZUERST prüfen.
- **Project Knowledge Base pflegen (PFLICHT)** — Wenn du während der Arbeit ein grundlegendes Projektfakt entdeckst (Infrastruktur, Architektur-Entscheidung, Workaround, API-Feldnamen, Datenformate), das zukünftige Sessions wissen müssten: trage es SOFORT eigenständig in `.github/instructions/project-knowledge.instructions.md` ein — BEVOR der Task als abgeschlossen gemeldet wird. Keine Duplikate, max 40 Einträge, veraltete entfernen wenn Limit erreicht.
- **Testdaten aus DB ableiten** — Beim Erstellen neuer Testdaten oder Sample-Daten IMMER zuerst existierende DB-Einträge prüfen und Feldnamen/Formate daraus ableiten. NIEMALS Feldnamen raten (z.B. `email` statt `emailAddress`, `title` statt `nameTitle`).

---

## 11 — Supply Chain & Dependency Security

- **Lock-Files committen** — `package-lock.json`, `poetry.lock`, `uv.lock` etc. MÜSSEN im Repo sein. Deterministische Builds.
- **Regelmäßige Audits** — `npm audit` / `pip audit` regelmäßig ausführen. Critical/High Vulnerabilities zeitnah fixen.
- **Dependency-Prüfung** — Vor jeder neuen Dependency: Lizenz prüfen, Maintainer verifizieren, bekannte CVEs checken.
- **Pinning-Strategie** — Exakte Versionen in Lock-Files. Keine offenen Ranges in Production-Dependencies.
- **Minimale Dependencies** — Kein Paket für Trivialfunktionen. Weniger Dependencies = weniger Angriffsfläche.

---

## 12 — Git-Workflow

- **Conventional Commits** — `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`, `security:`.
- **Feature Branches** — Neue Features und Fixes auf separaten Branches entwickeln. PR/Review für Production-Merges.
- **Build vor Merge** — Type-Checks, Linter und Tests MÜSSEN grün sein bevor Code in den Hauptbranch gemergt wird.
- **Keine Secrets in Git-History** — Wenn Secrets versehentlich committet wurden: sofort rotieren, nicht nur in neuem Commit entfernen.
- **Migrations append-only** — Bestehende DB-Migrations NIEMALS editieren. Neue Migration für Schema-Änderungen.

---

## 13 — Coding-Konventionen

- **Strict Mode** — TypeScript: `strict: true`, `noUncheckedIndexedAccess: true`. Python: Type Hints + Strict Linting.
- **Kein `any` / `@ts-ignore` / `type: ignore`** — Ohne dokumentierte Begründung verboten.
- **Naming:** camelCase (Variablen/Funktionen), PascalCase (Klassen/Components), snake_case (DB-Spalten, Python).
- **Sprache:** Code und Kommentare auf Englisch. UI-Texte und Fehlermeldungen auf Deutsch.
- **Imports:** Konsistente Import-Organisation. Path-Aliases (`@/` → `src/`) wo vom Framework unterstützt.

---

## 14 — Known Pitfalls

<!-- Lebende Sektion: Max 30 Einträge. Agent fügt nach nicht-trivialen Bugfixes neue hinzu. -->
<!-- Format: **[Titel]**: Symptom → Lösung. (Bereich) -->
<!-- Vor dem Debugging: diese Sektion ZUERST prüfen! -->
<!-- Veraltete Einträge entfernen wenn Limit erreicht. -->

- **Crypto-Modul existiert ≠ Crypto wird aufgerufen**: Crypto-Utility (`encrypt()`/`decrypt()`) implementiert aber nie in Routes/Services importiert → Credentials im Klartext in DB. Lösung: Bei JEDEM neuen Codepfad der Drittanbieter-Credentials liest/schreibt prüfen ob `encrypt()`/`decrypt()` aufgerufen wird. (Security, § 2.8)

---

<!-- ============================================================ -->
<!-- PROJEKT-SPEZIFISCHE ERWEITERUNGEN AB HIER -->
<!-- Die Sektionen oben sind universelle JF-Standards. -->
<!-- Projekt-spezifische Regeln (Framework, Pfade, etc.) unten ergänzen. -->
<!-- ============================================================ -->

## Projekt-spezifisch

<!-- TODO: Framework-spezifische Patterns hier ergänzen, z.B.: -->
<!-- - Next.js App Router Conventions -->
<!-- - FastAPI Endpoint-Patterns -->
<!-- - Prisma/SQLAlchemy Schema-Regeln -->
<!-- - Dateipfade und Projektstruktur -->

### Vollständige Guideline-Referenzen

Die folgenden Dateien sind vollständig Teil dieser Instructions und müssen bei jeder relevanten Aufgabe berücksichtigt werden:

- **UI/UX:** @docs/ui_ux_guidelines.md — Layout, Komponenten, Zustände, Microcopy, Barrierefreiheit
- **Engineering:** @docs/engineering_guidelines.md — Code-Style, API-Design, Testing-Strategie, Security, Logging
- **E2E Testing:** @docs/e2e_testing_guidelines.md — Playwright-Setup, Auth-Injection, API-Mocking, Audit-Reporting

Neue UI-Patterns, technische Entscheidungen oder abweichende Patterns **immer** in der jeweiligen Guideline-Datei dokumentieren (per PR).

### Known Pitfalls

<!-- Lebende Sektion: Max 30 Einträge. Agent fügt nach nicht-trivialen Bugfixes neue hinzu. -->
<!-- Format: **[Titel]**: Symptom → Lösung. (Bereich) -->
<!-- Vor dem Debugging: diese Sektion ZUERST prüfen! -->

*(Noch keine Einträge — werden im Projektverlauf ergänzt)*
