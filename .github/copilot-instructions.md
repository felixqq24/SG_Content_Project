<!-- Universelle AI Coding Standards für SG_Content_Projekt -->
<!-- Diese Datei wird automatisch von GitHub Copilot / AI-Agenten geladen. -->
<!-- Verbindlich in diesem Workspace. Projektspezifische Erweiterungen am Ende. -->

## Projekt

**SG_Content_Projekt** — Content- und Webprojekt-Hub für SGs neues Geschäftsfeld als internationale Nanny mit fachlicher Qualifikation. Der Workspace begleitet den gesamten Aufbau: Discovery-Interview → Positionierung → Messaging → Website-Konzept → Umsetzung → Reichweitenaufbau.

## Arbeitsweise in diesem Workspace

- **Phase:** Aktuell Content-/Konzept-Phase. Tech-Entscheidungen (Framework, Hosting) werden erst mit dem Website-Konzept getroffen.
- **Quellen der Wahrheit:**
  - [docs/initial_context.md](../docs/initial_context.md) — Business-Kontext, Qualifikationen, Ziele
  - [docs/decisions.md](../docs/decisions.md) — getroffene Entscheidungen (ADR-light)
  - [docs/glossary.md](../docs/glossary.md) — Fachbegriffe
  - [.github/instructions/project-knowledge.instructions.md](./instructions/project-knowledge.instructions.md) — Living Knowledge Base (wird automatisch geladen)
- **Sprache:** Inhalte und UI auf Deutsch (primär), Englisch (sekundär, "internationale Nanny"). Code und technische Kommentare auf Englisch.

> **Hinweis:** Falls Copilot die Knowledge Base nicht automatisch lädt:
> `Settings → github.copilot.chat.codeGeneration.useInstructionFiles → true`

---

## 1 — Grundprinzipien

- **Secure by Default** — Jede Konfiguration und Schnittstelle ist im Ausgangszustand sicher. Unsichere Optionen werden bewusst und dokumentiert aktiviert.
- **Zero Trust** — Keine Komponente wird implizit vertraut. Jede Anfrage wird authentifiziert, autorisiert und validiert — unabhängig vom Ursprung.
- **Fail Secure** — Bei Fehlern oder unerwarteten Zuständen fällt das System in einen sicheren Zustand. Fehler dürfen niemals Zugriff gewähren, der ohne den Fehler nicht bestünde.
- **Least Privilege** — Jeder Benutzer, Dienst und Prozess erhält ausschließlich die Berechtigungen, die für die spezifische Aufgabe erforderlich sind.
- **Input ist feindlich** — Alle externen Eingaben werden als potenziell bösartig behandelt und vor Verarbeitung validiert.
- **Defense in Depth** — Sicherheit hängt nie von einer einzelnen Maßnahme ab. Auth, Validierung, Netzwerk und Monitoring bilden unabhängige Schutzschichten.

---

## 2 — Security Standards

### 2.1 Authentication & Authorization

- **Auth an jeder Systemgrenze** — Jeder Endpunkt und jede Server Action beginnt mit einem Auth-Guard. Keine Ausnahmen außer explizit definierte Public-Routen.
- **IDOR/Object-Level Authorization** — Rollen-Check allein reicht NICHT. Jeder Zugriff auf eine Ressource MUSS prüfen, ob der anfragende User Eigentümer oder berechtigt ist.
- **Rollenbasierte Zugriffssteuerung** — Admin-Operationen erfordern explizite Admin-Prüfung. Niemals nur Frontend-basierte Zugriffskontrolle.
- **Session-Security** — Serverseitige Sessions bevorzugen. Sessions mit definierten Lebenszeiten, HttpOnly/Secure/SameSite Cookie-Flags.

### 2.2 Input-Validierung & Injection-Prävention

