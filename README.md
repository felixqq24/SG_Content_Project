# {{PROJEKT}}

<!-- TODO: Projektbeschreibung hier einfügen -->

> **Template:** Erstellt aus [jf-project-template](https://github.com/jf-hospitality/jf-project-template).  
> **Stand:** {{DATUM}}

---

## Quick Start

```bash
# Dependencies installieren
{{INSTALL_COMMAND}}

# Entwicklungsserver starten
{{DEV_COMMAND}}

# Tests ausführen
{{TEST_COMMAND}}

# Build verifizieren
{{BUILD_COMMAND}}
```

---

## AI Coding Standards — Pflichtlektüre

Dieses Projekt verwendet **GitHub Copilot mit verbindlichen Coding Standards**. Die Standards werden automatisch in jede AI-Interaktion geladen und stellen sicher, dass generierter Code unseren Sicherheits-, Architektur- und Qualitätsanforderungen entspricht.

### Wie es funktioniert

1. **`.github/copilot-instructions.md`** — Diese Datei enthält die verbindlichen Standards. VS Code / GitHub Copilot lädt sie automatisch bei jeder Interaktion im Workspace.
2. **Kein Opt-out** — Die Instructions gelten für JEDEN der in diesem Repo mit Copilot arbeitet. Sie sind keine Empfehlungen, sondern Pflicht.
3. **Projekt-spezifische Erweiterungen** — Die universellen Standards können im selben File um projektspezifische Regeln erweitert werden (Framework-Patterns, Dateipfade, etc.).

### Was die Standards abdecken

| Bereich | Inhalt |
|---------|--------|
| Security | Auth-Guards, IDOR-Schutz, Input-Validierung, CORS, Security Headers, Rate Limiting |
| DSGVO | PII-Minimierung, Löschpflichten, keine personenbezogenen Daten in Logs |
| Architektur | Schichtenarchitektur, Thin API Layer, Error-Handling-Patterns |
| Datenbank | Minimale Reads, Transactions, Idempotente Writes, Connection Management |
| Testing | Domain-Logik + Security-Contracts testen, Negative Cases, Build-Validation |
| UI | WCAG AA, strukturierte Eingaben, Loading/Error States, Corporate Design |
| Observability | Strukturiertes Logging, Health-Endpoints, Error Tracking |
| API-Design | Konsistentes Error-Format, Pagination, Versionierung |
| AI-Entwicklung | Dependency-Verifikation, LLM-Output als untrusted, Review-Pflicht |
| Supply Chain | Lock-Files committen, Audits, Dependency-Prüfung |
| Git-Workflow | Conventional Commits, Feature Branches, Build vor Merge |
| **UI/UX Guidelines** | Layout, Komponenten, Zustände, Microcopy, Barrierefreiheit → [`docs/ui_ux_guidelines.md`](docs/ui_ux_guidelines.md) |
| **Engineering Guidelines** | Code-Style, API-Design, Testing-Strategie, Security, Logging → [`docs/engineering_guidelines.md`](docs/engineering_guidelines.md) |
| **E2E Testing** | Playwright-Setup, Auth-Injection, API-Mocking, Audit-Reporting → [`docs/e2e_testing_guidelines.md`](docs/e2e_testing_guidelines.md) |

### Für neue Entwickler

1. **VS Code installieren** mit GitHub Copilot Extension
2. **Repo klonen** — die Instructions sind automatisch aktiv
3. **Copilot Chat nutzen** — der Agent kennt die Standards und wendet sie an
4. **Known Pitfalls lesen** — am Ende der Instructions stehen projektspezifische Fallstricke

### Standards aktualisieren

Die universellen Standards werden zentral im [jf-project-template](https://github.com/jf-hospitality/jf-project-template) gepflegt. Um ein bestehendes Projekt zu aktualisieren:

```bash
# Aus dem jf_github_org Repo:
./sync-standards.sh /pfad/zum/projekt
```

Das Script kopiert die aktuellen universellen Standards, ohne projektspezifische Erweiterungen zu überschreiben.

---

## Projektstruktur

<!-- TODO: Projektspezifische Struktur dokumentieren -->

```
{{PROJEKT}}/
├── .github/
│   ├── copilot-instructions.md    ← AI Coding Standards (NICHT löschen)
│   ├── instructions/
│   │   └── project-knowledge.instructions.md  ← Living Knowledge Base
│   └── workflows/
│       └── ci.yml                  ← CI/CD Pipeline
├── docs/
│   ├── architecture.md            ← Systemarchitektur
│   ├── engineering_guidelines.md  ← Engineering-Standards
│   ├── e2e_testing_guidelines.md  ← E2E-Testing-Anleitung
│   ├── incident-response.md       ← Runbook & Rollback
│   └── ui_ux_guidelines.md        ← UI/UX-Standards
├── .editorconfig
├── .gitignore
├── .env.example
└── README.md
```

---

## Deployment

<!-- TODO: Projektspezifisches Deployment dokumentieren -->

Siehe [docs/architecture.md](docs/architecture.md) für Systemübersicht.  
Siehe [docs/incident-response.md](docs/incident-response.md) für Rollback & Eskalation.

---

## Neues Projekt aus diesem Template erstellen

1. **GitHub → "Use this template" → "Create a new repository"**
2. Repository klonen
3. **Init-Script ausführen** — ersetzt alle `{{PLATZHALTER}}` automatisch:
   ```bash
   chmod +x init.sh && ./init.sh
   ```
4. Projektspezifische Regeln am Ende von `.github/copilot-instructions.md` ergänzen
5. `docs/architecture.md` mit tatsächlicher Architektur befüllen
6. `docs/ui_ux_guidelines.md` — `<!-- TODO -->`-Blöcke mit projektspezifischen Patterns füllen
7. `docs/engineering_guidelines.md` — Tech-Stack-Platzhalter ersetzen, Multi-Tenancy-Abschnitte entfernen wenn nicht relevant
8. `docs/e2e_testing_guidelines.md` — Auth-Provider-Abschnitt anpassen, Audit-Szenarien ergänzen
9. `.github/instructions/project-knowledge.instructions.md` — Projektfakten eintragen (Infra, Architektur, Workarounds)
