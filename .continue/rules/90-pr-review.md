---
description: "Laden bei PR-Review, Diff-Analyse, Code-Review-Aufgaben"
alwaysApply: false
---
# PR Review

Prüfe Änderungen immer auf:

- **Tenant-Isolation** — Keine Datenlecks zwischen Mandanten
- **Security und Input-Validierung** — Alle Eingaben validiert, Auth an jeder Grenze
- **Architektur- und Domain-Konsistenz** — Keine Layer-Verletzungen, Business-Logic im richtigen Layer
- **Logging, Fehlerbehandlung, Monitoring** — Strukturiertes Logging, keine PII, Health-Checks
- **Testabdeckung und Regressionen** — Negative Cases getestet, Mocks aktuell
- **Datenminimierung und Compliance** — DSGVO, Purpose Limitation, Retention
- **Unnötige Komplexität oder stille Breaking Changes** — API-Verträge stabil, Migrations append-only

---

# Karpathy Review Checklist

**Zusätzliche Prüfung auf Karpathy-Prinzipien** (aus 00-global-operating-model.md):

- [ ] **Think Before Coding** — Waren Annahmen geklärt? Wurde bei Unklarheit gefragt? Wurden Alternativen dargestellt?
- [ ] **Simplicity First** — Ist der Code minimal? Keine spekulativen Features/Abstraktionen/Konfigurierbarkeit?
- [ ] **Surgical Changes** — Nur nötige Dateien geändert? Bestehender Style exakt gematcht? Kein Drive-by Refactoring?
- [ ] **Goal-Driven Execution** — Gab es verifizierbare Kriterien? Wurden sie geprüft (Tests, Build, Lint, manueller Check)?

> **Hinweis:** Diese Checklist gilt für **menschliche Reviews** UND **automatisierte Continue Checks** (`.continue/checks/`).


## Review- und Freigaberegeln

- Kein Merge ohne menschliches Review bei produktivem Code
- Security-, Auth-, Tenant-, MCP-, Modell- und CI-Änderungen benötigen einen zweiten Reviewer oder explizite Owner-Freigabe
- Ausnahmen müssen im PR begründet und als Ausnahme markiert werden