- **Schema-Validierung an jeder Grenze** — Alle Eingaben via Zod, Pydantic o.ä. validieren BEVOR Verarbeitung stattfindet.
- **Parametrisierte Queries** — ORM-Methoden oder parametrisierte Statements. Niemals String-Konkatenation in Queries.
- **Command Injection** — Kein `exec()`, `spawn()`, `os.system()` mit User-Input. Shell-Ausführungen nur über Allowlists.
- **XSS-Prävention** — Framework-Escaping nutzen. Kein `dangerouslySetInnerHTML` / `|safe` ohne explizite Sanitisierung.
- **File-Upload-Validierung** — Mehrstufig: Dateigröße → MIME-Type → Magic-Byte → Filename-Sanitization.

### 2.3 Fail Secure & Error Handling

- **Deny by Default** — Wenn Auth-Check, Validierung oder Daten-Lookup fehlschlägt → Zugriff verweigern.
- **Error Response Sanitization** — Production-Responses dürfen KEINE Stacktraces, DB-Schema-Details, interne Dateipfade oder Server-Versionen enthalten.
- **Keine leeren Catches** — Try-Catch-Blöcke dürfen sicherheitskritische Fehler nicht verschlucken.

### 2.4 Infrastructure & Production Hardening

- **Security Headers** — Jede Web-Applikation setzt mindestens: `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`.
- **CORS** — Explizite Allowlist. `Access-Control-Allow-Origin: *` ist verboten.
- **TLS everywhere** — Alle Kommunikation über TLS 1.2+.
- **Production Hardening** — Debug-Modi, Hot-Reload, Source Maps, Dev-Tools in Production deaktiviert.
- **Keine Secrets im Code** — Secrets via Environment-Variablen oder Secret-Management. `.env` in `.gitignore`.

---

## 3 — DSGVO & Datenschutz

- **PII-Minimierung** — Nur personenbezogene Daten erheben/speichern, die für den konkreten Zweck erforderlich sind.
- **Zweckbindung** — Daten nur für den erhobenen Zweck verwenden.
- **Löschpflichten** — Löschfristen definieren und technisch umsetzen. Right-to-Erasure (Art. 17 DSGVO) muss implementierbar sein.
- **Keine PII in Logs/Error-Reports** — Namen, E-Mail-Adressen, IPs, Zahlungsdaten gehören nicht in Log-Dateien.
- **Datenexport** — Systeme müssen perspektivisch Nutzerdaten exportieren können (Art. 20 DSGVO).
- **Einwilligungsmanagement** — Wo Einwilligung die Rechtsgrundlage ist, muss diese dokumentiert und widerrufbar sein.

### Projekt-spezifisch: Interview-Material

- **Roh-Transkripte und persönliche Aussagen** aus dem Discovery-Interview werden **nicht ins Repo committet**. `interview/raw/` ist via `.gitignore` ausgeschlossen.
- **Einwilligung vor Aufnahme** ist verpflichtend und wird in [interview/setup.md](../interview/setup.md) dokumentiert.
- **Verwertung** im Repo nur in **strukturierter, kuratierter Form** (abgeleitete Aussagen, Zitate nur mit expliziter Freigabe).

---

## 10 — AI-gestützte Entwicklung

- **KI-Output ist untrusted** — Jeder KI-generierte Code/Text wird behandelt wie Output eines Junior-Beitragenden: nicht vertrauenswürdig bis reviewed.
- **Phantom-Dependency-Schutz** — KI halluziniert Paketnamen. Jede vorgeschlagene Dependency MUSS gegen die offizielle Registry verifiziert werden.
- **Review-Fokus bei KI-Code** — Besondere Aufmerksamkeit auf: Input-Validierung, Auth-Logik, neue Dependencies, Business-Logic-Alignment.
- **Content-Review** — KI-generierte Texte für Website/Content werden vor Veröffentlichung von SG freigegeben. Keine erfundenen Referenzen, Qualifikationen oder Erfolgsgeschichten.
- **Known Pitfalls pflegen (PFLICHT)** — Jeder nicht-triviale Bugfix, falsche Annahme oder Framework-Eigenart wird SOFORT als Pitfall-Eintrag dokumentiert, bevor der Task abgeschlossen wird. Format: `**[Titel]**: Symptom → Lösung. (Bereich)`.
- **Project Knowledge Base pflegen (PFLICHT)** — Neu entdeckte Fakten (Business-Kontext, technische Entscheidungen, Workarounds) SOFORT in [.github/instructions/project-knowledge.instructions.md](./instructions/project-knowledge.instructions.md) eintragen. Keine Duplikate, max 40 Einträge.

