---
alwaysApply: true
---
# Security

## Authentication & Authorization

- **Auth an jeder Systemgrenze** — Jeder Endpunkt und jede Server Action beginnt mit einem Auth-Guard. Keine Ausnahmen außer explizit definierte Public-Routen (Health-Checks, Login).
- **IDOR/Object-Level Authorization** — Jeder Zugriff auf eine Ressource MUSS prüfen: Eigentümer oder berechtigt (`resource.ownerId === session.userId`).
- **Rollenbasierte Zugriffssteuerung** — Admin-Operationen erfordern explizite Admin-Prüfung. Niemals nur Frontend-basierte Zugriffskontrolle.
- **Session-Security** — Serverseitige Sessions bevorzugen (DB-Sessions statt JWT wo möglich). HttpOnly/Secure/SameSite Cookie-Flags.

## Input-Validierung & Injection-Prävention

- **Schema-Validierung an jeder Grenze** — Alle Eingaben via Zod (TS), Pydantic (Python) validieren BEVOR Verarbeitung. Unvalidierter Input darf nie an DB/Services weitergegeben werden.
- **Parametrisierte Queries** — ORM-Methoden oder parametrisierte Statements. Niemals String-Konkatenation in Queries.
- **Command Injection** — Kein `exec()`, `spawn()`, `os.system()` mit User-Input. Shell-Ausführungen nur über Allowlists.
- **XSS-Prävention** — Framework-Escaping nutzen. Kein `dangerouslySetInnerHTML` / `set:html` / `|safe` ohne explizite Sanitisierung.
- **File-Upload-Validierung** — Mehrstufig: Dateigröße → MIME-Type → Magic-Byte-Validierung → Filename-Sanitization.

## Fail Secure & Error Handling

- **Deny by Default** — Wenn Auth-Check, Validierung oder Daten-Lookup fehlschlägt → Zugriff verweigern. Niemals bei Fehlern Zugriff gewähren.
- **Error Response Sanitization** — Production-Responses dürfen KEINE Stacktraces, DB-Schema-Details, interne Dateipfade oder Server-Versionen enthalten.
- **Keine leeren Catches** — Try-Catch-Blöcke dürfen sicherheitskritische Fehler nicht verschlucken. Errors loggen, sicher behandeln, niemals ignorieren.

## Infrastructure & Production Hardening

- **Security Headers** — Mindestens: `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`.
- **CORS** — Explizite Allowlist für erlaubte Origins. `Access-Control-Allow-Origin: *` ist verboten.
- **TLS everywhere** — Alle Kommunikation über TLS 1.2+. HTTP ohne Redirect ist verboten.
- **Production Hardening** — Debug-Modi, Hot-Reload-Endpoints, Source Maps und Dev-Tools in Production NICHT aktiviert.
- **Container als non-root** — Docker-Container laufen als non-root User. Localhost-only Port-Binding in Production.
- **Keine Secrets im Code** — Alle Secrets via Environment-Variablen oder Secret-Management. `.env` in `.gitignore`. Keine Secrets in Logs.

## Rate Limiting & Abuse Prevention

- **Rate Limiting ist Baseline** — Alle API-Endpunkte MÜSSEN Rate Limiting haben. Standard, nicht "abwägen".
- **Ressourcenintensive Operationen** — Imports, Bulk-Writes, Report-Generierung: explizite Throttling-Mechanismen.
- **Bounded Processing** — Queue-Verarbeitung mit konfigurierbarer Batch-Größe, kein unbegrenztes Processing.

## Least Privilege

- **DB-Credentials** — Applikationen nutzen DB-User mit minimalen Rechten. Keine Admin/Root-Credentials in App-Config.
- **Service-Accounts** — Jeder Dienst bekommt eigene Credentials mit Scope-Einschränkung.
- **API-Keys** — Kryptografisch generiert, SHA-256-gehasht in DB gespeichert, nur einmal bei Erstellung sichtbar.

## Audit Trail

- **Activity Logging** — Sicherheitsrelevante Aktionen (Auth-Events, Datenmutationen, Admin-Operationen) protokollieren: Wer, was, wann, welche Entität.
- **Logging ist fire-and-forget** — Logging-Fehler blockieren nie den Hauptflow, werden aber als Warning geloggt.
- **Keine sensiblen Daten in Logs** — Passwords, API-Keys, Tokens, PII niemals loggen. Nur IDs und Aktionstypen.

## Secrets at Rest

- **Drittanbieter-Credentials in DB verschlüsseln** — Secrets die wieder auslesbar sein müssen (OAuth Client Secrets, API-Keys externer Dienste) werden mit AES-256-GCM verschlüsselt gespeichert. Niemals Klartext.
- **Eigene API-Keys → SHA-256-Hash**. Drittanbieter-Secrets → reversible Verschlüsselung.
- **Encrypt-on-Write / Decrypt-on-Read** — Jeder Codepfad der Drittanbieter-Secrets in die DB schreibt MUSS `encrypt()` aufrufen. Jeder Codepfad der sie liest und weitergibt MUSS `decrypt()` aufrufen.
- **Integritätsprüfung** — Vor dem Decrypt prüfen ob der Wert verschlüsselt ist (`isEncrypted()`), für Abwärtskompatibilität bei Migration.
- **Cache-Invalidierung** — Nach Credential-Updates MÜSSEN betroffene Caches (Token-Cache, Session-Cache) invalidiert werden.