---

## 11 — Supply Chain & Dependency Security

- **Lock-Files committen** — `package-lock.json`, `poetry.lock`, `uv.lock` etc. MÜSSEN im Repo sein.
- **Regelmäßige Audits** — `npm audit` / `pip audit` regelmäßig. Critical/High Vulnerabilities zeitnah fixen.
- **Dependency-Prüfung** — Vor jeder neuen Dependency: Lizenz prüfen, Maintainer verifizieren, CVEs checken.
- **Pinning-Strategie** — Exakte Versionen in Lock-Files. Keine offenen Ranges in Production-Dependencies.
- **Minimale Dependencies** — Kein Paket für Trivialfunktionen.

---

## 12 — Git-Workflow

- **Conventional Commits** — `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `content:`, `security:`.
- **Feature Branches** — Neue Arbeit auf separaten Branches. PR/Review für Merges nach main.
- **Keine Secrets in Git-History** — Bei versehentlichem Commit sofort rotieren.
- **Migrations append-only** — Bestehende DB-Migrations NIEMALS editieren.

---

## 13 — Coding-Konventionen (wenn Code entsteht)

- **Strict Mode** — TypeScript: `strict: true`, `noUncheckedIndexedAccess: true`. Python: Type Hints + Strict Linting.
- **Kein `any` / `@ts-ignore` / `type: ignore`** ohne dokumentierte Begründung.
- **Naming:** camelCase (Variablen/Funktionen), PascalCase (Klassen/Components), snake_case (DB-Spalten, Python).
- **Sprache:** Code und Kommentare auf Englisch. UI-Texte auf Deutsch (+ EN für internationale Zielgruppe).
- **Imports:** Konsistente Organisation. Path-Aliases (`@/` → `src/`) wo vom Framework unterstützt.

---

## 14 — Content-Standards (SG-Projekt-spezifisch)

- **Markenname:** **Riviera & Ridge** (entschieden 2026-05-31). Platzhalter `[Markenname]` wurde in allen Content-Dateien ersetzt.
- **Tonalität:** Wird im Messaging-Framework nach dem Interview definiert. Bis dahin: warm, fachlich fundiert, keine Buzzwords.
- **Faktentreue:** Qualifikationen, Erfahrungen und Referenzen nur dokumentieren wenn durch Quelle (SG direkt, Zeugnis, Referenz) belegt. Nichts erfinden.
- **Zielgruppen-Respekt:** Inhalte zu Kindern mit besonderen Bedürfnissen (Down-Syndrom, Autismus, körperliche Behinderung, Hochbegabung) in respektvoller, personenzentrierter Sprache ("Kind mit Autismus" statt "autistisches Kind"). Keine defizitäre Sprache.
- **Quellen nennen** — Externe Aussagen, Statistiken oder Studien mit Quelle versehen.

---

## 15 — Known Pitfalls

<!-- Lebende Sektion: Max 30 Einträge. Agent fügt nach nicht-trivialen Bugfixes/Fehlannahmen neue hinzu. -->
<!-- Format: **[Titel]**: Symptom → Lösung. (Bereich) -->
<!-- Vor dem Debugging: diese Sektion ZUERST prüfen! -->

*(Noch keine Einträge — werden im Projektverlauf ergänzt)*

---

<!-- ============================================================ -->
<!-- PROJEKT-SPEZIFISCHE ERWEITERUNGEN AB HIER -->
<!-- ============================================================ -->

## Projekt-spezifische Patterns

*Werden ergänzt, sobald Tech-Stack / Website-Framework entschieden ist (Phase 5).*

Archivierte technische Vorlagen (für spätere Reaktivierung) liegen in [docs/_template/](../docs/_template/).
